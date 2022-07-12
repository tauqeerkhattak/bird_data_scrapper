import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

base_url = "https://www.bing.com"
search = "/images/search?q="


class ScrapThird:

    def scrape_images(self, bird_name):
        bird_name = bird_name.replace(" ", "+")
        url = base_url + search + bird_name + "&first=1&tsc=ImageHoverTitle"
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ul = soup.find("ul", class_="dgControl_list")
        print(len(ul.contents))
        index = 0
        for i in ul.contents:
            a = i.next.next.next
            data = json.loads(a.attrs["m"])
            print(data["murl"])
            self.save_image(index, bird_name, ".jpg", data["murl"])
            index += 1
            time.sleep(5)

    def save_image(self, index, bird_name, extension, pic_url):
        bird_name = bird_name.replace("'", "").replace("+", "-").lower()
        image_content = requests.get(pic_url)
        directory = "birds/" + bird_name
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        path = directory + "/" + bird_name + "_" + str(index) + extension
        with open(path, "wb") as handle:
            handle.write(image_content.content)


    def scrap(self):
        i = 0
        with open("birds.json", "r") as data_file:
            temp = json.loads(data_file.read())
            birds_list = temp["birds"]
            print(birds_list)
            while i < 50:
                self.scrape_images(birds_list[i])
                i += 1