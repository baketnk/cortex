from typing import Callable
import torch
import pyaudio
import numpy as np
import wave
from pynput import keyboard
import logging
import time
from torch.cuda import is_available
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

MODEL_ID = "distil-whisper/distil-large-v3"


class CortexListener:

    def __init__(self):
        logging.debug(f"setting up {MODEL_ID}")
        self.dtype = torch.float32
        if torch.cuda.is_available():
            self.device = "cuda"
            self.dtype = torch.float16
        elif torch.backends.mps.is_available():
            self.device = "mps"
            self.dtype = torch.float16
        else:
            self.device = "cpu"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            MODEL_ID, 
            torch_dtype=self.dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained(MODEL_ID)
        self.pipeline = pipeline(
                "automatic-speech-recognition",
                model=self.model,
                tokenizer=self.processor.tokenizer,
                feature_extractor=self.processor.feature_extractor,
                max_new_tokens=128,
                torch_dtype=self.dtype,
                device=self.device,
            )
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.record_seconds = 5  # Default recording time
        self.audio = pyaudio.PyAudio()

        # handle input
        self.is_recording = False
        self.listener.start()
        self.callbacks = {
            "on_asr_complete": []
        }
        logging.info("listener setup completed")

    def set_on_asr_complete(self, callback: Callable):
        self.callbacks["on_asr_complete"].append(callback)

    def on_asr_complete(self, asr_result):
        for func in self.callbacks["on_asr_complete"]:
            func(asr_result)

    def on_press(self, key_code):



    def do_asr(self):
        """Record user audio until a stop condition, then process it with the model and return"""
        logging.debug("Starting audio recording...")
        
        # Set up the stream for recording
        stream = self.audio.open(format=self.format, channels=self.channels,
                                rate=self.rate, input=True,
                                frames_per_buffer=self.chunk)

        frames = []
        start_time = time.time()
        logging.debug("Recording... Press 'F5' to stop.")

        while self.is_recording:
            data = stream.read(self.chunk)
            frames.append(data)

            if (time.time() - start_time) > self.record_seconds:
                self.is_recording = False

        logging.debug("Finished recording.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Combine all audio frames into a single buffer
        audio_data = b''.join(frames)

        # Convert audio data to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        logging.debug("Processing audio with ASR model...")
        result = self.pipeline(audio_np)

        logging.debug(f"ASR result: {result}")
        self.on_asr_complete(result)
        return result


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    listener = CortexListener()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
