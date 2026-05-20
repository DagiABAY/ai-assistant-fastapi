import subprocess
import uuid

class TTSService:

    def speak(self, text, language="en"):

        output_file = f"audio/{uuid.uuid4()}.wav"

        model = "models/piper/en_US-lessac-medium.onnx"

        command = (
            f'echo "{text}" | '
            f'piper --model {model} '
            f'--output_file {output_file}'
        )

        subprocess.run(command, shell=True)

        return output_file