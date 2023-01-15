import requests
import datetime
from selenium import webdriver

# Настройки
formob = 'З' # форма образования: "Д" - дневная, "В" - вечерняя, "3" - заочная, "У" - дистанционная, "2" - второе высшее, "М" - магистратура, "А" - аспирантура.
group = 'ФРиСО_РСО_РСОвЦС (Группа: 1)' # название группы как на сайте
kyrs = '3' # номер курса
# Пути к html файлам с расписанием для браузера (для создания фото-предпросмотра), зависят от того где лежит скрипт
week_file_path = 'file:///home/username/папка_скрипта/raspweek.html'
month_file_path = 'file:///home/username/папка_скрипта/raspmonth.html'
sem_file_path = 'file:///home/username/папка_скрипта/raspsem.html'

# webdriver Selenium
browser = webdriver.Firefox()

#Поиск значения для группы
headers = {
    'Accept': '*/*',
    'Origin': 'https://raspis.rggu.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://raspis.rggu.ru/',
}
groupvaluedata = {
    'formob': formob,
    'kyrs': kyrs,
}
idresponse = requests.post('https://raspis.rggu.ru/rasp/2.php', headers=headers, data=groupvaluedata)
idresponse = idresponse.text
idlist = idresponse.replace("<option value='", "").replace("</option>", ",\n").replace("'>", '')

with open('./grouplist.txt', 'w', encoding='utf-8') as file: 
    file.write(idlist)
with open("./grouplist.txt") as file:
    groupid = file.readlines()
    for line in groupid:
        if group in line:
            groupid = line
groupid = groupid.replace(group, '').replace(',\n', '')

print("Значение для указанной группы: ", groupid)

# Запись нужных параметров в переменные
today = datetime.date.today()
week = datetime.date.today() + datetime.timedelta(days=8)
mes = datetime.date.today() + datetime.timedelta(days=30)

datasem = {
  'formob': formob,
  'kyrs': kyrs,
  'srok': 'sem',
  'caf': groupid,
  'cafzn': group,
  'sdate_year': today.year,
  'sdate_month': today.month,
  'sdate_day': today.day,
}

datamonth = {
  'formob': formob,
  'kyrs': kyrs,
  'srok': mes,
  'caf': groupid,
  'cafzn': group,
  'sdate_year': today.year,
  'sdate_month': today.month,
  'sdate_day': today.day,
  'fdate_year': mes.year,
  'fdate_month': mes.month,
  'fdate_day': mes.day
}

dataweek = {
  'formob': formob,
  'kyrs': kyrs,
  'srok': week,
  'caf': groupid,
  'cafzn': group,
  'sdate_year': today.year,
  'sdate_month': today.month,
  'sdate_day': today.day,
  'fdate_year': week.year,
  'fdate_month': week.month,
  'fdate_day': week.day
}

# Получение расписания с сайта по заданным параметрам и добавление времени к номерам пары
rasp = requests.post('https://raspis.rggu.ru/rasp/3.php', headers=headers, data=datasem)
with open('./raspsem.html', 'w+', encoding='utf-8') as f:
    rasp = rasp.text
    replace = rasp.replace('>1</td>', '>1| 08:45</td>').replace('>2</td>', '>2| 10:15</td>').replace('>2</td>', '>2| 10:15</td>').replace('>3</td>', '>3| 12:10</td>').replace('>4</td>', '>4| 13:40</td>').replace('>5</td>', '>5| 15:35</td>').replace('>6</td>', '>6| 17:05</td>').replace('>7</td>', '>7| 18:50</td>').replace('>8</td>', '>8| 20:20</td>').replace('10px', '14px')
    f.write(replace)

rasp = requests.post('https://raspis.rggu.ru/rasp/3.php', headers=headers, data=datamonth)
with open('./raspmonth.html', 'w+', encoding='utf-8') as f:
    rasp = rasp.text
    replace = rasp.replace('>1</td>', '>1| 08:45</td>').replace('>2</td>', '>2| 10:15</td>').replace('>2</td>', '>2| 10:15</td>').replace('>3</td>', '>3| 12:10</td>').replace('>4</td>', '>4| 13:40</td>').replace('>5</td>', '>5| 15:35</td>').replace('>6</td>', '>6| 17:05</td>').replace('>7</td>', '>7| 18:50</td>').replace('>8</td>', '>8| 20:20</td>').replace('10px', '14px')
    f.write(replace)

rasp = requests.post('https://raspis.rggu.ru/rasp/3.php', headers=headers, data=dataweek)
with open('./raspweek.html', 'w+', encoding='utf-8') as f:
    rasp = rasp.text
    replace = rasp.replace('>1</td>', '>1| 08:45</td>').replace('>2</td>', '>2| 10:15</td>').replace('>2</td>', '>2| 10:15</td>').replace('>3</td>', '>3| 12:10</td>').replace('>4</td>', '>4| 13:40</td>').replace('>5</td>', '>5| 15:35</td>').replace('>6</td>', '>6| 17:05</td>').replace('>7</td>', '>7| 18:50</td>').replace('>8</td>', '>8| 20:20</td>').replace('10px', '14px')
    f.write(replace)

print("html файлы с расписанием созданы")

# Создание предпросмотров
try:
    browser.set_window_size(800, 1644)
    browser.get(sem_file_path)
    browser.save_screenshot("".join(['./pic/raspsem-', str(today), '.png' ]))
    browser.get(month_file_path)
    browser.save_screenshot("".join(['./pic/raspmonth-', str(today), '.png' ]))
    browser.get(week_file_path)
    browser.save_screenshot("".join(['./pic/raspweek-', str(today), '.png' ]))
    print("Предпросмотры созданы")
finally:
    browser.quit()
