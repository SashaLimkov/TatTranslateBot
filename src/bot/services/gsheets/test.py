import pygsheets


async def get_data():
    c = pygsheets.authorize(service_account_file="ttrans-354808-b525bb0e46e2.json")
    sh = c.open("tattrans")
    wks = sh.worksheet_by_title("Лист1")
    cell_matrix = wks.get_all_values(returnas="matrix")
    work_space = cell_matrix[1:]
    final = {}
    for row in work_space:
        if len(row[0]) <= 100 and len(row[0].strip().split(" ")) > 1:
            if row[1].strip() == row[2].strip() == row[3].strip():
                continue
            final.update(
                {
                    row[0].strip(): {
                        "Tatsoft": row[1].strip(),
                        "Yandex": row[2].strip(),
                        "Google": row[3].strip(),
                    }
                }
            )
    return final


# if __name__ == '__main__':
#     c = pygsheets.authorize(service_account_file="ttrans-354808-b525bb0e46e2.json")
#     sh = c.open('tattrans')
#     wks = sh.worksheet_by_title("Лист1")
#     cell_matrix = wks.get_all_values(returnas='matrix')
#
#
#     r = json.dumps(final)
#     with open("res.json", "w", encoding="utf-8") as file:
#         file.write(r)
