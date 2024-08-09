import pandas as pd

# Чтение данных из CSV файла
data = pd.read_csv('d-max.csv')

# Генерация HTML-кода
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Listings</title>
    <style>
        table {
            width: 80%;
            border-collapse: collapse;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        a {
            color: blue;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>Car Listings</h1>
    <table>
        <tr>
            <th>URL</th>
            <th>Title</th>
            <th>Price</th>
            <th>Mileage</th>
            <th>Year</th>
            <th>Month</th>
            <th>Gear and Displacement</th>
            <th>Engine Info</th>
            <th>Location</th>
        </tr>
'''

# Добавление строк таблицы из данных CSV
for index, row in data.iterrows():
    html_content += f'''
        <tr>
            <td><a href="{row['url']}">{row['url']}</a></td>
            <td>{row['title']}</td>
            <td>{row['price']}</td>
            <td>{row['mileage']}</td>
            <td>{row['year']}</td>
            <td>{row['month']}</td>
            <td>{row['gear_and_displacement']}</td>
            <td>{row['engine_info']}</td>
            <td>{row['location']}</td>
        </tr>
    '''

# Закрытие HTML-тегов
html_content += '''
    </table>
</body>
</html>
'''

# Запись HTML в файл
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML файл успешно создан!")