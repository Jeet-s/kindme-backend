import whisper
model = whisper.load_model("small")

def audio_to_text(audio_path):
    result = model.transcribe(audio_path)
    print(result["text"])
    return result["text"]
    