from golos import Сказ
import random
import time
import webbrowser
import os
import frazi
import subprocess
from datetime import datetime
import tron
import sys
import subprocess
import winreg
import pygetwindow as gw
import psutil  
import pyautogui
import platform

def get_installed_programs():
    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    programs = []
    for key_path in uninstall_keys:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        except FileNotFoundError:
            continue
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)
                display_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                programs.append(display_name)
            except FileNotFoundError:
                continue
            except OSError:
                continue
    return programs
def get_correct_form(number, forms):
    """Возвращает правильную форму слова в зависимости от числа."""
    if number % 10 == 1 and number % 100 != 11:
        return forms[0]
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return forms[1]
    else:
        return forms[2]
FILE_NAME = "interface_name.txt"
def get_interface_name():
    # Сначала пытаемся получить имя из команды
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, encoding='cp866')

    if result.returncode == 0:
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "Имя" in line and ":" in line:
                interface_name = line.split(":")[1].strip()
                # Сохраняем имя в файл
                with open(FILE_NAME, "w", encoding="utf-8") as f:
                    f.write(interface_name)
                print(f"Имя интерфейса получено и сохранено: {interface_name}")
                return interface_name
    else:
        print("Ошибка при получении имени:", result.stderr)

    # Если не удалось получить имя из команды, пробуем прочитать из файла
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            interface_name = f.read().strip()
            print(f"Имя интерфейса взято из файла: {interface_name}")
            return interface_name

    print("Не удалось определить имя интерфейса")
    return None

            




def приветствие():
    text = random.choice(frazi.Приветсвие)
    print(text)
    Сказ(text)
    
def запуск_браузер():
    url = "http://t.me/TRONexCompany"
    webbrowser.open(url, new=2)
    text = random.choice(frazi.запускбраузера)
    print(text)
    Сказ(text)

def закрытие_браузера():
    command = "taskkill /IM browser.exe /f"
    os.system(command)
    text = random.choice(frazi.выключениебраузера)
    print(text)
    Сказ(text)
   

def открытие_кальк():
    os.system('calc')
    text = 'Калькулятор открыт, сэр!'
    print(text)
    Сказ(text)

def закркальк():
    os.system('TASKKILL /F /IM CalculatorApp.exe')
    text = "Калькулятор закрыт, сэр!"
    print(text)
    Сказ(text)

def выключениепк():
    text = "Спокойной ночи, сэр!"
    print(text)
    Сказ(text)

    os.system("shutdown /s /t 0")

def время():
 
 
 t = time.localtime()
 hours = t.tm_hour
 minutes = t.tm_min
 seconds = t.tm_sec

 hours_form = get_correct_form(hours, ["час", "часа", "часов"])
 minutes_form = get_correct_form(minutes, ["минута", "минуты", "минут"])
 seconds_form = get_correct_form(seconds, ["секунда", "секунды", "секунд"])

 text = str(f"{hours} {hours_form}: {minutes} {minutes_form}: {seconds} {seconds_form}")
 text = 'Время на данный момент:' + text
 print(text)
 Сказ(text)

def выкл():
 text = random.choice(frazi.прощание)
 print(text)
 Сказ(text)
 sys.exit()
 
def открытьвпн():
    installed_apps = get_installed_programs()
    vpn_apps = [app for app in installed_apps if "vpn" in app.lower()]
    print("Найденные VPN приложения:", vpn_apps)

    if vpn_apps:
        # Запускаем VPN приложение
        os.system("start " + vpn_apps[0])
        time.sleep(4)  # Ждем, чтобы окно успело открыться

        # Пытаемся найти окно по названию
        windows = gw.getWindowsWithTitle(vpn_apps[0])
        if windows:
            vpn_window = windows[0]
            vpn_window.activate()  # Активируем окно
            time.sleep(1)
        else:
            print("Окно VPN приложения не найдено.")
    else:
        print("VPN приложения не найдены.")
    text = "впн запущщен"
    Сказ(text)
    print(text)

def закрытьвпн():
    installed_apps = get_installed_programs()
    vpn_apps = [app for app in installed_apps if "vpn" in app.lower()]
    if not vpn_apps:
        print("VPN приложения не найдены.")
        return

    vpn_name = vpn_apps[0]
    print(f"Попытка закрыть VPN приложение: {vpn_name}")

    # Ищем окна с названием VPN приложения и закрываем их
    windows = gw.getWindowsWithTitle(vpn_name)
    for w in windows:
        try:
            w.close()
            print(f"Окно '{w.title}' закрыто.")
        except Exception as e:
            print(f"Не удалось закрыть окно '{w.title}': {e}")

    # Дополнительно можно попытаться закрыть процесс по имени (если известно)
    # Для этого нужно знать точное имя процесса или exe-файл VPN клиента
    # Ниже пример, если известно имя процесса (замените 'vpnclient.exe' на нужное)
    process_name = vpn_name.lower().replace(" ", "") + ".exe"  # пример преобразования
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name:
            proc.terminate()
            print(f"Процесс {proc.info['name']} завершен.")
            proc.wait(timeout=5)
    text = "впн закрыт"
    Сказ(text)
    print(text)

def выклинтернет():
    interface_name = get_interface_name()
    if interface_name:
        subprocess.run([
            "netsh", 
            "interface", 
            "set", 
            "interface", 
            f"name={interface_name}",
            "admin=DISABLED"
        ], check=True)
    text = random.choice(frazi.база)
    print(text)
    Сказ(text)  

def вклинтернет():
    interface_name = get_interface_name()
    if interface_name:
        subprocess.run([
            "netsh",
            "interface",
            "set", 
            "interface", 
            f"name={interface_name}",  
            "admin=ENABLED"
        ], check=True)
    text = "Сейчас запущу!"
    print(text)
    Сказ(text)

def раскладка():
    pyautogui.keyDown('alt')
    pyautogui.press('shift')
    pyautogui.keyUp('alt')
    text = random.choice(frazi.база)
    print(text)
    Сказ(text)  

def сон():
    text = "Спокойной ночи, сэр"
    Сказ(text)
    print(text)
    system = platform.system()
    if system == "Windows":
        # В Windows команда для перехода в спящий режим
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif system == "Linux":
        # В Linux команда systemctl suspend
        os.system("systemctl suspend")
    elif system == "Darwin":  # macOS
        os.system("pmset sleepnow")
    else:
        raise NotImplementedError(f"Sleep mode not implemented for {system}")
    
def перезагрузка():
    text = random.choice(frazi.база)
    print(text)
    Сказ(text)  
    system = platform.system()
    if system == "Windows":
        os.system("shutdown /r /t 0")
    elif system == "Linux" or system == "Darwin":
        os.system("sudo reboot")
    else:
        raise NotImplementedError(f"Reboot not implemented for {system}")
    
def отисткамусора():
    os.system("PowerShell.exe -Command Clear-RecycleBin -Force")
    text = random.choice(frazi.база)
    print(text)
    Сказ(text)   