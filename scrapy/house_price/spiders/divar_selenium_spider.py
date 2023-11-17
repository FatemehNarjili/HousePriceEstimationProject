import json
from time import sleep

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class DivarSeleniumSpider(scrapy.Spider):
    name = "divar_selenium"

    start_urls = ["https://divar.ir/s/tehran/buy-residential"]

    def parse(self, response):
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))
        driver.get('https://divar.ir/s/tehran/buy-residential')
        driver.implicitly_wait(20)

        end_of_scroll = driver.execute_script(
            "return document.body.scrollHeight")
        i = 0
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            sleep(2)
            my_scroll = driver.execute_script(
                "return document.body.scrollHeight")
            if my_scroll == end_of_scroll:
                break
            end_of_scroll = my_scroll

            sleep(5)
            elems = driver.find_elements(
                By.CSS_SELECTOR, "div.post-card-item-af972.kt-col-6-bee95.kt-col-xxl-4-e9d46 a[href]")
            list_of_tokens = [elem.get_attribute(
                'href').split("/")[-1] for elem in elems]

            detail_page_links = []
            for token in list_of_tokens:
                detail_page_links.append(
                    f"https://api.divar.ir/v8/posts/{token}")
            yield from response.follow_all(detail_page_links, self.parse_detail)

            i += 1
            sleep(2)

    def parse_detail(self, response):
        district_name = None
        real_estate_type = None
        real_estate_area = None
        real_estate_age = None
        total_rooms = None
        price = None
        price_per_meter = None
        real_estate_agencey = None
        floor = None
        elevator = None
        parking = None
        warehouse = None
        units_per_floor = None
        document = None
        building_direction = None
        unit_status = None
        facilities = []

        detail_data = json.loads(response.body.decode('utf-8'))

        district_name = detail_data['data']['district']

        real_estate_type = detail_data['data']['category']['slug']

        for data in detail_data['widgets']['list_data']:
            if data['title'] == "اطلاعات":
                items = data.get("items")
                for item in items:
                    if item['title'] == "متراژ":
                        real_estate_area = item['value']
                    if item['title'] == "ساخت":
                        real_estate_age = item['value']
                    if item['title'] == "اتاق":
                        total_rooms = item['value']

            if data['title'] == "قیمت کل":
                price = data['value']

            if data['title'] == "قیمت هر متر":
                price_per_meter = data['value']

            if data['title'] == "آژانس املاک":
                real_estate_agencey = data['value']

            if data['title'] == "طبقه":
                floor = data['value']

            if data['title'] == "ویژگی‌ها و امکانات":
                items = data.get("items")
                for item in items:
                    if item['title'] == "آسانسور":
                        elevator = item['available']
                    if item['title'] == "پارکینگ":
                        parking = item['available']
                    if item['title'] == "انباری":
                        warehouse = item['available']

                facility_page = data.get("next_page")
                if facility_page is not None:
                    facility_list = facility_page.get("widget_list")
                    for facility in facility_list:
                        if (facility['data'].get('text') == "ویژگی‌ها") or (facility['data'].get('text') == "امکانات"):
                            pass
                        elif facility['data']['title'] == "تعداد واحد در طبقه":
                            units_per_floor = facility['data']['value']
                        elif facility['data']['title'] == "سند":
                            document = facility['data']['value']
                        elif facility['data']['title'] == "جهت ساختمان":
                            building_direction = facility['data']['value']
                        elif facility['data']['title'] == "وضعیت واحد":
                            unit_status = facility['data']['value']
                        else:
                            if facility['data']['has_divider'] == True:
                                facilities.append(facility['data']['title'])

        yield {
            "district_name": district_name,
            "real_estate_type": real_estate_type,
            "real_estate_area": real_estate_area,
            "real_estate_age": real_estate_age,
            "total_rooms": total_rooms,
            "price": price,
            "price_per_meter": price_per_meter,
            "real_estate_agencey": real_estate_agencey,
            "floor": floor,
            "elevator": elevator,
            "parking": parking,
            "warehouse": warehouse,
            "units_per_floor": units_per_floor,
            "document": document,
            "building_direction": building_direction,
            "unit_status": unit_status,
            "facilities": facilities
        }
