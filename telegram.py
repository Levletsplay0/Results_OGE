import requests
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("token", parse_mode=None)

def get_results(Lastname, Name, SecondName, DocNumber):
    
    data = {"Lastname": Lastname, "Name": Name, "SecondName": SecondName, "DocNumber": DocNumber}

    res = requests.post("http://nscm.ru/giaresult/tablresult.php", data=data).content


    soup = BeautifulSoup(res, 'html.parser')
    name = soup.h2.get_text(strip=True)

    table = soup.find('table', class_='tab_result')
    rows = table.find_all('tr')[1:]

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


    
    return results



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Введите данные в формате: Фамилия имя отчество номерпаспорта")
    

@bot.message_handler(func=lambda m: True)
def echo_all(message):

    parts = message.text.split()

    if len(parts) != 4:
        bot.send_message(message.chat.id, "Ошибка, введите данные в формате: Фамилия имя отчество номерпаспорта")
    else:
        last_name = parts[0]
        first_name = parts[1]
        middle_name = parts[2]
        passport_number = parts[3]

        bot.send_message(message.chat.id, "Отлично! Получаем данные...")
        results = get_results(last_name, first_name, middle_name, passport_number)

        bot.send_message(message.chat.id, f"Результаты ученика: {first_name}")
        for result in results:
            bot.send_message(message.chat.id, f"{result['Предмет']}: {result['Балл']} баллов, оценка: {result['Оценка']}, дата экзамена: {result['Дата']}")
            


bot.infinity_polling()
