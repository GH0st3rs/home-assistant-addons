"""Constants for the Samsung TV integration."""
import logging

LOGGER = logging.getLogger(__package__)
DOMAIN = "samsung_tv"

DEFAULT_NAME = "Samsung TV"

VALUE_CONF_NAME = "HomeAssistant"
VALUE_CONF_ID = "ha.component.samsung"

CONF_DESCRIPTION = "description"
CONF_MANUFACTURER = "manufacturer"
CONF_MODEL = "model"
CONF_ON_ACTION = "turn_on_action"

RESULT_AUTH_MISSING = "auth_missing"
RESULT_SUCCESS = "success"
RESULT_NOT_SUCCESSFUL = "not_successful"
RESULT_NOT_SUPPORTED = "not_supported"

METHOD_LEGACY = "legacy"
METHOD_WEBSOCKET = "websocket"

CODES = {
    'KEY_POWEROFF',
    'KEY_POWERON',
    'KEY_POWER',
    'KEY_SOURCE',
    'KEY_COMPONENT1',
    'KEY_COMPONENT2',
    'KEY_AV1', 'KEY_AV2', 'KEY_AV3',
    'KEY_SVIDEO1',
    'KEY_SVIDEO2',
    'KEY_SVIDEO3',
    'KEY_HDMI',
    'KEY_HDMI1',
    'KEY_HDMI2',
    'KEY_HDMI3',
    'KEY_HDMI4',
    'KEY_FM_RADIO',
    'KEY_DVI',
    'KEY_DVR',
    'KEY_TV',
    'KEY_ANTENA',
    'KEY_DTV',
    'KEY_1', 'KEY_2', 'KEY_3',
    'KEY_4', 'KEY_5', 'KEY_6',
    'KEY_7', 'KEY_8', 'KEY_9',
    'KEY_0',
    'KEY_PANNEL_CHDOWN',
    'KEY_ANYNET',
    'KEY_ESAVING',
    'KEY_SLEEP',
    'KEY_DTV_SIGNAL',
    'KEY_CHUP',
    'KEY_CHDOWN',
    'KEY_PRECH',
    'KEY_FAVCH',
    'KEY_CH_LIST',
    'KEY_AUTO_PROGRAM',
    'KEY_MAGIC_CHANNEL',
    'KEY_VOLUP',
    'KEY_VOLDOWN',
    'KEY_MUTE',
    'KEY_UP',
    'KEY_DOWN',
    'KEY_LEFT',
    'KEY_RIGHT',
    'KEY_RETURN',
    'KEY_ENTER',
    'KEY_REWIND',
    'KEY_STOP',
    'KEY_PLAY',
    'KEY_FF',
    'KEY_REC',
    'KEY_PAUSE',
    'KEY_LIVE',
    'KEY_QUICK_REPLAY',
    'KEY_STILL_PICTURE',
    'KEY_INSTANT_REPLAY',
    'KEY_PIP_ONOFF',
    'KEY_PIP_SWAP',
    'KEY_PIP_SIZE',
    'KEY_PIP_CHUP',
    'KEY_PIP_CHDOWN',
    'KEY_AUTO_ARC_PIP_SMALL',
    'KEY_AUTO_ARC_PIP_WIDE',
    'KEY_AUTO_ARC_PIP_RIGHT_BOTTOM',
    'KEY_AUTO_ARC_PIP_SOURCE_CHANGE',
    'KEY_PIP_SCAN',
    'KEY_VCR_MODE',
    'KEY_CATV_MODE',
    'KEY_DSS_MODE',
    'KEY_TV_MODE',
    'KEY_DVD_MODE',
    'KEY_STB_MODE',
    'KEY_PCMODE',
    'KEY_GREEN',
    'KEY_YELLOW',
    'KEY_CYAN',
    'KEY_RED',
    'KEY_TTX_MIX',
    'KEY_TTX_SUBFACE',
    'KEY_ASPECT',
    'KEY_PICTURE_SIZE',
    'KEY_4_3',
    'KEY_16_9',
    'KEY_EXT14',
    'KEY_EXT15',
    'KEY_PMODE',
    'KEY_PANORAMA',
    'KEY_DYNAMIC',
    'KEY_STANDARD',
    'KEY_MOVIE1',
    'KEY_GAME',
    'KEY_CUSTOM',
    'KEY_EXT9',
    'KEY_EXT10',
    'KEY_MENU',
    'KEY_TOPMENU',
    'KEY_TOOLS',
    'KEY_HOME',
    'KEY_CONTENTS',
    'KEY_GUIDE',
    'KEY_DISC_MENU',
    'KEY_DVR_MENU',
    'KEY_HELP',
    'KEY_INFO',
    'KEY_CAPTION',
    'KEY_CLOCK_DISPLAY',
    'KEY_SETUP_CLOCK_TIMER',
    'KEY_SUB_TITLE',
    'KEY_ZOOM_MOVE',
    'KEY_ZOOM_IN',
    'KEY_ZOOM_OUT',
    'KEY_ZOOM1',
    'KEY_ZOOM2',
    'KEY_WHEEL_LEFT',
    'KEY_WHEEL_RIGHT',
    'KEY_ADDDEL',
    'KEY_PLUS100',
    'KEY_AD',
    'KEY_LINK',
    'KEY_TURBO',
    'KEY_CONVERGENCE',
    'KEY_DEVICE_CONNECT',
    'KEY_11',
    'KEY_12',
    'KEY_FACTORY',
    'KEY_3SPEED',
    'KEY_RSURF',
    'KEY_FF_',
    'KEY_REWIND_',
    'KEY_ANGLE',
    'KEY_RESERVED1',
    'KEY_PROGRAM',
    'KEY_BOOKMARK',
    'KEY_PRINT',
    'KEY_CLEAR',
    'KEY_VCHIP',
    'KEY_REPEAT',
    'KEY_DOOR',
    'KEY_OPEN',
    'KEY_DMA',
    'KEY_MTS',
    'KEY_DNIe',
    'KEY_SRS',
    'KEY_CONVERT_AUDIO_MAINSUB',
    'KEY_MDC',
    'KEY_SEFFECT',
    'KEY_PERPECT_FOCUS',
    'KEY_CALLER_ID',
    'KEY_SCALE',
    'KEY_MAGIC_BRIGHT',
    'KEY_W_LINK',
    'KEY_DTV_LINK',
    'KEY_APP_LIST',
    'KEY_BACK_MHP',
    'KEY_ALT_MHP',
    'KEY_DNSe',
    'KEY_RSS',
    'KEY_ENTERTAINMENT',
    'KEY_ID_INPUT',
    'KEY_ID_SETUP',
    'KEY_ANYVIEW',
    'KEY_MS',
    'KEY_MORE',
    'KEY_MIC',
    'KEY_NINE_SEPERATE',
    'KEY_AUTO_FORMAT',
    'KEY_DNET',
    'KEY_AUTO_ARC_C_FORCE_AGING',
    'KEY_AUTO_ARC_CAPTION_ENG',
    'KEY_AUTO_ARC_USBJACK_INSPECT',
    'KEY_AUTO_ARC_RESET',
    'KEY_AUTO_ARC_LNA_ON',
    'KEY_AUTO_ARC_LNA_OFF',
    'KEY_AUTO_ARC_ANYNET_MODE_OK',
    'KEY_AUTO_ARC_ANYNET_AUTO_START',
    'KEY_AUTO_ARC_CAPTION_ON',
    'KEY_AUTO_ARC_CAPTION_OFF',
    'KEY_AUTO_ARC_PIP_DOUBLE',
    'KEY_AUTO_ARC_PIP_LARGE',
    'KEY_AUTO_ARC_PIP_LEFT_TOP',
    'KEY_AUTO_ARC_PIP_RIGHT_TOP',
    'KEY_AUTO_ARC_PIP_LEFT_BOTTOM',
    'KEY_AUTO_ARC_PIP_CH_CHANGE',
    'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS',
    'KEY_AUTO_ARC_AUTOCOLOR_FAIL',
    'KEY_AUTO_ARC_JACK_IDENT',
    'KEY_AUTO_ARC_CAPTION_KOR',
    'KEY_AUTO_ARC_ANTENNA_AIR',
    'KEY_AUTO_ARC_ANTENNA_CABLE',
    'KEY_AUTO_ARC_ANTENNA_SATELLITE',
    'KEY_PANNEL_POWER',
    'KEY_PANNEL_CHUP',
    'KEY_PANNEL_VOLUP',
    'KEY_PANNEL_VOLDOW',
    'KEY_PANNEL_ENTER',
    'KEY_PANNEL_MENU',
    'KEY_PANNEL_SOURCE',
    'KEY_PANNEL_ENTER',
    'KEY_EXT1',
    'KEY_EXT2',
    'KEY_EXT3',
    'KEY_EXT4',
    'KEY_EXT5',
    'KEY_EXT6',
    'KEY_EXT7',
    'KEY_EXT8',
    'KEY_EXT11',
    'KEY_EXT12',
    'KEY_EXT13',
    'KEY_EXT16',
    'KEY_EXT17',
    'KEY_EXT18',
    'KEY_EXT19',
    'KEY_EXT20',
    'KEY_EXT21',
    'KEY_EXT22',
    'KEY_EXT23',
    'KEY_EXT24',
    'KEY_EXT25',
    'KEY_EXT26',
    'KEY_EXT27',
    'KEY_EXT28',
    'KEY_EXT29',
    'KEY_EXT30',
    'KEY_EXT31',
    'KEY_EXT32',
    'KEY_EXT33',
    'KEY_EXT34',
    'KEY_EXT35',
    'KEY_EXT36',
    'KEY_EXT37',
    'KEY_EXT38',
    'KEY_EXT39',
    'KEY_EXT40',
    'KEY_EXT41',
}