import json


def delete_mobo_entries(file_name):
    socket = {"AM4", "AM5", "LGA1700"}
    with open(file_name, 'r') as filepointer:
        data = json.load(filepointer)
    for elements in data:
        if elements['socket'] in socket:
            print(elements['socket'])


def create_new_gpu_file(file_name):
    unique_chipset = {"GeForce RTX 3050 8GB": 1,
                      "GeForce RTX 3060 12GB": 1,
                      "GeForce RTX 3070 LHR": 1,
                      "GeForce RTX 3080 12GB LHR": 1,
                      "Geforce RTX 3090": 1,
                      "GeForce RTX 4060": 1,
                      "GeForce RTX 4070": 1,
                      "GeForce RTX 4070 Ti": 1,
                      "GeForce RTX 4080": 1,
                      "GeForce RTX 4090": 1,
                      "Radeon RX 6600 XT": 1,
                      "Radeon RX 6700 XT": 1,
                      "Radeon RX 6800 XT": 1,
                      "Radeon RX 6900 XT": 1,
                      "Radeon RX 7600": 1,
                      "Radeon RX 7700 XT": 1,
                      "Radeon RX 7800 XT": 1,
                      "Radeon RX 7900 XT": 1,
                      "Radeon RX 7900 XTX": 1,
                      }
    graphics_cards = {}
    with open(file_name, 'r') as filepointer:
        data = json.load(filepointer)
    for elements in data:
        if elements['chipset'] in unique_chipset and unique_chipset[elements['chipset']] == 1:
            graphics_cards[elements['chipset']] = elements
            unique_chipset[elements['chipset']] = 0

    with open('gpu.json', 'w') as fp:
        json.dump(list(graphics_cards.values()), fp, indent=4)



def create_new_mobo_file(file_name):
    unique_chipset = {"AM4": 8,
                      "AM5": 8,
                      "LGA1700" : 16
                      }
    cpu = {}
    with open(file_name, 'r') as filepointer:
        data = json.load(filepointer)
    for elements in data:
        if elements['socket'] in unique_chipset and unique_chipset[elements['socket']] != 0:
            cpu[elements['name']] = elements
            unique_chipset[elements['socket']] = unique_chipset.get(elements['socket']) - 1

    with open('motherboard.json', 'w') as fp:
        json.dump(list(cpu.values()), fp, indent=4)


def create_new_cpu_file(file_name):
    unique_chipset = {"AMD Ryzen 7 7800X3D": 1,
                      "AMD Ryzen 5 7600X": 1,
                      "AMD Ryzen 7 5800X3D": 1,
                      "AMD Ryzen 9 7950X": 1,
                      "Intel Core i5-12400F": 1,
                      "Intel Core i5-13400F": 1,
                      "Intel Core i5-12600K": 1,
                      "Intel Core i7-13700K": 1,
                      "Intel Core i7-12700K": 1,
                      }
    cpu = {}
    with open(file_name, 'r') as filepointer:
        data = json.load(filepointer)
    for elements in data:
        if elements['name'] in unique_chipset and unique_chipset[elements['name']] != 0:
            cpu[elements['name']] = elements
            unique_chipset[elements['name']] = unique_chipset.get(elements['name']) - 1

    with open('cpu.json', 'w') as fp:
        json.dump(list(cpu.values()), fp, indent=4)
