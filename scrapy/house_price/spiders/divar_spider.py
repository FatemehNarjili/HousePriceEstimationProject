import scrapy
import json


class DivarSpider(scrapy.Spider):
    name = "divar"

    start_urls = [
        "https://api.divar.ir/v8/web-search/tehran/buy-residential?page=1"]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):

        list_of_tokens = []
        data = json.loads(response.body.decode('utf-8'))
        post_list = data['web_widgets']['post_list']
        for i in range(len(post_list)):
            list_of_tokens.append(post_list[i]['data'].get('token', None))

        detail_page_links = []
        for token in list_of_tokens:
            if token is not None:
                detail_page_links.append(
                    f"https://api.divar.ir/v8/posts/{token}")

        yield from response.follow_all(detail_page_links, self.parse_detail)

        self.page_number += 1
        yield response.follow(f"https://api.divar.ir/v8/web-search/tehran/buy-residential?page={self.page_number}", self.parse)

    def parse_detail(self, response):
        district_name = None
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
