from threading import Lock

from hivemind_bus_client import HiveMessageBusClient
from hivemind_bus_client.decorators import on_mycroft_message
from mycroft import dialog
from mycroft.audio.audioservice import AudioService
from mycroft.client.speech.listener import RecognizerLoop
from mycroft.configuration import setup_locale
from mycroft.messagebus.message import Message
from mycroft.tts import TTSFactory
from mycroft.util import (
    create_daemon,
    wait_for_exit_signal
)
from mycroft.util.log import LOG

lock = Lock()
loop = None
tts = None
audio = None
config = {}

client_id = "HiveMindAudio"
bus = HiveMessageBusClient(client_id, port=6989, ssl=False)
bus.run_in_thread()


def handle_record_begin():
    """Forward internal bus message to external bus."""
    LOG.info("Begin Recording...")
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(Message('recognizer_loop:record_begin', context=context))


def handle_record_end():
    """Forward internal bus message to external bus."""
    LOG.info("End Recording...")
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(Message('recognizer_loop:record_end', context=context))


def handle_no_internet():
    LOG.debug("Notifying enclosure of no internet connection")
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(Message('enclosure.notify.no_internet', context=context))


def handle_awoken():
    """Forward mycroft.awoken to the messagebus."""
    LOG.info("Listener is now Awake: ")
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(Message('mycroft.awoken', context=context))


def handle_wakeword(event):
    LOG.info("Wakeword Detected: " + event['utterance'])
    bus.emit_mycroft(Message('recognizer_loop:wakeword', event))


def handle_utterance(event):
    LOG.info("Utterance: " + str(event['utterances']))
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    if 'ident' in event:
        ident = event.pop('ident')
        context['ident'] = ident
    bus.emit_mycroft(Message('recognizer_loop:utterance', event, context))


def handle_unknown():
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(
        Message('mycroft.speech.recognition.unknown', context=context))


@on_mycroft_message("speak", bus=bus)
def handle_speak(event):
    """
       execute TTS
    """
    listen = event.data.get('expect_response', False)
    utterance = event.data['utterance']
    LOG.info("Speak: " + utterance)
    try:
        tts.execute(utterance, "", listen)
    except Exception:
        LOG.exception('TTS execution failed.')


@on_mycroft_message("complete_intent_failure", bus=bus)
def handle_complete_intent_failure(event):
    """Extreme backup for answering completely unhandled intent requests."""
    LOG.info("Failed to find intent.")
    data = {'utterance': dialog.get('not.loaded')}
    context = {'client_name': client_id,
               'source': client_id,
               'destination': ["JarbasHiveMind"]}
    bus.emit_mycroft(Message('speak', data, context))


@on_mycroft_message("recognizer_loop:sleep", bus=bus)
def handle_sleep(event):
    """Put the recognizer loop to sleep."""
    loop.sleep()


@on_mycroft_message("recognizer_loop:wake_up", bus=bus)
def handle_wake_up(event):
    """Wake up the the recognize loop."""
    loop.awaken()


@on_mycroft_message("mycroft.mic.mute", bus=bus)
def handle_mic_mute(event):
    """Mute the listener system."""
    loop.mute()


@on_mycroft_message("mycroft.mic.unmute", bus=bus)
def handle_mic_unmute(event):
    """Unmute the listener system."""
    loop.unmute()


@on_mycroft_message("mycroft.mic.listen", bus=bus)
def handle_mic_listen(_):
    """Handler for mycroft.mic.listen.

    Starts listening as if wakeword was spoken.
    """
    loop.responsive_recognizer.trigger_listen()


@on_mycroft_message("mycroft.mic.get_status", bus=bus)
def handle_mic_get_status(event):
    """Query microphone mute status."""
    data = {'muted': loop.is_muted()}
    bus.emit_mycroft(event.response(data))


@on_mycroft_message("recognizer_loop:audio_output_start", bus=bus)
def handle_audio_start(event):
    """Mute recognizer loop."""
    if config.get("listener", {}).get("mute_during_output"):
        loop.mute()


@on_mycroft_message("recognizer_loop:audio_output_end", bus=bus)
def handle_audio_end(event):
    """Request unmute, if more sources have requested the mic to be muted
    it will remain muted.
    """
    if config.get("listener", {}).get("mute_during_output"):
        loop.unmute()  # restore


@on_mycroft_message("mycroft.stop", bus=bus)
@on_mycroft_message("mycroft.audio.speech.stop", bus=bus)
def handle_stop(event):
    """Handler for mycroft.stop, i.e. button press."""
    loop.force_unmute()
    tts.playback.clear()  # Clear here to get instant stop
    bus.emit_mycroft(Message("mycroft.stop.handled", {"by": "LocalAudio"}))


def connect_loop_events():
    loop.on('recognizer_loop:utterance', handle_utterance)
    loop.on('recognizer_loop:speech.recognition.unknown', handle_unknown)
    loop.on('recognizer_loop:record_begin', handle_record_begin)
    loop.on('recognizer_loop:awoken', handle_awoken)
    loop.on('recognizer_loop:wakeword', handle_wakeword)
    loop.on('recognizer_loop:record_end', handle_record_end)
    loop.on('recognizer_loop:no_internet', handle_no_internet)


def connect_hivebus_events():
    # Register handlers for events on HiveMind bus
    # bus.on('open', handle_open)
    # bus.on_close = handle_shutdown
    # bus.on("message", handle_hive_message)
    pass


def main(port=6989, host="127.0.0.1"):
    global bus
    global loop
    global config
    global audio
    global tts

    setup_locale()
    connect_hivebus_events()

    # connect audio service
    audio = AudioService(bus)

    # Register handlers on internal RecognizerLoop bus
    loop = RecognizerLoop()
    connect_loop_events()
    create_daemon(loop.run)

    # connect TTS
    tts = TTSFactory.create()
    tts.init(bus)

    wait_for_exit_signal()

    if tts:
        tts.playback.stop()
        tts.playback.join()


if __name__ == "__main__":
    main()
