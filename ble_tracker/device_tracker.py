"""Tracking for bluetooth low energy devices."""
import asyncio
from datetime import datetime, timedelta
import logging

from bluepy import btle
from . import gatt
import voluptuous as vol

from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.components.device_tracker.const import (
    CONF_SCAN_INTERVAL,
    CONF_TRACK_NEW,
    SCAN_INTERVAL,
    SOURCE_TYPE_BLUETOOTH_LE,
)
from homeassistant.components.device_tracker.legacy import (
    YAML_DEVICES,
    async_load_config,
)
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_point_in_utc_time
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)

CONF_TRACK_BATTERY = "track_battery"
CONF_TRACK_BATTERY_INTERVAL = "track_battery_interval"
DEFAULT_TRACK_BATTERY_INTERVAL = timedelta(days=1)
DATA_BLE = "BLE"
DATA_BLE_ADAPTER = "ADAPTER"
BLE_PREFIX = "BLE_"
MIN_SEEN_NEW = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_TRACK_BATTERY, default=False): cv.boolean,
        vol.Optional(
            CONF_TRACK_BATTERY_INTERVAL, default=DEFAULT_TRACK_BATTERY_INTERVAL
        ): cv.time_period,
    }
)


def setup_scanner(hass, config, see, discovery_info=None):
    """Set up the Bluetooth LE Scanner."""

    new_devices = {}
    hass.data.setdefault(DATA_BLE, {DATA_BLE_ADAPTER: None})

    def handle_stop(event):
        """Try to shut down the bluetooth child process nicely."""
        # These should never be unset at the point this runs, but just for
        # safety's sake, use `get`.
        adapter = hass.data.get(DATA_BLE, {}).get(DATA_BLE_ADAPTER)
        if adapter is not None:
            adapter = None

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, handle_stop)

    if config[CONF_TRACK_BATTERY]:
        battery_track_interval = config[CONF_TRACK_BATTERY_INTERVAL]
    else:
        battery_track_interval = timedelta(0)

    def see_device(address, name, new_device=False, battery=None):
        """Mark a device as seen."""
        if name is not None:
            name = name.strip()[0]

        if new_device:
            if address in new_devices:
                new_devices[address]["seen"] += 1
                if name:
                    new_devices[address]["name"] = name
                else:
                    name = new_devices[address]["name"]
                _LOGGER.info("Seen %s %s times", address, new_devices[address]["seen"])
                if new_devices[address]["seen"] < MIN_SEEN_NEW:
                    return
                _LOGGER.info("Adding %s to tracked devices", address)
                devs_to_track.append(address)
                if battery_track_interval > timedelta(0):
                    devs_track_battery[address] = dt_util.as_utc(
                        datetime.fromtimestamp(0)
                    )
            else:
                _LOGGER.info("Seen %s for the first time", address)
                new_devices[address] = {"seen": 1, "name": name}
                return

        see(
            mac=BLE_PREFIX + address,
            host_name=name,
            source_type=SOURCE_TYPE_BLUETOOTH_LE,
            battery=battery,
        )

    def discover_ble_devices():
        """Discover Bluetooth LE devices."""
        _LOGGER.info("Discovering Bluetooth LE devices")
        devices = {}
        try:
            adapter = btle.Scanner()
            hass.data[DATA_BLE][DATA_BLE_ADAPTER] = adapter
            devs = adapter.scan()
            # Parse devices
            for item in devs:
                x = list(filter(lambda d: d[0] == 9, item.getScanData()))
                devices[item.addr.upper()] = {
                    'type': item.addrType,
                    'name': item.addr.upper()if not x else x[0][2]
                }
            _LOGGER.info("Bluetooth LE devices discovered = %s", devices)
        except (RuntimeError, btle.BTLEManagementError) as error:
            _LOGGER.error("Error during Bluetooth LE scan: %s", error)
            return {}
        except btle.BTLEDisconnectError as error:
            _LOGGER.error("Error to connect Bluetooth: %s", error)
            return {}
        return devices

    yaml_path = hass.config.path(YAML_DEVICES)
    devs_to_track = []
    devs_donot_track = []
    devs_track_battery = {}

    # Load all known devices.
    # We just need the devices so set consider_home and home range
    # to 0
    for device in asyncio.run_coroutine_threadsafe(
        async_load_config(yaml_path, hass, 0), hass.loop
    ).result():
        # check if device is a valid bluetooth device
        if device.mac and device.mac[:4].upper() == BLE_PREFIX:
            address = device.mac[4:]
            if device.track:
                _LOGGER.info("Adding %s to BLE tracker", device.mac)
                devs_to_track.append(address)
                if battery_track_interval > timedelta(0):
                    devs_track_battery[address] = dt_util.as_utc(
                        datetime.fromtimestamp(0)
                    )
            else:
                _LOGGER.info("Adding %s to BLE do not track", device.mac)
                devs_donot_track.append(address)

    # if track new devices is true discover new devices
    # on every scan.
    track_new = config.get(CONF_TRACK_NEW)

    if not devs_to_track and not track_new:
        _LOGGER.warning("No Bluetooth LE devices to track!")
        return False

    interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

    def update_ble(now):
        """Lookup Bluetooth LE devices and update status."""
        devs = discover_ble_devices()
        for mac in devs_to_track:
            if mac not in devs:
                continue

            battery = None
            if mac in devs_track_battery and now > devs_track_battery[mac] + battery_track_interval:
                handle = None
                try:
                    _LOGGER.info("Reading battery for Bluetooth LE device %s", mac)
                    bt_device = gatt.connect(mac, devs[mac]['type'])
                    bt_device.setDelegate(gatt.RecvDelegate())
                    handle = gatt.BattaryDriver(bt_device)
                    # Try to get the handle; it will raise a BLEError exception if not available
                    battery = handle.get_battery_level()
                    devs_track_battery[mac] = now
                    _LOGGER.info("Readed battery status %d", battery)
                # except pygatt.exceptions.NotificationTimeout:
                    # _LOGGER.warning("Timeout when trying to get battery status")
                except Exception as err:
                    _LOGGER.warning("Could not read battery status: %s", err)
                    if handle is not None:
                        # If the device does not offer battery information, there is no point in asking again later on.
                        # Remove the device from the battery-tracked devices, so that their battery is not wasted
                        # trying to get an unavailable information.
                        del devs_track_battery[mac]
            see_device(mac, devs[mac]['name'], battery=battery)

        if track_new:
            for address in devs:
                if address not in devs_to_track and address not in devs_donot_track:
                    _LOGGER.info("Discovered Bluetooth LE device %s", address)
                    see_device(address, devs[address]['name'], new_device=True)

        track_point_in_utc_time(hass, update_ble, dt_util.utcnow() + interval)

    update_ble(dt_util.utcnow())
    return True
