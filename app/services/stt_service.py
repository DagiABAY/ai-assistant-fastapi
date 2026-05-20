from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

class STTService:

    def transcribe(self, audio_path):

        segments, info = model.transcribe(
            audio_path
        )

        text = " ".join(
            segment.text for segment in segments
        )

        return {
            "text": text,
            "language": info.language
        }