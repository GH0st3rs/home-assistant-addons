# Custom Bluetooth LE tracker component

Component rewritten to use more stable bluepy module

## Usage
For usage see [Bluetooth LE Tracker](https://www.home-assistant.io/integrations/bluetooth_le_tracker/)

## Example

```yaml
device_tracker:
 - platform: ble_tracker
   track_battery: true
   interval_seconds: 360
```
