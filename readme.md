# LocalHive

The LocalHive is a hardened OpenVoiceOS skills service, the messagebus is replaced with a hivemind connection

https://github.com/JarbasHiveMind/LocalHive

_"security as a requirement, not a feature"_

- the LocalHive is HTTP only
- the LocalHive uses no crypto
- the LocalHive does not require accessKey, instead it only accepts connections coming from 0.0.0.0
- the LocalHive rejects all connections not coming from 0.0.0.0
- the LocalHive runs in port 6989
- skills can not listen to each other's traffic
- skills can only inject whitelisted messages to LocalHive (by default intents + converse + speak)
- by default skills only register and trigger intents, nothing else
- each skill can run in it's own .venv with it's own requirements
- TODO - skills should be able to request to listen for specific messages, cross skill communication is currently impossible

## Mycroftium

you can replace OpenVoiceOS/Mycroft/Neon with "Mycroftium", a hardened hivemind based stack running same skills from OpenVoiceOS

LocalHive is built on top of ovos-core, it replaces both the messagebus and skills service, skills should be launched standalone via LocalHive and are isolated from each other

The default terminals can connect to LocalHive as long as they are running on same device, eg, you can connect the voice satellite to LocalHive

- ovos-core + messagebus -> LocalHive
- ovos-audio + ovos-dinkum-listener -> HiveMind Voice Satellite
- ovos-cli-client -> HiveMind Remote Cli
- launch skills standalone, see [./examples](./examples) folder

PHAL and GUI are not yet supported under this configuration

### Skill Permissions

default permissions for skills can be found in [permissions.py](./local_hive/permissions.py)

you can allow new messages per skill_id by editing the json file at `~/.config/LocalHive/skill_permissions.json`

```
{
    "ovos-stop.openvoiceos": ["mycroft.stop"]
}
```

### Usage Logs

launch local hive
```
/home/miro/PycharmProjects/LocalHive/local_hive/__main__.py
2023-08-03 23:11:54.934 - HiveMind - local_hive.service:on_alive:26 - INFO - LocalHive service alive
2023-08-03 23:11:55.275 - HiveMind - ovos_core.transformers:load_plugins:32 - INFO - loaded utterance transformer plugin: ovos-utterance-coref-normalizer
2023-08-03 23:11:55.276 - HiveMind - ovos_core.transformers:load_plugins:32 - INFO - loaded utterance transformer plugin: ovos-utterance-normalizer
2023-08-03 23:11:55.284 - HiveMind - local_hive.service:on_started:30 - INFO - LocalHive service started!
2023-08-03 23:11:55.284 - HiveMind - local_hive.service:run:109 - INFO - ws connection started
2023-08-03 23:11:55.285 - HiveMind - local_hive.service:on_ready:22 - INFO - LocalHive service ready!
```

