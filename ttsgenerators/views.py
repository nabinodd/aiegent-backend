import os
import subprocess
import tempfile
import uuid
import wave

from django.conf import settings
from piper import PiperVoice, SynthesisConfig
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


PIPER_MODEL_PATH = "piper-voices/en/ljspeech/medium/en_US-ljspeech-medium.onnx"

OUTPUT_SUBDIR = "tts"

SYNTHESIS_CFG = SynthesisConfig(
    volume=1.0,
    length_scale=0.95,
    noise_scale=0.667,
    noise_w_scale=0.8,
    normalize_audio=False,
)


VOICE = PiperVoice.load(PIPER_MODEL_PATH)

def _ensure_out_dir():
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        raise RuntimeError("MEDIA_ROOT is not configured.")
    out_dir = os.path.join(media_root, OUTPUT_SUBDIR)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def _ffmpeg_ok():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def _synthesize_wav(text, wav_path) -> None:
    with wave.open(wav_path, "wb") as wav_file:
        VOICE.synthesize_wav(text, wav_file, syn_config=SYNTHESIS_CFG)

def _to_ogg_opus_mono(in_wav, out_ogg):
    if not _ffmpeg_ok():
        raise RuntimeError("ffmpeg not found. Install ffmpeg to produce ogg/opus.")
    cmd = [
        "ffmpeg", "-y", "-i", in_wav,
        "-ar", "16000",         # resample for speech; stable on WA
        "-ac", "1",             # mono
        "-af", "loudnorm=I=-18:TP=-2:LRA=7",  # clean, broadcast-ish loudness
        "-c:a", "libopus",
        "-b:a", "32k",          # speech transparent at 24–32k
        "-vbr", "on",
        "-application", "voip", # Opus tuning for speech
        "-frame_duration", "60",# fewer artifacts; longer frames ok for voice
        "-compression_level", "10",
        out_ogg
    ]
    subprocess.run(cmd, check=True)
    try: os.remove(in_wav)
    except OSError: pass


class TextToSpeechAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "Field 'text' is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            out_dir = _ensure_out_dir()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        uid = uuid.uuid4().hex
        out_filename = f"{uid}.ogg"
        out_path = os.path.join(out_dir, out_filename)

        tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_wav_path = tmp_wav.name
        tmp_wav.close()

        try:
            _synthesize_wav(text, tmp_wav_path)
            _to_ogg_opus_mono(tmp_wav_path, out_path)
        except Exception as e:
            try:
                os.remove(tmp_wav_path)
            except OSError:
                pass
            return Response({"detail": f"TTS/convert failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        media_url = getattr(settings, "MEDIA_URL", "/media/")
        if not media_url.endswith("/"):
            media_url += "/"
        rel_url = f"{media_url}{OUTPUT_SUBDIR}/{out_filename}"
        audio_url = request.build_absolute_uri(rel_url)

        return Response(
            {"audio_url": audio_url, "mime": "audio/ogg", "id": uid},
            status=status.HTTP_201_CREATED,
        )
