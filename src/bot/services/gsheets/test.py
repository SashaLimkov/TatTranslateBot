import pygsheets
import json


async def get_data():
    c = pygsheets.authorize()
    sh = c.open('Копия Сравнение переводчиков')
    wks = sh.worksheet_by_title("Лист1")
    cell_matrix = wks.get_all_values(returnas='matrix')
    final = {row[0]: {"Tatsoft": row[1], "Yandex": row[2], "Google": row[3]} for row in cell_matrix[1:] if
             len(row[1]) <= 100}
    return final


if __name__ == '__main__':
    c = pygsheets.authorize()
    sh = c.open('Копия Сравнение переводчиков')
    wks = sh.worksheet_by_title("Лист1")
    cell_matrix = wks.get_all_values(returnas='matrix')
    final = {row[0]: {"Tatsoft": row[1], "Yandex": row[2], "Google": row[3]} for row in cell_matrix[1:] if
             len(row[1]) <= 100}
    r = json.dumps(final)
    with open("r.json", "w", encoding="utf-8") as file:
        file.write(r)