connect a skill to local hive
```
/home/miro/.venvs/HiveMind/bin/python /home/miro/PycharmProjects/LocalHive/examples/jokes_skill.py
2023-08-03 23:11:59.640 - OVOS - hivemind_bus_client.protocol:bind:99 - INFO - Initializing HiveMindSlaveInternalProtocol
2023-08-03 23:11:59.640 - OVOS - hivemind_bus_client.protocol:bind:102 - INFO - registering protocol handlers
2023-08-03 23:11:59.642 - OVOS - hivemind_bus_client.client:connect:116 - INFO - Connecting to Hivemind
2023-08-03 23:11:59.646 - OVOS - hivemind_bus_client.protocol:bind:99 - INFO - Initializing HiveMindSlaveInternalProtocol
2023-08-03 23:11:59.646 - OVOS - hivemind_bus_client.protocol:bind:102 - INFO - registering protocol handlers
2023-08-03 23:11:59.651 - OVOS - hivemind_bus_client.protocol:handle_hello:128 - INFO - HELLO: {'handshake': False, 'crypto': False, 'peer': 'HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e', 'node_id': 'master:0.0.0.0'}
2023-08-03 23:11:59.652 - OVOS - hivemind_bus_client.protocol:handle_hello:133 - INFO - Connected to HiveMind: master:0.0.0.0
2023-08-03 23:11:59.654 - OVOS - hivemind_bus_client.protocol:handle_handshake:169 - INFO - HANDSHAKE: {'handshake': False, 'binarize': False, 'preshared_key': False, 'password': False, 'crypto_required': False}
2023-08-03 23:11:59.657 - OVOS - ovos_workshop.skill_launcher:load:295 - INFO - ATTEMPTING TO LOAD SKILL: mycroft-joke.mycroftai
2023-08-03 23:11:59.669 - OVOS - mycroft:<module>:37 - WARNING - mycroft has been deprecated! please start importing from ovos_core and companion packages
mycroft module remains available for backwards compatibility and will be removed in version 0.2.0
2023-08-03 23:11:59.673 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.stop
2023-08-03 23:11:59.674 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: skill.converse.ping
2023-08-03 23:11:59.675 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: skill.converse.request
2023-08-03 23:11:59.675 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft-joke.mycroftai.activate
2023-08-03 23:11:59.676 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft-joke.mycroftai.deactivate
2023-08-03 23:11:59.676 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: intent.service.skills.deactivated
2023-08-03 23:11:59.677 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: intent.service.skills.activated
2023-08-03 23:11:59.677 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skill.enable_intent
2023-08-03 23:11:59.678 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skill.disable_intent
2023-08-03 23:11:59.679 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skill.set_cross_context
2023-08-03 23:11:59.679 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skill.remove_cross_context
2023-08-03 23:11:59.680 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skills.settings.changed
2023-08-03 23:11:59.681 - OVOS - ovos_utils.gui:get_ui_directories:94 - INFO - Checking for legacy UI directories
2023-08-03 23:11:59.682 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skills.settings.update
2023-08-03 23:11:59.683 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skills.settings.download
2023-08-03 23:11:59.684 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skills.settings.upload
2023-08-03 23:11:59.684 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.skills.settings.upload.meta
2023-08-03 23:11:59.685 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft.paired
2023-08-03 23:11:59.689 - OVOS - mycroft.deprecated.skills.settings:__init__:99 - WARNING - skill_name is deprecated! use skill_id instead
2023-08-03 23:11:59.694 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.694 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.695 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.696 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.697 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.698 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.700 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.700 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.701 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.702 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.703 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.704 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.705 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.705 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.707 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.707 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.709 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.709 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.710 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_vocab
2023-08-03 23:11:59.711 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.712 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_intent
2023-08-03 23:11:59.713 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.714 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft-joke.mycroftai:NeutralJokeIntent
2023-08-03 23:11:59.715 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_intent
2023-08-03 23:11:59.716 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.717 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft-joke.mycroftai:ChuckJokeIntent
2023-08-03 23:11:59.718 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: register_intent
2023-08-03 23:11:59.719 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.719 - OVOS - ovos_utils.events:add:155 - DEBUG - Added event: mycroft-joke.mycroftai:JokingIntent
2023-08-03 23:11:59.720 - OVOS - local_hive.loader:emit:37 - DEBUG - <<: mycroft.skills.loaded
2023-08-03 23:11:59.720 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
2023-08-03 23:11:59.720 - OVOS - ovos_workshop.skill_launcher:_communicate_load_status:506 - INFO - Skill mycroft-joke.mycroftai loaded successfully
```

