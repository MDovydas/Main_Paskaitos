from bs4 import BeautifulSoup
import requests
import time
import csv

req = requests.Session()
server = "https://autogidas.lt"
headers = {
    'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 '
        'Safari/537.36 Edg/103.0.1264.44 '
}

data = []
data_count = 0
with open("autogidas.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Kaina", "Markė", "Modelis", "Variklio tūris", "galia, kW", "metai", "rida", "kėbulas"])

for i in range(1, 200):
    page = req.get(f'https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page={i}', headers=headers).text
    soup = BeautifulSoup(page, "html.parser")
    cars = soup.find_all(class_='list-item')
    for car in cars:
        data.append(["Nan", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])
        car_link = car.find('a', href=True)
        print("Getting data from:")
        print(car_link['href'])
        link = car_link['href']
        car_page = req.get(server + link, headers=headers).text
        car_soup = BeautifulSoup(car_page, "html.parser")
        find_price = car_soup.find_all(class_="price")
        for item in find_price:
            car_price = item.get_text()
            car_price = car_price.replace("€", "")
            data[data_count][0] = (int(car_price.replace(" ", "")))
            break
        params_block = car_soup.find_all(class_="params-block")[1]
        params_block = params_block.get_text()
        params_block = params_block.split('\n')
        counter = 0
        for param in params_block:
            if "Markė" in param:
                data[data_count][1] = params_block[counter + 1]
            if "Modelis" in param:
                data[data_count][2] = params_block[counter + 1]
            if "Variklis" in param:
                data[data_count][3] = float(params_block[counter + 1].split(" ")[0])
                if len(params_block[counter + 1].split(" ")) > 2:
                    data[data_count][4] = int(params_block[counter + 1].split(" ")[2])
                else:
                    power = "NaN"
            if "Metai" in param:
                data[data_count][5] = int(params_block[counter + 1].split("-")[0])
            if "Rida" in param:
                data[data_count][6] = int(params_block[counter + 1].split(" ")[0])
            if "Kėbulo tipas" in param:
                data[data_count][7] = params_block[counter + 1]

            counter += 1
        with open('autogidas.csv', 'a', newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data[data_count])
        data_count += 1

        time.sleep(1)
    time.sleep(1)
