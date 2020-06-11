# Integration for Samsung TV

Integration for Samsung TV based on [original component](https://www.home-assistant.io/integrations/samsungtv/) and [home-assistant-custom-components](https://github.com/p3g4asus/home-assistant-custom-components#samsungctl_remote)


### Sending commands

The supported commands can be found [here](https://github.com/kdschlosser/samsungctl/blob/master/samsungctl/key_mappings.py).

Examples of command list:

example| action
:--- | :---
`"ch345"`| will send `KEY_3`, `KEY_4` and `KEY_5` in sequence
`"KEY_SOURCE#3"`| will send `KEY_SOURCE`, three times
`"KEY_SOURCE","t1","KEY_LEFT","t0.5","KEY_LEFT"`| will send `KEY_SOURCE`, wait 1s, send `KEY_LEFT`, wait 0.5s and send `KEY_LEFT`.


### Changing channels

Changing channels can be done by calling the `media_player.play_media` service with the following payload:

```yaml
entity_id: media_player.samsung_tv
media_content_id: KEY_VOLUP,t1,KEY_VOLUP,t0.5,KEY_VOLDOWN
media_content_type: channel
```
