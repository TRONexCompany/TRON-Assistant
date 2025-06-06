import os
import subprocess
import webbrowser
import pygetwindow as gw
from golos import Сказ
import random
import frazi
from listen import listen_command

from protokols.protokol import Протокол

class браузер(Протокол):
    def __init__(self):
        self.словарь_команд = {
            "браузер" : ["браузер", "поисковик", "интернет браузер", "browser", "Yandex", "Chrome", "браузере", "поисковике"],
            "запуск": ["открыть", "запустить", "включить", "активировать"],
            "закрыть": ['закрыть', "уничтожить", "прервать", "отключить", "прекратить работу", "выключить", "погасить", "гасить"],
            "поиск" : ["найти", "поиск", "поищи" ],
            "вкладка" : ["вкладка", "вклада", "вкладку", "вкладу", "новую вкладку", "новая вкладка"],
            "свернуть" : ["свернуть", "прикрыть"],
            "развернуть" : ["развернуть"]
            }
        self.словарь_действий = {
        "запускбраузера" : ["запуск", "браузер"],
        "закрытие_браузера": ["закрыть", "браузер"],
        "запусквкладки" : ["запуск", "вкладка"],
        "закрытьвкладку" : ["закрыть", "вкладка"],
        "свернутьбраузер": ["свернуть", "браузер"],
        "развернутьбраузер" : ["развернуть", "браузер"],
        "поисквбраузере" : ["поиск", "браузер"]
        
        

        }
        self.функции = {
         "запускбраузера" : self.запускбраузера,
         "закрытие_браузера" : self.закрытьбраузер,
         "свернутьбраузер" : self.свернутьбраузер,
         "развернутьбраузер" : self.развернутьбраузер,
         "поисквбраузере" : self.поисквбраузере
        }
        
    def запускбраузера(self):

     def check_process(process_name):
      tasks = subprocess.getoutput('tasklist')
      if process_name not in tasks:
        os.system("start browser.exe")
      else:
        window_title = "Браузер"
        windows = gw.getWindowsWithTitle(window_title)
        if windows: 
         window = windows[0] 
         window.minimize()
         window.maximize()
     check_process("browser.exe")
     text = random.choice(frazi.запускбраузера)
     print(text)
     Сказ(text)

    def закрытьбраузер(self):
        command = "taskkill /IM browser.exe /f"
        os.system(command)
        text = random.choice(frazi.выключениебраузера)
        print(text)
        Сказ(text)
    
    def свернутьбраузер(self):
     window_title = "Браузер"  # Убедитесь, что название указано в строках
     windows = gw.getWindowsWithTitle(window_title)
    
     if windows:  # Проверяем, есть ли окна с таким заголовком
        window = windows[0]
        window.minimize()
        text = "Выполняю"
        print(text)
        Сказ(text)
     
    def поисквбраузере(self):
     text = "Пожалуйста, скажите запрос для поиска"
     Сказ(text)
     print(text)
    

     query = listen_command() 

     url = f"https://yandex.ru/search/?text={query}"
     webbrowser.open(url)

    def развернутьбраузер(self):
     window_title = "Браузер"
     windows = gw.getWindowsWithTitle(window_title)
    
     if windows:
        window = windows[0]
        window.maximize()
        text = "Выполняю!"
        print(text)
        Сказ(text)


    def активировать_протокол(self):
     self.запускбраузера()
     text = "Протокол активирован"
     print(text)
     Сказ(text)




    




      
    



      
    
    
    
    
    
  






