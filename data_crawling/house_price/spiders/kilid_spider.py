import scrapy
import re


class KilidSpider(scrapy.Spider):
    name = "kilid"

    start_urls = ["https://kilid.com/buy-residential/tehran"]

    def parse(self, response):
        detail_page_links = response.css("a.style_plp-card-link__yPlrt")
        yield from response.follow_all(detail_page_links, self.parse_detail)

        next_page_number = response.css(
            "button.px-3.justify-center::text").get()
        yield response.follow(f"?page={next_page_number}", self.parse)

    def parse_detail(self, response):
        district = response.css("p.mb-6::text").get().split("،")
        district_number = district[1].strip()
        district_number = int(re.findall(r"\d", district_number)[0])
        district_name = district[2].strip()

        features = [li.css("::text").get() for li in response.css("ul.m-0 li")]
        real_estate_type = features[1]
        real_estate_area = float(features[2])

        for i in range(3, 6):
            if not features[i].isnumeric():
                features[i] = 0

        total_rooms = int(features[3])
        number_of_parking = int(features[4])
        real_estate_age = int(features[5])

        price = response.css("h1.mb-6::text").get()
        price, unit = re.split(r'(\d+(?:\.\d+)?)', price)[1:]
        if unit.strip() == "میلیارد":
            price = float(price) * 1_000_000_000
        elif unit.strip() == "میلیون":
            price = float(price) * 1_000_000

        facilities = response.css("span.text-lg.text-gray-800::text").getall()

        yield {
            "district_number": district_number,
            "district_name": district_name,
            "real_estate_type": real_estate_type,
            "real_estate_area": real_estate_area,
            "total_rooms": total_rooms,
            "number_of_parking": number_of_parking,
            "real_estate_age": real_estate_age,
            "price": price,
            "facilities": facilities,
        }
