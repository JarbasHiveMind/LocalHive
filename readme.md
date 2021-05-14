# LocalHive

The LocalHive is a hardened mycroft skills service, the mycroft messagebus is replaced with a hivemind connection

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


LocalHive is built on top of HolmesV and **can not coexist with mycroft-core, it replaces it**, be sure to use a dedicated .venv

The default terminals can connect to LocalHive as long as they are running on same device, the full mycroft stack can be replaced with the equivalent terminal (WIP audio service)