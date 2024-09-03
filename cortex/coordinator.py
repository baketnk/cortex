
import logging
from pynput import keyboard

from .listen import CortexListener
from .tts import CortexTTS
from .llm import CortexLLM

class CortexCoordinator:
    def __init__(self):
        self.llm = CortexLLM()
        self.listener = CortexListener()
        self.tts = CortexTTS()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keymap = {}

    def on_press(self, key):
    	try:
            if key in self.keymap:
                logging.debug(f"command key detected {key}")
                self.keymap[key]()
        except AttributeError:
            pass


    def bind_key(self, key, func):


    def setup_defaults(self):
        self.listener.on_asr_complete
        self.bind_key(
