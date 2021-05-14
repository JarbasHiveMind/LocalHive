from hivemind_bus_client import HiveMessageBusClient, HiveMessageType
from hivemind_bus_client.decorators import on_hive_message
from mycroft_bus_client import Message

bus = HiveMessageBusClient("CliTerminal", port=6989, ssl=False)
bus.run_in_thread()


@on_hive_message(message_type=HiveMessageType.BUS, bus=bus)
def on_mycroft(msg):
    print("\n>> " + msg.payload.msg_type)


print("HiveMindTerminal:")
while True:
    utt = input("\n")
    mycroft_msg = Message("recognizer_loop:utterance",
                          {"utterances": [utt]})
    bus.emit_mycroft(mycroft_msg)

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
