import scrapy
import re


class MrestateSpider(scrapy.Spider):
    name = "mrestate"

    start_urls = ["https://mrestate.ir/f/tehran/buy_residential_apartment"]

    def parse(self, response):
        detail_page_links = response.css("article.w-full.px-4.py-5 a")
        yield from response.follow_all(detail_page_links, self.parse_detail)

        next_page_link = response.css(
            'a.flex.p-0.justify-center::attr(href)').getall()[-1]
        yield response.follow(next_page_link, self.parse)

    def parse_detail(self, response):
        district_name = response.css(
            'div.flex.items-center.text-14.font-medium.text-customBlack.mx-3::text').getall()[1]

        real_estate_type = response.css(
            'p.text-14.text-gray-400::text').getall()[2]

        features = features = response.css(
            'div.flex.flex-wrap.mb-6 div.text-sm.font-medium::text').getall()
        features_length = len(features)

        real_estate_area = int(re.findall(
            r"\d+", features[0])[0]) if features_length > 0 else None
        real_estate_age = 1402 - \
            int(re.findall(r"\d+", features[1])[0]
                ) if features_length > 1 else None
        total_rooms = int(re.findall(
            r"\d+", features[2])[0]) if features_length > 2 else None
        floor = int(re.findall(
            r"\d+", features[2])[0]) if features_length > 3 else None

        price = response.css(
            'div.text-16.text-left.font-medium.text-customBlack::text').get()
        price = "".join(price.split(" ")[0].split(","))

        facilities = response.css(
            'ul.flex.flex-wrap.mb-6.py-3 div.text-customBlack.px-3.text-sm.font-medium::text').getall()

        for index, facility in enumerate(facilities):
            if 'پارکینگ' in facility:
                try:
                    number_of_parking = int(re.findall(r"\d+", facility)[0])
                except IndexError:
                    number_of_parking = 0
                facilities.pop(index)
                break
        else:
            number_of_parking = 0

        yield {
            #     "district_number": district_number,
            "district_name": district_name,
            "real_estate_type": real_estate_type,
            "real_estate_area": real_estate_area,
            "total_rooms": total_rooms,
            "number_of_parking": number_of_parking,
            "real_estate_age": real_estate_age,
            "price": price,
            "facilities": facilities,
            "floor": floor,
        }
