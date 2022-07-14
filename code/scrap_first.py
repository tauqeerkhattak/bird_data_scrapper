import json
from pathlib import Path

import requests
import os
from PIL import Image
from bs4 import BeautifulSoup

base_url = "https://animalia.bio/"
error_list = {"names": []}


class ScrapFirst:
    def save_image(self, image_url, bird_name):
        image_page = requests.get(image_url)
        directory = "birds/" + bird_name
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        path = directory + "/" + bird_name + ".webp"
        with open(path, "wb") as handle:
            handle.write(image_page.content)
        image = Image.open(path).convert("RGB")
        image.save("birds/" + bird_name + "/" + bird_name + "_1.jpg", "jpeg")
        os.remove(path)

    def scrap_data(self, bird_name):
        bird_name = bird_name.replace(" ", "-").replace("'", "").lower()
        url = base_url + bird_name
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            div = soup.find('div', class_="s-char-img open-gallery")
            image = div.next.next
            self.save_image(image.attrs["src"], bird_name)
        except AttributeError:
            print("Image not found: " + bird_name)
            error_list["names"].insert(0, bird_name)


    def scrap(self):
        with open("birds.json", "r") as json_file:
            data = json.load(json_file)
            birds = data["birds"]
            i = 0
            while i < 700:
                print("Bird No: "+str(i))
                self.scrap_data(birds[i])
                i += 1

        with open("error.json", "w") as outfile:
            outfile.write(json.dumps(error_list, indent=4))
