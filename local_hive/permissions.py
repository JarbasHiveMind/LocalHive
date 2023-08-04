UTTERANCES = ["recognizer_loop:utterance"]
INTENTS = [
    "mycroft.skill.handler.start",
    "mycroft.skill.handler.complete",
    "intent.service.intent.get",
    "intent.service.skills.get",
    "intent.service.active_skills.get",
    "intent.service.adapt.get",
    "intent.service.padatious.get",
    "intent.service.adapt.manifest.get",
    "intent.service.padatious.manifest.get",
    "intent.service.adapt.vocab.manifest.get",
    "intent.service.padatious.entities.manifest.get",
    "register_vocab",
    "register_intent",
    "detach_intent",
    "detach_skill",
    "add_context",
    "remove_context",
    "clear_context",
    'padatious:register_intent',
    'padatious:register_entity',
    "mycroft.skill.set_cross_context",
    "mycroft.skill.remove_cross_context"
]
CONVERSE = [
    # "skill.converse.request",  # handle in internal protocol - localhive -> skill
    # "skill.converse.ping",  # handle in internal protocol - localhive -> skill
    "skill.converse.response",
    "skill.converse.pong",
    "active_skill_request",
    "intent.service.skills.activated",
    "intent.service.skills.deactivated",
]
SPEAK = ["speak"]
STOP = ["mycroft.stop"]

DEFAULT = INTENTS + \
          CONVERSE + \
          SPEAK + \
          ["mycroft.skills.loaded"]



