import csv
import re

# ВАРИНТ 1
# with open("phonebook_raw.csv", encoding="UTF8") as f:
#     rows = csv.reader(f, delimiter=",")
#     contacts_list = list(rows)
#
#
# def list_LFS(data):
#     result = []
#     for contact in data:
#         if len(contact) > len(data[0]):
#             contact.pop(-1)
#             line = ",".join(contact)
#             lastname = re.match(r"(\w+)[\S+|\s+]?(\w+)[\S+|\s+](\w+)", line)
#             contact[0] = lastname.group(1)
#             contact[1] = lastname.group(2)
#             contact[2] = lastname.group(3)
#             result.append(contact)
#         else:
#             line = ",".join(contact)
#             lastname = re.match(r"(\w+)[\S+|\s+]?(\w+)[\S+|\s+](\w+)", line)
#             contact[0] = lastname.group(1)
#             contact[1] = lastname.group(2)
#             contact[2] = lastname.group(3)
#             result.append(contact)
#     return result
#
# def get_unique_numbers(list):
#     unique = []
#
#     for item in list:
#         if item in unique:
#             continue
#         else:
#             unique.append(item)
#     return unique
#
# def contacts_list1(contacts_list):
#     list1 = list_LFS(contacts_list)
#
#     for data_contact1 in list1:
#         for contact_list2_2 in list1:
#             if data_contact1[0] == contact_list2_2[0]:
#                 index = list1.index(contact_list2_2)
#                 for i in range(len(contact_list2_2)):
#                     if len(contact_list2_2[i]) > len(data_contact1[i]):
#                             list1[index][i] = contact_list2_2[i]
#                     else:
#                             list1[index][i] = data_contact1[i]
#     return get_unique_numbers(list1)
#
# def contacts_list1_normal_form_tel(list):
#     result = []
#     for contact in contacts_list1(list):
#         ii = ",".join(contact)
#         tel = re.sub(
#             r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?\s*?(\d{3})[\s-]?\s*?(\d{2})[\s-]?\s?(\d{2})\s+(\(?(\w+)\.\s+(\d+)\)?)?",
#             r"+7(\2)\3-\4-\5 \7.\8", ii)
#         kk = re.split(r",", tel)
#         result.append(kk)
#
#     return result
#
#
# with open("phonebook.csv", "w",encoding="UTF8") as f:
#   datawriter = csv.writer(f, delimiter=",",lineterminator="\r")
#   datawriter.writerows(contacts_list1_normal_form_tel(contacts_list))
#
#

# ВАРИНТ 2

with open("phonebook_raw.csv", encoding="UTF8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def list_LFS(data):
    result = []
    for contact in data:
        line = ",".join(contact)
        lastname = re.match(r"(\w+)[\S+|\s+]?(\w+)[\S+|\s+](\w+)", line)
        contact[0] = lastname.group(1)
        contact[1] = lastname.group(2)
        contact[2] = lastname.group(3)
        result.append(contact)
    return result


def get_unique_numbers(data_list):
    unique = []

    for item in data_list:
        if item in unique:
            continue
        else:
            unique.append(item)
    for temporary in data_list:
        for temporary_2 in data_list:
            if temporary_2[0] == temporary[0] and temporary_2 > temporary:
                ii = unique.index(temporary)
                unique.pop(ii)

    return unique


def contacts_list1(contacts_list):
    list1 = list_LFS(contacts_list)
    for contact_list1_1 in list1:
        for contact_list2_2 in list1:
            if contact_list1_1[0] == contact_list2_2[0] and contact_list1_1 != contact_list2_2:
                index = list1.index(contact_list2_2)
                counter = -1
                for i, s in zip(contact_list2_2, contact_list1_1):
                    counter += 1
                    if len(i) > len(s):
                        list1[index][counter] = contact_list2_2[counter]
                    else:
                        list1[index][counter] = contact_list1_1[counter]

    return get_unique_numbers(list1)


def contacts_list1_normal_form_tel(list):
    result = []
    for contact in contacts_list1(list):
        ii = ",".join(contact)
        tel = re.sub(
            r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?\s*?(\d{3})[\s-]?\s*?(\d{2})[\s-]?\s?(\d{2})\s+(\(?(\w+)\.\s+(\d+)\)?)?",
            r"+7(\2)\3-\4-\5 \7.\8", ii)
        kk = re.split(r",", tel)
        result.append(kk)

    return result


with open("phonebook.csv", "w", encoding="UTF8") as f:
    datawriter = csv.writer(f, delimiter=",", lineterminator="\r")

    datawriter.writerows(contacts_list1_normal_form_tel(contacts_list))
