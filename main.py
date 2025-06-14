import requests
from bs4 import BeautifulSoup

Lastname = input("Введите фамилию: ")
Name = input("Введите Имя: ")
SecondName = input("Введите отчество: ")
DocNumber = input("Введите номер паспорта: ")

data = {"Lastname": Lastname, "Name": Name, "SecondName": SecondName, "DocNumber": DocNumber}

res = requests.post("http://nscm.ru/giaresult/tablresult.php", data=data).content


# Создаём объект BeautifulSoup
soup = BeautifulSoup(res, 'html.parser')
name = soup.h2.get_text(strip=True)
print(f"ФИО: {name}")

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


print("\nРезультаты:")
for result in results:
    print(f"{result['Предмет']}: {result['Балл']} баллов, оценка: {result['Оценка']}, дата экзамена: {result['Дата']}")