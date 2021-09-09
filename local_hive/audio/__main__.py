from threading import Lock

from hivemind_bus_client import HiveMessageBusClient
from hivemind_bus_client.decorators import on_mycroft_message
from local_hive.audio import SpeechLoop
from mycroft import dialog
from mycroft.audio.audioservice import AudioService
from mycroft.configuration import setup_locale
from mycroft.messagebus.message import Message
from mycroft.util import (
    create_daemon,
    wait_for_exit_signal
)
from mycroft.util.log import LOG
from ovos_plugin_manager.stt import OVOSSTTFactory
from ovos_plugin_manager.tts import OVOSTTSFactory

lock = Lock()
loop = None
tts = None
audio = None
config = {}

client_id = "HiveMindAudio"
bus = HiveMessageBusClient(client_id, port=6989, ssl=False)
bus.run_in_thread()


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



def main(port=6989, host="127.0.0.1"):
    global bus
    global loop
    global audio
    global tts

    setup_locale()

    # connect audio service
    audio = AudioService(bus)

    # Register STT on SpeechLoop event emitter
    stt = OVOSSTTFactory.create({"stt": {"module": "google"}})
    loop = SpeechLoop(stt=stt, bus=bus)
    create_daemon(loop.run)

    # connect TTS
    tts = OVOSTTSFactory.create({"tts": {"module": "google"}})
    tts.init(bus)

    wait_for_exit_signal()

    if loop:
        loop.stop()

    if tts:
        tts.playback.stop()
        tts.playback.join()


if __name__ == "__main__":
    main()