see skill loading in local hive logs
```
2023-08-03 23:11:59.646 - HiveMind - local_hive.service:open:47 - INFO - authorizing skill_id: mycroft-joke.mycroftai
2023-08-03 23:11:59.647 - HiveMind - local_hive.protocol:handle_new_client:145 - INFO - new client: HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e
2023-08-03 23:11:59.649 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e: {"msg_type": "hello", "payload": {"handshake": false, "crypto": false, "peer": "HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e", "node_id": "master:0.0.0.0"}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.652 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e: {"msg_type": "shake", "payload": {"handshake": false, "binarize": false, "preshared_key": false, "password": false, "crypto_required": false}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.696 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "chuck", "entity_type": "mycroft_joke_mycroftaiChuck", "lang": "en-us", "start": "chuck", "end": "mycroft_joke_mycroftaiChuck"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.697 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "chuck", "entity_type": "mycroft_joke_mycroftaiChuck", "lang": "en-us", "start": "chuck", "end": "mycroft_joke_mycroftaiChuck"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.698 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "chuck norris", "entity_type": "mycroft_joke_mycroftaiChuck", "lang": "en-us", "start": "chuck norris", "end": "mycroft_joke_mycroftaiChuck"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.699 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "chuck norris", "entity_type": "mycroft_joke_mycroftaiChuck", "lang": "en-us", "start": "chuck norris", "end": "mycroft_joke_mycroftaiChuck"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.701 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "neutral", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "neutral", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.702 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "neutral", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "neutral", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.703 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "non-offensive", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "non-offensive", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.704 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "non-offensive", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "non-offensive", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.706 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "geeky", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "geeky", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.707 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "geeky", "entity_type": "mycroft_joke_mycroftaiNeutral", "lang": "en-us", "start": "geeky", "end": "mycroft_joke_mycroftaiNeutral"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.709 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "joke", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "joke", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.710 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "joke", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "joke", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.711 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "jokes", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "jokes", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.712 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "jokes", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "jokes", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.714 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "make me laugh", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "make me laugh", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.715 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "make me laugh", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "make me laugh", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.717 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "brighten my day", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "brighten my day", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.717 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "brighten my day", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "brighten my day", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.719 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "tell me joke", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "tell me joke", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.720 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_vocab", "data": {"entity_value": "tell me joke", "entity_type": "mycroft_joke_mycroftaiJoke", "lang": "en-us", "start": "tell me joke", "end": "mycroft_joke_mycroftaiJoke"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.722 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:NeutralJokeIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"], ["mycroft_joke_mycroftaiNeutral", "mycroft_joke_mycroftaiNeutral"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.723 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:NeutralJokeIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"], ["mycroft_joke_mycroftaiNeutral", "mycroft_joke_mycroftaiNeutral"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.725 - HiveMind - local_hive.protocol:handle_internal_mycroft:84 - INFO - Register Intent: mycroft-joke.mycroftai:NeutralJokeIntent Skill: mycroft-joke.mycroftai
2023-08-03 23:11:59.726 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:ChuckJokeIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"], ["mycroft_joke_mycroftaiChuck", "mycroft_joke_mycroftaiChuck"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.727 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:ChuckJokeIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"], ["mycroft_joke_mycroftaiChuck", "mycroft_joke_mycroftaiChuck"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.728 - HiveMind - local_hive.protocol:handle_internal_mycroft:84 - INFO - Register Intent: mycroft-joke.mycroftai:ChuckJokeIntent Skill: mycroft-joke.mycroftai
2023-08-03 23:11:59.729 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:JokingIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.730 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "register_intent", "data": {"name": "mycroft-joke.mycroftai:JokingIntent", "requires": [["mycroft_joke_mycroftaiJoke", "mycroft_joke_mycroftaiJoke"]], "at_least_one": [], "optional": []}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.732 - HiveMind - local_hive.protocol:handle_internal_mycroft:84 - INFO - Register Intent: mycroft-joke.mycroftai:JokingIntent Skill: mycroft-joke.mycroftai
2023-08-03 23:11:59.733 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::20170943-4dd9-4714-9c55-b2129fefa10e message: {"msg_type": "bus", "payload": {"type": "mycroft.skills.loaded", "data": {"path": "/home/miro/PycharmProjects/LocalHive/examples/test_skills/mycroft-joke.mycroftai", "id": "mycroft-joke.mycroftai", "name": "JokingSkill"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:11:59.734 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "mycroft.skills.loaded", "data": {"path": "/home/miro/PycharmProjects/LocalHive/examples/test_skills/mycroft-joke.mycroftai", "id": "mycroft-joke.mycroftai", "name": "JokingSkill"}, "context": {"skill_id": "mycroft-joke.mycroftai", "source": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
```

