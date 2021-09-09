from hivemind_bus_client import HiveMessageBusClient, HiveMessageType
from hivemind_bus_client.decorators import on_hive_message
from mycroft_bus_client import Message
from mycroft.util.log import LOG
from time import sleep
bus = HiveMessageBusClient("CliTerminal", port=6989, ssl=False)
bus.run_in_thread()


@on_hive_message(message_type=HiveMessageType.BUS, bus=bus)
def on_mycroft(msg):
    print(">> " + msg.payload.msg_type)
    if msg.payload.msg_type == "speak":
        print("Speak: " + msg.payload.data["utterance"])


print("HiveMindTerminal:")
while True:
    try:
        sleep(1)
        utt = input("<<")
        mycroft_msg = Message("recognizer_loop:utterance",
                              {"utterances": [utt]})
        bus.emit_mycroft(mycroft_msg)
    except KeyboardInterrupt:
        break

"""
HiveMindTerminal:
hello world
>> mycroft.skill.handler.start
speak:Hi to you too
>> mycroft.skill.handler.complete
tell me a joke
>> mycroft-joke.mycroftai:JokingIntent
>> mycroft.skill.handler.start
speak:How do you generate a random string? Put a first year Computer Science student in Vim and ask them to save and exit.
>> mycroft.skill.handler.complete
thank you
>> mycroft.skill.handler.start
speak:Any time.
>> mycroft.skill.handler.complete
"""
