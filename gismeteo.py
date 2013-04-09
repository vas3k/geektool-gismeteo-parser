#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Gismeteo geeklet - simple script for load and display weather information
    in Russian cities on GeekTool (http://projects.tynsoe.org/en/geektool/).

    Author: vas3k
    Web: http://vas3k.ru/dev/geektool_gismeteo/
    Date: 2012-09-10
    License: MIT
    Requirements: Python (installed with xcode), sometimes lxml (if an error occurs)

    Установка:

    0) Распакуйте скрипт в папку, в которой через месяц вы не забудете, что это за херня и не
       удалите его случайно.

    1) Создайте "Shell", в поле "Command" впишите: 
          "<путь до папки>/gismeteo.py && cat <путь до папки>/weather.txt"
       Это отобразит температуру и текстовую информацию о погоде. Поставьте интервал обновления,
       например, в 600 секунд.

    2) Создайте "Image" и пропишите путь до картинки: "<путь до папки>/weather.jpg". Это будет 
       иконка погоды. Поставьте интервал обновление тоже 600 секунд.

    3) Создайте "Shell" и пропишите в "Command": "cat <путь до папки>/forecast.txt".
       Про интервал обновления напоминать всё еще надо?

    4) Настройка шрифтов и расположения - на ваше усмотрение. Я использую Helvetica Neue Light 
       или Ultra Light. Дополнительные типа "Погода в моей деревне:" делаем сами, не маленькие уже.
"""

import urllib, urllib2, re, os, codecs, sys
from bs4 import BeautifulSoup

city_id = 4690      # id вашего города на gismeteo.ru, по-умолчанию - Новосибирск
get_weekly = True   # загружать ли прогноз на 2 недели
days_limit = 9      # сколько дней прогноза сохранять в файл

# Получение текущей погоды

page = urllib2.urlopen("http://www.gismeteo.ru/city/weekly/%s/" % city_id).read()
soup = BeautifulSoup(page)

temp_elem = soup.select("dd.value.m_temp.c")
cloudness_elem = soup.select("dl.cloudness dt")

if temp_elem:
    temp = temp_elem[0].contents[0]

if cloudness_elem:
    cloudness = cloudness_elem[0]["title"]
    icon = cloudness_elem[0]["style"][22:-1]
    if icon:
        urllib.urlretrieve(icon, os.path.join(os.path.dirname(__file__), "weather.jpg"))

with codecs.open(os.path.join(os.path.dirname(__file__), "weather.txt"), "w", "utf-8") as weather_file:
    if temp:
        weather_file.write(u"%s˚ C\n%s" % (temp, cloudness))
    else:
        weather_file.write(u"Какие-то проблемы :(")

# Получение прогноза на ближайшие дни

if not get_weekly: 
    sys.exit(0)

days = soup.select("#weather-weekly div.rframe.wblock.wdata div.wbshort table")

with codecs.open(os.path.join(os.path.dirname(__file__), "forecast.txt"), "w", "utf-8") as forecast_file:
    for day in days[:days_limit]:
        day_date = day.select("td.workday .s_date") or day.select("td.weekend .s_date")
        day_temp = [d.string for d in day.select("td.temp span.value.m_temp.c")]
        if day_temp:
            forecast_file.write(u"%s: %4s/%s\n" % (day_date[0].contents[0].rjust(5), day_temp[0], day_temp[1]))
