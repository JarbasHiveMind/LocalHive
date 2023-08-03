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
- by default skills only register and trigger intents, nothing else
- each skill can run in it's own .venv with it's own requirements

## Mycroftium

you can replace OpenVoiceOS/Mycroft/Neon with "Mycroftium", a hardened hivemind based stack running same skills from OpenVoiceOS

LocalHive is built on top of ovos-core, it replaces both the messagebus and skills service, skills should be launched standalone via LocalHive and are isolated from each other

The default terminals can connect to LocalHive as long as they are running on same device, eg, you can connect the voice satellite to LocalHive

- ovos-core + messagebus -> LocalHive
- ovos-audio + ovos-dinkum-listener -> HiveMind Voice Satellite
- ovos-cli-client -> HiveMind Remote Cli
- launch skills standalone, see [./examples](./examples) folder

PHAL and GUI are not yet supported under this configuration