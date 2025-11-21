import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import subprocess

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_animated_feature_films_of_2025'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(" Начинаем сбор данных с Wikipedia...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f" Ошибка при загрузке страницы: {e}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        if not tables:
            print(" Таблицы не найдены!")
            return

        table = tables[0]

        # Инициализируем списки данных
        names = []
        countries = []
        directors = []
        release_dates = []

        print("\n Анализируем структуру таблицы...")
        first_data_row = table.find_all('tr')[1]
        columns = first_data_row.find_all(['td', 'th'])
        print(f" Всего столбцов в строке: {len(columns)}")      
        print("\n Начинаем обработку фильмов...")

        for row_num, row in enumerate(table.find_all('tr')[1:], 1):
            columns = row.find_all(['td', 'th'])
            
            if len(columns) < 7:
                continue
                
            try:
                # Название фильма (1-й столбец)
                name_link = columns[0].find('a')
                name = name_link.text.strip() if name_link else columns[0].text.strip()
                
                # Страна (2-й столбец)
                country = columns[1].text.strip()
                
                # Директор (3-й столбец)
                director = columns[2].text.strip()
                
                # Дата выхода (7-й столбец - индекс 6)
                release_date = columns[6].text.strip()

                # Добавление данных в списки
                names.append(name)
                countries.append(country)
                directors.append(director)
                release_dates.append(release_date)
                
                       
            except Exception as e:
                print(f"️ Ошибка при обработке строки {row_num}: {e}")
                continue

        # Создаем DataFrame
        df = pd.DataFrame({
            'Название фильма': names,
            'Страна': countries,
            'Режиссер': directors,
            'Дата выхода': release_dates
        })

        # Показываем предпросмотр данных
        print("\n ПРЕДПРОСМОТР ДАННЫХ:")
        print("=" * 50)
        print(df.head(10))  # Первые 10 строк
        print("=" * 50)
        
        # Сохранение данных в Excel
        filename = 'анимационные_фильмы_2025.xlsx'
        df.to_excel('outputs/filename', index=False, engine='openpyxl')
        
        # Полный путь к файлу
        file_path = os.path.abspath(filename)
        
        print(f"\n Данные успешно сохранены!")
        print(f" Файл: {file_path}")
        print(f"️ Всего обработано фильмов: {len(df)}")
        
        # Автоматическое открытие файла
        print("\n Открываю файл в Excel...")
        try:
            if os.name == 'nt':  # Windows
                os.startfile(filename)
            elif os.name == 'posix':  # Mac/Linux
                try:
                    subprocess.call(['open', filename])  # Mac
                except:
                    subprocess.call(['xdg-open', filename])  # Linux
            print(" Файл открыт в Excel!")
        except Exception as e:
            print(f"️ Не удалось открыть файл автоматически: {e}")
            print(f" Файл находится здесь: {file_path}")
            
    else:
        print(f" Ошибка при запросе: {response.status_code}")

if __name__ == "__main__":
    main()

