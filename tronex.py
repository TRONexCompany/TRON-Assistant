import sys
import tkinter as tk
from tkinter import scrolledtext
import threading
import tron  # ваш модуль tron.py
import listen  # ваш модуль listen.py

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', text)
        self.text_widget.see('end')
        self.text_widget.config(state='disabled')

    def flush(self):
        pass  # Для совместимости с sys.stdout

class TronApp:
    def __init__(self, root):
        self.root = root
        root.title("TRON")
        root.iconbitmap('C:\\TRON\\yarlik\\аватрона.ico')

        # Фон всего окна
        root.configure(background='black')

        # Текстовое поле для чата (чёрный фон, белый текст)
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20,
                                                   state='disabled', font=("Consolas", 12),
                                                   background='black', foreground='white')
        self.chat_area.pack(padx=10, pady=10)

        # Перенаправляем stdout в self.chat_area
        sys.stdout = StdoutRedirector(self.chat_area)

        # Поле ввода текста (чёрный фон, белый текст, белый курсор)
        self.input_entry = tk.Entry(root, width=80, font=("Consolas", 12),
                                    background='black', foreground='white', insertbackground='white')
        self.input_entry.pack(padx=10, pady=(0,10))
        self.input_entry.bind('<Return>', self.on_send_text)

        # Кнопка отправки текстовой команды (чёрный фон, белый текст)
        self.send_button = tk.Button(root, text="Отправить", command=self.on_send_text,
                                     bg='black', fg='white')
        self.send_button.pack(pady=(0,10))

        # Кнопка включения/выключения микрофона (чёрный фон, белый текст)
        self.mic_button = tk.Button(root, text="Включить микрофон", command=self.toggle_microphone,
                                    bg='black', fg='white')
        self.mic_button.pack(pady=(0,10))

        # Кнопка выхода (чёрный фон, белый текст)
        self.exit_button = tk.Button(root, text="Выключить помощника", command=self.on_exit,
                                     bg='black', fg='white')
        self.exit_button.pack(pady=(0,10))

        # Переменные для управления микрофоном
        self.listening = False
        self.listen_thread = None
        self.stop_listening_event = threading.Event()

    def append_chat(self, text):
        """Добавить текст в чат с прокруткой вниз."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, text + '\n')
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def on_send_text(self, event=None):
        """Обработка отправки текстовой команды."""
        query = self.input_entry.get().strip()
        if not query:
            return
        self.append_chat(f"> {query}")  # показать ввод пользователя
        self.input_entry.delete(0, tk.END)

        # Выполнить команду из tron.execute_command в отдельном потоке
        threading.Thread(target=self.process_command, args=(query,), daemon=True).start()

    def process_command(self, query):
        """Выполнить команду и вывести результат (если нужно)."""
        response = tron.execute_command(query)
        if response:
            self.append_chat(response)

    def toggle_microphone(self):
        """Включить или выключить микрофон."""
        if not self.listening:
            self.listening = True
            self.mic_button.config(text="Выключить микрофон")
            self.stop_listening_event.clear()
            self.listen_thread = threading.Thread(target=self.listen_microphone, daemon=True)


            self.listen_thread.start()
            self.append_chat("[Микрофон включён]")
        else:
            self.listening = False
            self.mic_button.config(text="Включить микрофон")
            self.stop_listening_event.set()
            self.append_chat("[Микрофон выключен]")

    def listen_microphone(self):
        """Поток прослушивания микрофона с возможностью остановки."""
        import pyaudio
        import vosk
        import json

        model = vosk.Model("C:\\TRON\\model-small") 
        recognizer = vosk.KaldiRecognizer(model, 16000)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        while not self.stop_listening_event.is_set():
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                query = json.loads(result)["text"].lower()
                if query:
                    self.append_chat(f"> {query}")
                    tron.execute_command(query)
            else:
                # Можно показывать частичные результаты, если нужно
                pass

        stream.stop_stream()
        stream.close()
        p.terminate()

    def on_exit(self):
        """Выход из приложения."""
        if self.listening:
            self.stop_listening_event.set()
        self.root.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = TronApp(root)
    root.mainloop()