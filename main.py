from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

url = "https://www.kinopoisk.ru/premiere/"
driver.get(url)

time.sleep(5)

movies = driver.find_elements(By.CSS_SELECTOR, "div.textBlock")[:10]

film_data = []

for movie in movies:
    try:
        # Название фильма
        title = movie.find_element(By.CSS_SELECTOR, "span.name_big a").text

    
        info_block = movie.find_element(By.CSS_SELECTOR, "span[style='margin: 0']")
        info_text = info_block.text.strip()

        # Страна 
        country = info_text.split(",")[0].strip()

        # Режиссёр 
        director = info_block.find_element(By.CSS_SELECTOR, "i a").text

        # Дата выхода 
        try:
            prem_day = movie.find_element(By.XPATH, "./ancestor::div[@class='text']/following-sibling::div[@class='prem_day']")

            day_img = prem_day.find_element(By.CSS_SELECTOR, "div.day img").get_attribute("src")
            month_img = prem_day.find_element(By.CSS_SELECTOR, "img[src*='month']").get_attribute("src")

            
            day = day_img.split("/")[-1].split("g")[0]  # '3g.gif' → '3'
            month = month_img.split("/")[-1].split("_")[1].split("g")[0]  # 'month_04g.gif' → '04'

            # Словарь для перевода номера месяца в текст
            months_dict = {
                "01": "января", "02": "февраля", "03": "марта", "04": "апреля",
                "05": "мая", "06": "июня", "07": "июля", "08": "августа",
                "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"
            }

            release_date = f"{day} {months_dict.get(month, month)}"
        except:
            release_date = "Неизвестно"

        # Добавляем в список
        film_data.append([title, director, country, release_date])

    except Exception as e:
        print(f"Ошибка при обработке фильма: {e}")


driver.quit()

# Записываем в CSV
df = pd.DataFrame(film_data, columns=["Название", "Режиссёр", "Страна", "Дата выхода"])
df.to_csv("kinopoisk_premieres.csv", index=False, encoding="utf-8-sig")

print("✅ Данные успешно сохранены в 'kinopoisk_premieres.csv'")