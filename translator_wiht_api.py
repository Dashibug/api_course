from tkinter import *
import requests


# Функция для перевода с помощью Microsoft Translator
def translate_microsoft(string):
    url = "https://microsoft-translator-text-api3.p.rapidapi.com/translate"
    querystring = {"to": "es", "from": "ru", "textType": "plain"}
    payload = [{"Text": string}]
    headers = {
        "x-rapidapi-key": "7251aa7cc0mshe40dd589a75de3bp10095ejsn0939f5c1eb03",
        "x-rapidapi-host": "microsoft-translator-text-api3.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()[0].get("translations", [{}])[0].get("text", "Ошибка перевода")
    else:
        return "Ошибка подключения к API"


# Функция для перевода с помощью Google Translator
def translate_google(string):
    url = "https://ai-translate.p.rapidapi.com/translate"
    payload = {
        "texts": [string],
        "tl": "av",
        "sl": "auto"
    }
    headers = {
        "x-rapidapi-key": "7251aa7cc0mshe40dd589a75de3bp10095ejsn0939f5c1eb03",
        "x-rapidapi-host": "ai-translate.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("texts", ["Ошибка перевода"])
    else:
        return "Ошибка подключения к API"


# Общая функция для перевода
def translate():
    string = text.get('1.0', END).strip()

    # В зависимости от выбора переводчика, вызываем нужную функцию
    if translator_choice.get() == "Microsoft Translator":
        translated_text = translate_microsoft(string)
    else:
        translated_text = translate_google(string)

    # Выводим результат в поле для вывода перевода
    otvet.delete('1.0', END)
    otvet.insert(END, translated_text)


# Настройка интерфейса tkinter
root = Tk()
root.title("Переводчик :)")
root.geometry('500x500')

canvas = Canvas(root, height=300, width=300)
canvas.pack()

frame = Frame(root, bg='black')
frame.place(relheight=1, relwidth=1)

title = Label(frame, text="Введи текст", bg='white', font=40)
title.place(relx=0.5, y=30, anchor=CENTER)

text = Text(root, width=35, height=5, font=20, bg='white')
text.place(relx=0.5, y=100, anchor=CENTER)

# Создаем переменную для выбора переводчика и выпадающий список
translator_choice = StringVar(root)
translator_choice.set("Microsoft Translator")

# Выпадающий список для выбора API переводчика
dropdown = OptionMenu(root, translator_choice, "Microsoft Translator", "Google Translator")
dropdown.place(relx=0.5, y=400, anchor=CENTER)

btn = Button(root, width=45, text='Перевести', command=translate)
btn.place(relx=0.5, y=200, anchor=CENTER)

otvet = Text(root, width=35, height=5, font=20, bg='white')
otvet.place(relx=0.5, y=260, anchor=CENTER)

root.mainloop()