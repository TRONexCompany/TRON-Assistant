import pyttsx3
engine = pyttsx3.init()

engine.setProperty('rate', 160)  # Скорость речи
engine.setProperty('volume', 0.37)  # Громкость
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)  # Выбор голоса


def Сказ(text):
 engine.say(text)
 engine.runAndWait()





