import time

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from pathlib import Path


base_url = "https://en.wikipedia.org"
counter = 100
error_birds = {"names": []}
error_index = 0


def scrap_bird_list():
    url = "https://en.wikipedia.org/wiki/List_of_birds_by_common_name"
    page = urlopen(url)
    html_bytes = page.read()
    html_data = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html_data, "html.parser")
    page_elements = soup.find_all('li')
    print("No. of Birds: "+str(len(page_elements)))
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


def scrap_bird_image(bird_name):
    bird_name = bird_name.replace(" ", "_").lower()
    print(bird_name)
    wiki_page_url = base_url + "/wiki/" + bird_name
    wiki_page = requests.get(wiki_page_url)
    soup = BeautifulSoup(wiki_page.content, "html.parser")
    image_link = soup.find('a', class_="image")
    try:
        download_url = base_url + image_link.attrs["href"]
        bird_image_page = requests.get(download_url)
        soup = BeautifulSoup(bird_image_page.content, "html.parser")
        bird_image = soup.find("div", id="file")
        print("https:" + bird_image.next.attrs["href"])
        save_image(bird_name, ".jpg", "https:" + bird_image.next.attrs["href"])
    except AttributeError:
        print("Attribute Error: "+bird_name)
        error_birds["names"].insert(error_index, bird_name)


def save_image(bird_name, extension, pic_url):
    headers = {
        'User-Agent': 'My User Agent 1.0'
    }
    image_content = requests.get(pic_url, headers=headers)
    directory = "birds/"+bird_name
    Path(directory).mkdir(parents=True, exist_ok=True)
    path = directory + "/" + bird_name + extension
    print(path)
    with open(path, "wb") as handle:
        handle.write(image_content.content)


if __name__ == '__main__':

    with open("birds.json", "r") as file:
        data = json.load(file)
        birds_data = data["birds"]
        i = 0
        while i < counter:
            scrap_bird_image(birds_data[i])
            time.sleep(4)
            i = i + 1
    with open("error.json", "w") as outfile:
        outfile.write(json.dumps(error_birds, indent=4))
