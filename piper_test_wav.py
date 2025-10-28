import os
import wave
from time import sleep

from piper import PiperVoice, SynthesisConfig

model = "piper-voices/en/ljspeech/medium/en_US-ljspeech-medium.onnx"

voice = PiperVoice.load(model)

if os.path.exists("test.wav"):
    os.remove("test.wav")

sleep(0.1)

with wave.open("test.wav", "wb") as wav_file:
    syn_config = SynthesisConfig(
        volume=1.0,  # half as loud
        length_scale=1.0,  # twice as slow
        noise_scale=1.0,  # more audio variation
        noise_w_scale=1.0,  # more speaking variation
        normalize_audio=False, # use raw audio from voice
    )

    voice.synthesize_wav("Welcome to the world of speech synthesis!", wav_file, syn_config=syn_config)