test skills via cli terminal, connect to LocalHive instead of the standard hivemind-core
```
/home/miro/.venvs/HiveMind/bin/python /home/miro/PycharmProjects/hivemind_websocket_client/hivemind_bus_client/scripts.py terminal --port 6989 --host ws://127.0.0.1
2023-08-03 23:12:04.214 - OVOS - ovos_bus_client.conf:load_message_bus_config:28 - DEBUG - Loading message bus configs
2023-08-03 23:12:04.237 - OVOS - hivemind_bus_client.client:connect:110 - DEBUG - Initializing HiveMindSlaveProtocol
2023-08-03 23:12:04.237 - OVOS - hivemind_bus_client.client:connect:116 - INFO - Connecting to Hivemind
2023-08-03 23:12:04.243 - OVOS - ovos_bus_client.client.client:on_open:86 - DEBUG - Connected
2023-08-03 23:12:04.245 - OVOS - hivemind_bus_client.protocol:bind:99 - INFO - Initializing HiveMindSlaveInternalProtocol
2023-08-03 23:12:04.246 - OVOS - hivemind_bus_client.protocol:bind:102 - INFO - registering protocol handlers
2023-08-03 23:12:04.246 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.HELLO
2023-08-03 23:12:04.247 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.BROADCAST
2023-08-03 23:12:04.248 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.PROPAGATE
2023-08-03 23:12:04.249 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.ESCALATE
2023-08-03 23:12:04.249 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.SHARED_BUS
2023-08-03 23:12:04.250 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.BUS
2023-08-03 23:12:04.251 - OVOS - hivemind_bus_client.client:on:280 - DEBUG - registering handler: HiveMessageType.HANDSHAKE
2023-08-03 23:12:09.252 - OVOS - hivemind_bus_client.protocol:start_handshake:139 - INFO - hivemind does not support binarization protocol
2023-08-03 23:12:09.254 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.HANDSHAKE
2023-08-03 23:12:09.259 - OVOS - hivemind_bus_client.protocol:handle_handshake:169 - INFO - HANDSHAKE: {'handshake': False, 'binarize': False, 'preshared_key': False, 'password': False, 'crypto_required': False}
== connected to HiveMind
2023-08-03 23:12:09.260 - OVOS - hivemind_bus_client.client:on_mycroft:265 - DEBUG - registering mycroft event: speak
Utterance: joke
2023-08-03 23:19:10.240 - OVOS - hivemind_bus_client.client:emit:220 - DEBUG - sending to HiveMind: HiveMessageType.BUS
Utterance:2023-08-03 23:19:10.554 - OVOS - hivemind_bus_client.protocol:handle_bus:196 - INFO - BUS: mycroft.skill.handler.start
>  What do you get when you cross a cat and a dog? Cat dog sin theta.
2023-08-03 23:19:10.567 - OVOS - hivemind_bus_client.protocol:handle_bus:196 - INFO - BUS: speak
2023-08-03 23:19:10.572 - OVOS - hivemind_bus_client.protocol:handle_bus:196 - INFO - BUS: mycroft.skill.handler.complete
```

