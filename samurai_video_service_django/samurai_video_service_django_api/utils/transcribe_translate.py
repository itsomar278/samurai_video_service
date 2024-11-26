import os
from faster_whisper import WhisperModel, BatchedInferencePipeline

# Load Whisper model once
whisper_model = None
batched_model = None


def load_whisper_model():
    """Load the Whisper model once."""
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    global whisper_model, batched_model
    if whisper_model is None:
        whisper_model = WhisperModel("base", device="cuda", compute_type="float16")  # Load faster-whisper model with float16 for better performance
        batched_model = BatchedInferencePipeline(model=whisper_model)  # Initialize BatchedInferencePipeline
        print("Faster Whisper model loaded.")
    return batched_model

def process_audio(audio_file):
    """Process the entire audio file using batched transcription."""
    if os.path.getsize(audio_file) == 0:
        return f"Error: Empty audio file {audio_file}"

    try:
        # Use batched model to transcribe the entire audio file
        batched_model = load_whisper_model()  # Load the model
        segments, info = batched_model.transcribe(audio_file, batch_size=16)

        # Collect the transcribed text from the segments
        transcribed_text = " ".join([segment.text for segment in segments])

        print(f"Processed audio file {audio_file} with result: {transcribed_text}")
        return transcribed_text
    except Exception as e:
        return f"Error processing audio file {audio_file}: {str(e)}"

def transcribe_or_translate(audio_file):
    """Transcribe or translate the entire audio file."""
    transcription = process_audio(audio_file)
    return transcription, "translation"
