import pyaudio
import vosk
import json

# Инициализация VOSK
model = vosk.Model("C:\\TRON\\model-small") 
recognizer = vosk.KaldiRecognizer(model, 16000)

def listen_command():
    # Инициализация PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Слушаю...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            query = json.loads(result)["text"].lower()
            print(f"Команда: {query}")
            return query
        else:
            partial_result = recognizer.PartialResult()
            print(json.loads(partial_result)["partial"])

