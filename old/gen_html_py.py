import pandas as pd

# Чтение данных из CSV файла
data = pd.read_csv('CSV/cars_data1.csv')

# Начало HTML-кода
html_content = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация об автомобилях</title>
    <style>
        .car-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px;
        }
        .car-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            width: 300px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .car-card img {
            width: 100%;
            border-radius: 5px;
        }
        .car-title {
            font-weight: bold;
            margin-top: 10px;
        }
        .car-info {
            margin-top: 5px;
        }
    </style>
</head>
<body>

<h1>Информация об автомобилях</h1>

<div class="car-container">
'''

# Генерация карточек для каждого автомобиля
for index, row in data.iterrows():
    html_content += f'''
    <div class="car-card">
        <a href="{row['url']}">
            <img src="{row['image_url']}" alt="{row['title']}">
            <div class="car-title">{row['title']}</div>
        </a>
            <div class="car-info">Цена: {row['price']}</div>
            <div class="car-info">Пробег: {row['mileage']}</div>
            <div class="car-info">Год: {row['year']}</div>
            <div class="car-info">Месяц: {row['month']}</div>
            <div class="car-info">КПП и объем: {row['gear_and_displacement']}</div>
            <div class="car-info">Двигатель: {row['engine_info']}</div>
            <div class="car-info">Местоположение: {row['location']}</div>
        
    </div>
    '''

# Завершение HTML-кода
html_content += '''
</div>

</body>
</html>
'''

# Запись в HTML-файл
with open('html/cars.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML файл успешно создан!")