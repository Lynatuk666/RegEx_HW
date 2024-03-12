import csv
import re
from pprint import pprint


with open ("phonebook_raw.csv", encoding="UTF-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

title = contacts_list[0]
new_row_contacts_list = {}
for inf in contacts_list[1:]:
    full_name = " ".join(inf[:3]).split()#убираю лишние пробелы и привожу к дному виду все
    name_surname = " ".join(full_name[:2])
    pattern = r"(\+7|8)[\s-]?\(?(\d{3})*\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s?\(*([а-я0-9\s\.]{9})?\)?"
    repl = r"+7(\2)\3-\4-\5 \6"
    number = re.sub(pattern, repl, inf[5])# меняю формат  написания номера телефона на необходимый
    if len(full_name) > 2: #в одном из имен не было отчества, отчего весь код падал с ошибкой.
        new_inf = [*full_name, inf[3], inf[4], number, inf[6]] #пришлось прописать для него отдельный кусочек
    else:
        new_inf = [*full_name, "", inf[3], inf[4], number, inf[6]]
    new_inf = dict(zip(title, new_inf)) #собираем словарь с нужными нам знначениями
    if name_surname not in new_row_contacts_list:
        new_row_contacts_list.update({" ".join(full_name[:2]): new_inf})
    else:
        if new_row_contacts_list[name_surname]["lastname"] == "":
            new_row_contacts_list[name_surname].update({
                "lastname": f"{new_row_contacts_list[name_surname]['lastname'] + new_inf['lastname']}"})
        if new_row_contacts_list[name_surname]["firstname"] == "":
            new_row_contacts_list[name_surname].update({
                "firstname": f"{new_row_contacts_list[name_surname]['firstname'] + new_inf['firstname']}"})
        if new_row_contacts_list[name_surname]["surname"] == "":
            new_row_contacts_list[name_surname].update({
                "surname": f"{new_row_contacts_list[name_surname]['surname'] + new_inf['surname']}"})
        if new_row_contacts_list[name_surname]["organization"] == "":
            new_row_contacts_list[name_surname].update({
                "organization": f"{new_row_contacts_list[name_surname]['organization'] + new_inf['organization']}"})
        if new_row_contacts_list[name_surname]["position"] == "":
            new_row_contacts_list[name_surname].update({
                "position": f"{new_row_contacts_list[name_surname]['position'] + new_inf['position']}"})
        if new_row_contacts_list[name_surname]["phone"] == "":
            new_row_contacts_list[name_surname].update({
                "phone": f"{new_row_contacts_list[name_surname]['phone'] + new_inf['phone']}"})
        if new_row_contacts_list[name_surname]["email"] == "":
            new_row_contacts_list[name_surname].update({
                "email": f"{new_row_contacts_list[name_surname]['email'] + new_inf['email']}"})

new_full_inf = list(new_row_contacts_list.values())

with open ("phonebook.csv", "w", encoding="UTF-8") as f:
    datawriter = csv.DictWriter(f, delimiter= ",", fieldnames=title)
    datawriter.writeheader()
    datawriter.writerows(new_full_inf)