and local hive logs side you will see
```
2023-08-03 23:12:04.239 - HiveMind - local_hive.service:open:47 - INFO - authorizing skill_id: None
2023-08-03 23:12:04.240 - HiveMind - local_hive.protocol:handle_new_client:145 - INFO - new client: HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45
2023-08-03 23:12:04.241 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45: {"msg_type": "hello", "payload": {"handshake": false, "crypto": false, "peer": "HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45", "node_id": "master:0.0.0.0"}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:12:04.243 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45: {"msg_type": "shake", "payload": {"handshake": false, "binarize": false, "preshared_key": false, "password": false, "crypto_required": false}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:12:09.255 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45 message: {"msg_type": "shake", "payload": {"pubkey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nxsFNBGSHvhEBEACxtTiq1Hhp64mG7JMO7xJhu8wJEqHislAhTBD9s7SM4kbUU4Zl\nlvEbCUsI3en3sxDLfD/kpgENCxLqGQIPeI0mN2c7LyR/DQwJjnkmHQqtQELoFV4G\nFRFndDuQZSrdR8TMuw6ric9b1kRH+W75s+s68YRm5JffEWyFAG/QtI0aqfL7OYpw\nxovOUf6txkZwtHkH1aBTxDMo4e6/TzHCWnhUYZIMuRYg2JtdjntzGVZ8HIoFnCCd\nvcbAvuMZKdji/0O/kF45EjZTO13TpBMMeLp4wIm89v240TO3m2V47sbnIbwXYp5+\nlhF+bX/ifPFWzROx3u0UNBDfhx+ZhhCRs8KmIppvZIhvPjz+yyk+BoRl1gf9gt0M\nFl4BJuZpI0JrSzzHQWiP1FzlQwlMbhFIQKsSjSxbfic4Ze8Iad645m44/TJ+14m1\nunU+vqMuKCcvMdMxv17dP66w1vAAAbf7MXhTF86OQeWCthnF02cnwhqmEpHVLhd5\nODGu9xuWfrLlo0gTffB4VLAWjCxHVwWbr19MGLuvFQS0tkjkBNb21PNVElBp9Fj0\n6xDsIl/NDSXSFHSYGlGr/K9epSSkkSC7vfjvqHBciQ6jQHhwFsk74tK6kO4oGu4t\nde3O+qWLmcUuo/5DctB1Oi503VTC66yhAYGte0+NyY3uy8OSt0MLcePL+QARAQAB\nzRBQb29yTWFuSGFuZHNoYWtlwsGGBBMBCgAwBQJkh74RAhsGAwsJDQMVCggEFgMB\nAAIeARYhBHE9qveHL6LFO1QCXR3P0r+CuxRiAAoJEB3P0r+CuxRi/4YP/i2ouyvR\nvrvqyH12ggrUSWDgoR5FVRcw15pe60LVGsetCr0/w50o1KRbT/LMbPue1gfFBqrd\nkik31HHeTZ7vDbmOmpOG4kWqaFbDEkTsBwT/U6R3H67SeeknG8EFzr0Ef5mUkC/2\nz6c3LE+HH1D4coigo7FztiixOIqlM1oGXUxF+3zToDozfMDM45h0JLoxJ+jGx/ti\n+w6hKZo+2uBlGXr04juTMZknPaa39rTJa3hwWRaWzyZZYABKiQoue+/isRp8x9N0\ne0wO+2yUIpYPyiBfpQ7HEElexGBOV6m2IhtFz1cfoEgnFzK7PhJ+/qK4BF/U/SeR\n5CnUToFbTnSVHy5EuIgbV+WM2ge7B7RVCT2TP9Reak6rR1yzR2tz5H01opGIHC2t\nw4DJS3JWmeddLJpvJZY4VF0v9ZpEcgpOCa7HtmfvWjnKMynnewuolcFbCLnAjkFT\n8IPz8TC7sxjpgEIYstgh3YiLsLC4D9IHC6VXfeUKzTpqy2W6xNAsMy/6guKT8tNe\nTckqx+UIK0oRlGQTclXQ8kmMTPSr8/glwAzHB+KsjkM7Pu8iNMx9BV3n5Wwh+C+8\nehuP1dbn3zOM6dlLz/MCb9dw91abdAUZ6izzyCCzODKDgKipcqZuBhDH9Uwj99CZ\n2tWsxdwC9K/URD9AwIchuhc1TD3Laeb3eQST\n=93WR\n-----END PGP PUBLIC KEY BLOCK-----\n", "binarize": false}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:12:09.256 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "shake", "payload": {"pubkey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nxsFNBGSHvhEBEACxtTiq1Hhp64mG7JMO7xJhu8wJEqHislAhTBD9s7SM4kbUU4Zl\nlvEbCUsI3en3sxDLfD/kpgENCxLqGQIPeI0mN2c7LyR/DQwJjnkmHQqtQELoFV4G\nFRFndDuQZSrdR8TMuw6ric9b1kRH+W75s+s68YRm5JffEWyFAG/QtI0aqfL7OYpw\nxovOUf6txkZwtHkH1aBTxDMo4e6/TzHCWnhUYZIMuRYg2JtdjntzGVZ8HIoFnCCd\nvcbAvuMZKdji/0O/kF45EjZTO13TpBMMeLp4wIm89v240TO3m2V47sbnIbwXYp5+\nlhF+bX/ifPFWzROx3u0UNBDfhx+ZhhCRs8KmIppvZIhvPjz+yyk+BoRl1gf9gt0M\nFl4BJuZpI0JrSzzHQWiP1FzlQwlMbhFIQKsSjSxbfic4Ze8Iad645m44/TJ+14m1\nunU+vqMuKCcvMdMxv17dP66w1vAAAbf7MXhTF86OQeWCthnF02cnwhqmEpHVLhd5\nODGu9xuWfrLlo0gTffB4VLAWjCxHVwWbr19MGLuvFQS0tkjkBNb21PNVElBp9Fj0\n6xDsIl/NDSXSFHSYGlGr/K9epSSkkSC7vfjvqHBciQ6jQHhwFsk74tK6kO4oGu4t\nde3O+qWLmcUuo/5DctB1Oi503VTC66yhAYGte0+NyY3uy8OSt0MLcePL+QARAQAB\nzRBQb29yTWFuSGFuZHNoYWtlwsGGBBMBCgAwBQJkh74RAhsGAwsJDQMVCggEFgMB\nAAIeARYhBHE9qveHL6LFO1QCXR3P0r+CuxRiAAoJEB3P0r+CuxRi/4YP/i2ouyvR\nvrvqyH12ggrUSWDgoR5FVRcw15pe60LVGsetCr0/w50o1KRbT/LMbPue1gfFBqrd\nkik31HHeTZ7vDbmOmpOG4kWqaFbDEkTsBwT/U6R3H67SeeknG8EFzr0Ef5mUkC/2\nz6c3LE+HH1D4coigo7FztiixOIqlM1oGXUxF+3zToDozfMDM45h0JLoxJ+jGx/ti\n+w6hKZo+2uBlGXr04juTMZknPaa39rTJa3hwWRaWzyZZYABKiQoue+/isRp8x9N0\ne0wO+2yUIpYPyiBfpQ7HEElexGBOV6m2IhtFz1cfoEgnFzK7PhJ+/qK4BF/U/SeR\n5CnUToFbTnSVHy5EuIgbV+WM2ge7B7RVCT2TP9Reak6rR1yzR2tz5H01opGIHC2t\nw4DJS3JWmeddLJpvJZY4VF0v9ZpEcgpOCa7HtmfvWjnKMynnewuolcFbCLnAjkFT\n8IPz8TC7sxjpgEIYstgh3YiLsLC4D9IHC6VXfeUKzTpqy2W6xNAsMy/6guKT8tNe\nTckqx+UIK0oRlGQTclXQ8kmMTPSr8/glwAzHB+KsjkM7Pu8iNMx9BV3n5Wwh+C+8\nehuP1dbn3zOM6dlLz/MCb9dw91abdAUZ6izzyCCzODKDgKipcqZuBhDH9Uwj99CZ\n2tWsxdwC9K/URD9AwIchuhc1TD3Laeb3eQST\n=93WR\n-----END PGP PUBLIC KEY BLOCK-----\n", "binarize": false}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:12:09.258 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f6f72ed7-22c6-4e10-bdf9-6bb28f321f45: {"msg_type": "shake", "payload": {"handshake": false, "binarize": false, "preshared_key": false, "password": false, "crypto_required": false}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.243 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab message: {"msg_type": "bus", "payload": {"type": "recognizer_loop:utterance", "data": {"utterances": ["joke"]}, "context": {"destination": "skills"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.244 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "recognizer_loop:utterance", "data": {"utterances": ["joke"]}, "context": {"destination": "skills"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.245 - HiveMind - local_hive.protocol:handle_inject_mycroft_msg:205 - INFO - Utterance: ['joke'] Peer: HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab
2023-08-03 23:19:10.508 - HiveMind - local_hive.protocol:handle_internal_mycroft:37 - INFO - Converse ping
2023-08-03 23:19:10.534 - HiveMind - padacioso:calc_intent:240 - INFO - No match
2023-08-03 23:19:10.538 - HiveMind - local_hive.protocol:handle_internal_mycroft:71 - INFO - Intent: mycroft-joke.mycroftai:JokingIntent Skill: mycroft-joke.mycroftai Source: HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab Target: HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e
2023-08-03 23:19:10.540 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e: {"msg_type": "bus", "payload": {"type": "mycroft-joke.mycroftai:JokingIntent", "data": {"utterances": ["joke"], "utterance": "joke", "intent_type": "mycroft-joke.mycroftai:JokingIntent", "mycroft_joke_mycroftaiJoke": "joke", "target": null, "confidence": 1.0, "__tags__": [{"match": "joke", "key": "joke", "start_token": 0, "entities": [{"key": "joke", "match": "joke", "data": [["joke", "mycroft_joke_mycroftaiJoke"]], "confidence": 1.0}], "end_token": 0, "from_context": false}]}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "skills", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.548 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e message: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.start", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.549 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.start", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.552 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.start", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.554 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e message: {"msg_type": "bus", "payload": {"type": "enclosure.active_skill", "data": {"skill_id": "mycroft-joke.mycroftai"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.555 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "enclosure.active_skill", "data": {"skill_id": "mycroft-joke.mycroftai"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.561 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e message: {"msg_type": "bus", "payload": {"type": "speak", "data": {"utterance": "What do you get when you cross a cat and a dog? Cat dog sin theta.", "expect_response": false, "meta": {"skill": "mycroft-joke.mycroftai"}, "lang": "en-us"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.562 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "speak", "data": {"utterance": "What do you get when you cross a cat and a dog? Cat dog sin theta.", "expect_response": false, "meta": {"skill": "mycroft-joke.mycroftai"}, "lang": "en-us"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.564 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab: {"msg_type": "bus", "payload": {"type": "speak", "data": {"utterance": "What do you get when you cross a cat and a dog? Cat dog sin theta.", "expect_response": false, "meta": {"skill": "mycroft-joke.mycroftai"}, "lang": "en-us"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.567 - HiveMind - hivemind_core.service:on_message:114 - INFO - received HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e message: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.complete", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.568 - HiveMind - hivemind_core.protocol:handle_message:303 - INFO - message: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.complete", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "IntentService", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
2023-08-03 23:19:10.570 - HiveMind - hivemind_core.protocol:send:78 - INFO - sending to HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab: {"msg_type": "bus", "payload": {"type": "mycroft.skill.handler.complete", "data": {"name": "JokingSkill.handle_general_joke"}, "context": {"destination": "HiveMessageBusClientV0.0.1:127.0.0.1::f7dd4386-9937-4d0a-8107-47776e290aab", "source": "HiveMessageBusClientV0.0.1:127.0.0.1::d422ee21-59f1-4e15-a485-40daa14b404e", "lang": "en-us", "skill_id": "mycroft-joke.mycroftai"}}, "route": [], "node": null, "source_peer": null}
```
