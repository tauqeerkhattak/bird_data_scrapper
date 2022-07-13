import time

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from pathlib import Path


class ScrapSecond:
    base_url = "https://en.wikipedia.org"
    error_birds = {"names": []}
    error_index = 0

    def scrap_bird_list(self):
        url = "https://en.wikipedia.org/wiki/List_of_birds_by_common_name"
        page = urlopen(url)
        html_bytes = page.read()
        html_data = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html_data, "html.parser")
        page_elements = soup.find_all('li')
        print("No. of Birds: " + str(len(page_elements)))
        count = 0
        birds_json = {'birds': []}
        with open("birds.json", "w") as outfile:
            index = 0
            for i in page_elements:
                count = count + 1
                if 27 < count < 11002:
                    print(i.text)
                    birds_json['birds'].insert(index, i.text)
                    index = index + 1
            print(birds_json)
            outfile.write(json.dumps(birds_json, indent=4))

    def scrap_bird_image(self, bird_name):
        bird_name = bird_name.replace(" ", "_").lower()
        wiki_page_url = self.base_url + "/wiki/" + bird_name
        wiki_page = requests.get(wiki_page_url)
        soup = BeautifulSoup(wiki_page.content, "html.parser")
        image_link = soup.find('a', class_="image")
        try:
            download_url = self.base_url + image_link.attrs["href"]
            bird_image_page = requests.get(download_url)
            soup = BeautifulSoup(bird_image_page.content, "html.parser")
            bird_image = soup.find("div", id="file")
            print("https:" + bird_image.next.attrs["href"])
            self.save_image(bird_name, ".jpg", "https:" + bird_image.next.attrs["href"])
        except AttributeError:
            print("Attribute Error: " + bird_name)
            self.error_birds["names"].insert(self.error_index, bird_name)

    def save_image(self, bird_name, extension, pic_url):
        headers = {
            'User-Agent': 'My User Agent 1.0'
        }
        bird_name = bird_name.replace("'", "").replace("_", "-")
        image_content = requests.get(pic_url, headers=headers)
        directory = "birds/" + bird_name
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        path = directory + "/" + bird_name + extension
        with open(path, "wb") as handle:
            handle.write(image_content.content)

    def scrap(self):
        with open("birds.json", "r") as file:
            data = json.load(file)
            birds_data = data["birds"]
            i = 500
            while i <= 700:
                print("Bird No: " + str(i) + " Name: " + str(birds_data[i]))
                self.scrap_bird_image(birds_data[i])
                time.sleep(3)
                i = i + 1
        with open("error.json", "w") as outfile:
            outfile.write(json.dumps(self.error_birds, indent=4))
