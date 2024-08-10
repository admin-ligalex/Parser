import pandas as pd

# Чтение данных из CSV файла
data = pd.read_csv('tesla.csv')

# Генерация HTML-кода
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Listings</title>
<style>
    .container {
        width: 80%;
        margin: 20px auto;
    }
    .row {
        display: flex;
        border-bottom: 1px solid black;
    }
    .header, .cell {
        padding: 8px;
        text-align: left;
        flex: 1; /* равномерное распределение ширины */
    }
    .header {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    a {
        color: blue;
        text-decoration: none;
    }
</style>
</head>
<body>
    <h1>Car Listings</h1>
    <div class="container">
        <div class="row header">
            <div class="cell">URL</div>
            <div class="cell">Title</div>
            <div class="cell">Price</div>
            <div class="cell">Mileage</div>
            <div class="cell">Year</div>
            <div class="cell">Month</div>
            <div class="cell">Gear and Displacement</div>
            <div class="cell">Engine Info</div>
            <div class="cell">Location</div>
        </div>
    </div>
</body>
'''

# Добавление строк таблицы из данных CSV
for index, row in data.iterrows():
    html_content += f'''
        <div class="row">
            <div class="cell"><a href="{row['url']}">{row['url']}</a></div>
            <div class="cell">{row['title']}</div>
            <div class="cell">{row['price']}</div>
            <div class="cell">{row['mileage']}</div>
            <div class="cell">{row['year']}</div>
            <div class="cell">{row['month']}</div>
            <div class="cell">{row['gear_and_displacement']}</div>
            <div class="cell">{row['engine_info']}</div>
            <div class="cell">{row['location']}</div>
        </div>
    '''

# Закрытие HTML-тегов
html_content += '''
    </div>
</body>
</html>
'''

# Запись HTML в файл
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML файл успешно создан!")