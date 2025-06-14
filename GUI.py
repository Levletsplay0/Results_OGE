import tkinter
from tkinter import ttk
from threading import Thread
import requests
from bs4 import BeautifulSoup
from tkinter.messagebox import showinfo, showerror
import json
import os

# Файл для сохранения данных
DATA_FILE = "user_data.json"

def save_data(lastname, name, patronymic, doc_number):
    """Сохраняет данные в JSON файл"""
    data = {
        "lastname": lastname,
        "name": name,
        "patronymic": patronymic,
        "doc_number": doc_number
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_data():
    """Загружает данные из JSON файла"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def insert_saved_data():
    """Вставляет сохраненные данные в поля ввода"""
    data = load_data()
    if data:
        entry_surname.delete(0, tkinter.END)
        entry_surname.insert(0, data.get("lastname", ""))
        
        entry_name.delete(0, tkinter.END)
        entry_name.insert(0, data.get("name", ""))
        
        entry_patronymic.delete(0, tkinter.END)
        entry_patronymic.insert(0, data.get("patronymic", ""))
        
        entry_document.delete(0, tkinter.END)
        entry_document.insert(0, data.get("doc_number", ""))

def get_results(Lastname, Name, SecondName, DocNumber):
    btn_accept.config(state="disabled")
    try:
        # Сохраняем данные перед запросом
        save_data(Lastname, Name, SecondName, DocNumber)

        label_progress.config(text="Обращение к серверу NSCM...\nВремя ожидания зависит от нагруженности сервера")

        data = {"Lastname": Lastname, "Name": Name, "SecondName": SecondName, "DocNumber": DocNumber}
        res = requests.post("http://nscm.ru/giaresult/tablresult.php", data=data).content

        # Создаём объект BeautifulSoup
        soup = BeautifulSoup(res, 'html.parser')
        name = soup.h2.get_text(strip=True)
        

        # Извлекаем данные таблицы
        table = soup.find('table', class_='tab_result')
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок

        results = []
        for row in rows:
            cols = row.find_all('td')
            subject = cols[0].get_text(strip=True)
            date = cols[1].get_text(strip=True)
            score = cols[2].get_text(strip=True)
            grade = cols[3].get_text(strip=True)
            
            results.append({
                'Предмет': subject,
                'Дата': date,
                'Балл': score,
                'Оценка': grade
            })


        a = f"Ученик: {name} "
        for result in results:
            a += f"───────────────────────────────────────────────────\n{result['Предмет']}: {result['Балл']} баллов, оценка: {result['Оценка']}, дата экзамена: {result['Дата']}\n"
        label_progress.config(text="")
        showinfo("Результаты", a)
    except Exception as e:
        label_progress.config(text="")
        showerror("Ошибка", "Для этого человека не найдены результаты.\nПроверьте введённые данные")
    
    btn_accept.config(state="normal")

root = tkinter.Tk()


screen_width = root.winfo_screenwidth()  
screen_height = root.winfo_screenheight()  
# Вычисляем координаты окна  
window_width = 500  
window_height = 500  
x = (screen_width // 2) - (window_width // 2)  
y = (screen_height // 2) - (window_height // 2)  


root.geometry(f"{window_width}x{window_height}+{x}+{y}") 
root.title("Оценки ОГЭ")
root.resizable(width=False, height=False)

ttk.Label(text="Оценки ОГЭ", font="Bahnschrift 25 bold").place(x=250, y=40, anchor="center")
ttk.Separator(root, orient="horizontal").place(width=270, x=250, y=70, anchor="center")
# Поля ввода
ttk.Label(text="Фамилия", font="Bahnschrift 15 bold").place(x=250, y=90, anchor="center")
entry_surname = ttk.Entry(font="Bahnschrift 15")
entry_surname.place(x=250, y=120, anchor="center", width=250, height=30)

ttk.Label(text="Имя", font="Bahnschrift 15 bold").place(x=250, y=150, anchor="center")
entry_name = ttk.Entry(font="Bahnschrift 15")
entry_name.place(x=250, y=180, anchor="center", width=250)

ttk.Label(text="Отчество", font="Bahnschrift 15 bold").place(x=250, y=210, anchor="center")
entry_patronymic = ttk.Entry(font="Bahnschrift 15")
entry_patronymic.place(x=250, y=240, anchor="center", width=250)

ttk.Label(text="Номер паспорта", font="Bahnschrift 15 bold").place(x=250, y=270, anchor="center")
entry_document = ttk.Entry(font="Bahnschrift 15")
entry_document.place(x=250, y=300, anchor="center", width=250)

# Кнопка для вставки сохраненных данных
btn_load = ttk.Button(
    text="Вставить недавно использованные данные", 
    command=insert_saved_data
)
btn_load.place(x=250, y=350, anchor="center", width=250, height=30)

# Основная кнопка
btn_accept = ttk.Button(
    text="Получить результаты", 
    command=lambda: Thread(
        target=get_results, 
        args=(
            entry_surname.get(), 
            entry_name.get(), 
            entry_patronymic.get(), 
            entry_document.get()
        )
    ).start()
)
btn_accept.place(x=250, y=410, anchor="center", width=250, height=50)
label_progress = ttk.Label(text="")
label_progress.place(x=250, y=450, anchor="center")


root.mainloop()