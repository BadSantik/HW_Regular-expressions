import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def format_phone_number(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?(доб\.)\s*(\d+)\)?)?"
    substitution = r"+7(\2)\3-\4-\5 \6\7"
    return re.sub(pattern, substitution, phone).strip()


contacts_dict = {}
for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).split()
    lastname = full_name[0] if len(full_name) > 0 else ""
    firstname = full_name[1] if len(full_name) > 1 else ""
    surname = full_name[2] if len(full_name) > 2 else ""

    organization = contact[3] if len(contact) > 3 else ""
    position = contact[4] if len(contact) > 4 else ""
    phone = format_phone_number(contact[5]) if len(contact) > 5 else ""
    email = contact[6] if len(contact) > 6 else ""

    key = (lastname, firstname)

    if key not in contacts_dict:
        contacts_dict[key] = [lastname, firstname,
                              surname, organization, position, phone, email]
    else:
        existing_contact = contacts_dict[key]
        contacts_dict[key] = [
            lastname,
            firstname,
            surname or existing_contact[2],
            organization or existing_contact[3],
            position or existing_contact[4],
            phone or existing_contact[5],
            email or existing_contact[6]
        ]

contacts_list = [contacts_list[0]] + list(contacts_dict.values())

with open("phonebook_raw.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)
