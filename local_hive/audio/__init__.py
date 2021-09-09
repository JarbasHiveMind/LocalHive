from mycroft.client.speech.listener import RecognizerLoop
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG
from ovos_plugin_manager.wakewords import OVOSWakeWordFactory

client_id = "HiveMindSTT"


class SpeechLoop(RecognizerLoop):
    bus = None

    def __init__(self, bus=None, *args, **kwargs):
        if bus:
            self.init_bus(bus)
        super(SpeechLoop, self).__init__(*args, **kwargs)
        self.responsive_recognizer.instant_listen = True

    @classmethod
    def init_bus(cls, bus):
        cls.bus = bus
        cls.connect_hivebus_events()

    @classmethod
    def connect_hivebus_events(cls):
        # Register handlers for events on HiveMind bus
        # bus.on('open', handle_open)
        # bus.on_close = handle_shutdown
        # bus.on("message", handle_hive_message)
        pass

    def create_wake_word_recognizer(self):
        """Create a local recognizer to hear the wakeup word

        For example 'Hey Mycroft'.

        The method uses the hotword entry for the selected wakeword, if
        one is missing it will fall back to the old phoneme and threshold in
        the listener entry in the config.

        If the hotword entry doesn't include phoneme and threshold values these
        will be patched in using the defaults from the config listnere entry.
        """
        LOG.info('Creating wake word engine')
        word = self.config.get('wake_word', 'hey mycroft')
        config = {'hotwords': {
            "hey mycroft": {
                "module": "pocketsphinx",
                "phonemes": "HH EY . M AY K R AO F T",
                "threshold": 1e-90,
                "lang": "en-us"
            }
        }}
        LOG.info('Using hotword entry for {}'.format(word))

        return OVOSWakeWordFactory.create_hotword(word, config, self.lang,
                                                  loop=self)

    def create_wakeup_recognizer(self):
        LOG.info("creating stand up word engine")
        word = self.config.get("stand_up_word", "wake up")
        config = {'hotwords': {
            "wake up": {
                "module": "pocketsphinx",
                "phonemes": "W EY K . AH P",
                "threshold": 1e-20,
                "lang": "en-us"
            }
        }}
        return OVOSWakeWordFactory.create_hotword(word,
                                                  config=config,
                                                  lang=self.lang,
                                                  loop=self)

    def connect_loop_events(self):
        self.on('recognizer_loop:utterance', self.handle_utterance)
        self.on('recognizer_loop:speech.recognition.unknown',
                self.handle_unknown)
        self.on('recognizer_loop:record_begin', self.handle_record_begin)
        self.on('recognizer_loop:awoken', self.handle_awoken)
        self.on('recognizer_loop:wakeword', self.handle_wakeword)
        self.on('recognizer_loop:record_end', self.handle_record_end)

    def run(self):
        self.connect_loop_events()
        super().run()

    @classmethod
    def handle_record_begin(cls):
        """Forward internal bus message to external bus."""
        LOG.info("Begin Recording...")
        context = {'client_name': client_id,
                   'source': client_id,
                   'destination': ["JarbasHiveMind"]}
        cls.bus.emit_mycroft(
            Message('recognizer_loop:record_begin', context=context))

    @classmethod
    def handle_record_end(cls):
        """Forward internal bus message to external bus."""
        LOG.info("End Recording...")
        context = {'client_name': client_id,
                   'source': client_id,
                   'destination': ["JarbasHiveMind"]}
        cls.bus.emit_mycroft(
            Message('recognizer_loop:record_end', context=context))

    @classmethod
    def handle_awoken(cls):
        """Forward mycroft.awoken to the messagebus."""
        LOG.info("Listener is now Awake: ")
        context = {'client_name': client_id,
                   'source': client_id,
                   'destination': ["JarbasHiveMind"]}
        cls.bus.emit_mycroft(Message('mycroft.awoken', context=context))

    @classmethod
    def handle_wakeword(cls, event):
        LOG.info("Wakeword Detected: " + event['utterance'])
        cls.bus.emit_mycroft(Message('recognizer_loop:wakeword', event))

    @classmethod
    def handle_utterance(cls, event):
        LOG.info("Utterance: " + str(event['utterances']))
        context = {'client_name': client_id,
                   'source': client_id,
                   'destination': ["JarbasHiveMind"]}
        if 'ident' in event:
            ident = event.pop('ident')
            context['ident'] = ident
        cls.bus.emit_mycroft(
            Message('recognizer_loop:utterance', event, context))

    @classmethod
    def handle_unknown(cls):
        context = {'client_name': client_id,
                   'source': client_id,
                   'destination': ["JarbasHiveMind"]}
        cls.bus.emit_mycroft(
            Message('mycroft.speech.recognition.unknown', context=context))
