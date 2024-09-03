

import librosa
import torch
import soundfile as sf
import subprocess
import sys
import logging

class CortexTTS:
    def __init__(self):
        raise NotImplementedError()

    def load_cloned_voice(self, file_path, ref_transcript):
        logging.getLogger().setLevel(logging.DEBUG)

    def generate_wave(self, prompt, output_file="data/output.wav"):
        raise NotImplementedError() 


if __name__ == "__main__":
	tts = CortexTTS()
	tts.generate_wave("Hello mister bakedanuki. Are you ready to have fun today?")

