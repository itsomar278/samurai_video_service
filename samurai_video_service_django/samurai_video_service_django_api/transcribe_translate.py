import whisper
import torch

# Global variable to hold the model
whisper_model = None

def check_cuda_availability():
    """Check and print CUDA availability and GPU details."""
    if torch.cuda.is_available():
        print("CUDA available")
        print("Device count:", torch.cuda.device_count())
        print("Current device:", torch.cuda.current_device())
        print("Device name:", torch.cuda.get_device_name(0))
    else:
        print("No GPU found")

def load_whisper_model():
    """Load the Whisper model once."""
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base", device="cuda")
        print("Whisper model loaded.")
    return whisper_model

def transcribe_or_translate(audio_file):
    """Transcribe audio if in English or translate it if in another language."""
    model = load_whisper_model()
    result = model.transcribe(audio_file)
    language = result.get('language')

    if language == 'en':
        return result['text'], "transcription"
    else:
        translation_result = model.transcribe(audio_file, task="translate")
        return translation_result['text'], "translation"
