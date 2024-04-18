import json


def delete_mobo_entries(file_name):
    socket = {"AM4", "AM5", "LGA1700"}
    with open(file_name, 'r') as filepointer:
        data = json.load(filepointer)
    for elements in data:
        if elements['socket'] in socket:
            print(elements['socket'])
