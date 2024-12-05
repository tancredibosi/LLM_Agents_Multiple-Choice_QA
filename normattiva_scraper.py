import os
import json
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

NUMERO_ART = "123"
NUMERO_COMMA = "1"
NUMERO_LEGGE = "1398"
ANNO = "1930"


class NormattivaScraper:
    def __init__(self, driver_path, headless=True):
    
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def fill_field(self, field_id, value):
        input_field = self.driver.find_element(By.ID, field_id)
        input_field.clear()
        input_field.send_keys(value)

    def get_originario(self):
        atto_version = self.driver.find_element(By.CSS_SELECTOR, "[action*='/atto/caricaDettaglioAtto']")
        buttons = atto_version.find_elements(By.CLASS_NAME, "check-custom-button")

        for button in buttons:
            if button.text == "originario":
                button.click()
                break

    def click_article(self, article_num):
        albero = self.driver.find_element(By.ID, "albero")
        articles = albero.find_elements(By.CLASS_NAME, "numero_articolo")
        for article in articles:
            # MODIFICATO QUI
            article_text = ''.join(filter(str.isdigit, article.text))
            if article_text == article_num:
                article.click()
                break

    def download_akomantoso(self, provvedimento, anno):
        self.fill_field("numeroProvvedimento", provvedimento)
        self.fill_field("annoProvvedimento", anno)

        self.driver.find_element(By.CSS_SELECTOR, "[type*='submit']").click()
        time.sleep(1)
        self.driver.find_elements(By.CSS_SELECTOR, "[title*='Dettaglio atto']")[0].click()
        self.get_originario()
        time.sleep(2)

        element = self.driver.find_element(By.XPATH, '//a[normalize-space(text())="esporta in Akoma ntoso"]')

        element.click()

    def get_article_text(self, provvedimento, anno, article_num):
        self.fill_field("numeroProvvedimento", provvedimento)
        self.fill_field("annoProvvedimento", anno)

        self.driver.find_element(By.CSS_SELECTOR, "[type*='submit']").click()
        time.sleep(1)
        self.driver.find_elements(By.CSS_SELECTOR, "[title*='Dettaglio atto']")[0].click()
        self.get_originario()
        time.sleep(2)

        if len(article_num) == 0:
            albero = self.driver.find_element(By.ID, "albero")
            articles = albero.find_elements(By.CLASS_NAME, "numero_articolo")

            commas_dict = ""
            for article in articles:
                if is_convertible_to_int(article.text):
                    article.click()
                    time.sleep(2)
                    body_testo = self.driver.find_element(By.CLASS_NAME, "bodyTesto")
                    article_text = body_testo.find_element(By.CLASS_NAME, "art-just-text-akn").text
                    commas_dict += article_text + " "
        else:
            self.click_article(article_num)
            time.sleep(2)

            body_testo = self.driver.find_element(By.CLASS_NAME, "bodyTesto")
            commas = body_testo.find_elements(By.CLASS_NAME, "art-comma-div-akn")
            
            commas_dict = {}
            for comma in commas:
                comma_num = comma.find_element(By.CLASS_NAME, "comma-num-akn").text[:-1]
                commas_dict[comma_num] = comma.text

            if len(commas) == 0:
                # MODIFICATO QUI
                try:
                    article_commas = body_testo.find_element(By.CLASS_NAME, "art-just-text-akn").text
                except:
                    article_commas = body_testo.find_element(By.CLASS_NAME, "attachment-just-text").text
                if "\n\n" in article_commas:
                    all_commas_text = article_commas.split("\n\n")
                else:
                    all_commas_text = article_commas.split("\n")
                for i, text in enumerate(all_commas_text):
                    commas_dict[str(i + 1)] = text

        output_dict = {
            "provvedimento": provvedimento,
            "anno": anno,
            "article": article_num,
            "commas": commas_dict
        }

        return output_dict

    def navigate_to_page(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()


def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def merge_dict_text(input_dict):
    merged_text = ""
    for key, value in input_dict.items():

        if value is not None:
            merged_text += str(value) + " "
    return merged_text.strip()


def main():
    driver_path = "/usr/local/bin/chromedriver"
    scraper = NormattivaScraper(driver_path, headless=True)
    scraper.navigate_to_page("https://www.normattiva.it/ricerca/avanzata")
    article_data = scraper.get_article_text(NUMERO_LEGGE, ANNO, NUMERO_ART)

    if NUMERO_COMMA is None:
        article_text = merge_dict_text(article_data['commas'])
    else:
        article_text = article_data['commas'][NUMERO_COMMA]

    print(article_data)
    print(article_text)

if __name__ == "__main__":
    main()
