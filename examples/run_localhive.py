from local_hive import LocalHiveListener
from os.path import join, dirname

# "system" skills
skills_folder = join(dirname(__file__), "test_skills", "local_skills")


def get_listener(port=6989):
    return LocalHiveListener(port=port)


if __name__ == "__main__":
    localmind = get_listener()
    localmind.hive.load_system_skills_folder(skills_folder)
    localmind.listen()

"""
2021-05-14 03:21:10.032 | ERROR    | 44031 | mycroft.skills.intent_services.padatious_service:__init__:44 | Padatious not installed. Falling back to Padaos, pure regex alternative
2021-05-14 03:21:10.041 | WARNING  | 44031 | mycroft.skills.intent_services.padatious_service:__init__:53 | using padaos instead of padatious. Some intents may be hard to trigger
2021-05-14 03:21:10.042 - OVOS - local_hive.master:load_system_skill:224 - INFO - Loading skill fallback-unknown.mycroftai
2021-05-14 03:21:10.046 | INFO     | 44031 | mycroft.skills.settings:get_local_settings:83 | /home/user/.config/mycroft/skills/fallback-unknown.mycroftai/settings.json
2021-05-14 03:21:10.051 - OVOS - jarbas_hive_mind:unsafe_listen:215 - INFO - HiveMind Listening (UNSECURED): ws://0.0.0.0:6989
2021-05-14 03:21:14.236 - OVOS - local_hive.master:onConnect:20 - INFO - Client connecting: tcp4:127.0.0.1:46706
2021-05-14 03:21:14.239 - OVOS - local_hive.master:onConnect:34 - INFO - HiveSkill connected CliTerminal
2021-05-14 03:21:14.243 - OVOS - jarbas_hive_mind.nodes.master:onOpen:88 - INFO - WebSocket connection open.
2021-05-14 03:21:14.245 - OVOS - jarbas_hive_mind.nodes.master:register_client:254 - INFO - registering client: tcp4:127.0.0.1:46706
2021-05-14 03:21:14.250 - OVOS - local_hive.master:onConnect:20 - INFO - Client connecting: tcp4:127.0.0.1:46708
2021-05-14 03:21:14.252 - OVOS - local_hive.master:onConnect:34 - INFO - HiveSkill connected mycroft-hello-world.mycroftai
2021-05-14 03:21:14.254 - OVOS - jarbas_hive_mind.nodes.master:onOpen:88 - INFO - WebSocket connection open.
2021-05-14 03:21:14.257 - OVOS - jarbas_hive_mind.nodes.master:register_client:254 - INFO - registering client: tcp4:127.0.0.1:46708
2021-05-14 03:21:14.260 - OVOS - local_hive.master:onConnect:20 - INFO - Client connecting: tcp4:127.0.0.1:46710
2021-05-14 03:21:14.262 - OVOS - local_hive.master:onConnect:34 - INFO - HiveSkill connected mycroft-joke.mycroftai
2021-05-14 03:21:14.265 - OVOS - jarbas_hive_mind.nodes.master:onOpen:88 - INFO - WebSocket connection open.
2021-05-14 03:21:14.267 - OVOS - jarbas_hive_mind.nodes.master:register_client:254 - INFO - registering client: tcp4:127.0.0.1:46710
2021-05-14 03:21:14.279 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-hello-world.mycroftai:HowAreYou.intent Skill: mycroft-hello-world.mycroftai
2021-05-14 03:21:14.281 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-hello-world.mycroftai:ThankYouIntent Skill: mycroft-hello-world.mycroftai
2021-05-14 03:21:14.282 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-hello-world.mycroftai:HelloWorldIntent Skill: mycroft-hello-world.mycroftai
2021-05-14 03:21:14.286 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-joke.mycroftai:JokingIntent Skill: mycroft-joke.mycroftai
2021-05-14 03:21:14.287 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-joke.mycroftai:ChuckJokeIntent Skill: mycroft-joke.mycroftai
2021-05-14 03:21:14.288 - OVOS - local_hive.master:handle_intent_service_message:115 - INFO - Register Intent: mycroft-joke.mycroftai:NeutralJokeIntent Skill: mycroft-joke.mycroftai
2021-05-14 03:21:44.855 - OVOS - local_hive.master:handle_incoming_mycroft:172 - INFO - Utterance: ['hello world'] Peer: tcp4:127.0.0.1:46706
2021-05-14 03:21:44.882 - OVOS - local_hive.master:handle_intent_service_message:124 - INFO - Intent: mycroft-hello-world.mycroftai:HelloWorldIntent Skill: mycroft-hello-world.mycroftai Source: tcp4:127.0.0.1:46706 Target: tcp4:127.0.0.1:46708
2021-05-14 03:21:44.887 - OVOS - local_hive.master:handle_skill_message:209 - DEBUG - destination: tcp4:127.0.0.1:46706 skill:mycroft-hello-world.mycroftai type:mycroft.skill.handler.start
2021-05-14 03:21:44.889 - OVOS - local_hive.master:handle_skill_message:209 - DEBUG - destination: tcp4:127.0.0.1:46706 skill:mycroft-hello-world.mycroftai type:speak
2021-05-14 03:21:44.891 - OVOS - local_hive.master:handle_skill_message:209 - DEBUG - destination: tcp4:127.0.0.1:46706 skill:mycroft-hello-world.mycroftai type:mycroft.skill.handler.complete
"""