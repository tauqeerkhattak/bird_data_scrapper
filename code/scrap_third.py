import requests
from bs4 import BeautifulSoup


class ScrapThird:
    base_url = "https://www.oiseaux.net/birds/"

    def scrape_website(self, bird_name):
        bird_name = bird_name.replace(" ", ".")
        url = self.base_url + bird_name + ".html"
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        img = soup.find("img", class_="on_img_id")
        print(img.attrs['src'])

    def scrape(self):
        self.scrape_website("African marsh harrier")
