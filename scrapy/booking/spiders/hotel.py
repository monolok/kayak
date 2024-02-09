import scrapy
from booking.items import BookingItem
import json

#TODO scrapy crawl hotel -o output.json

class HotelSpider(scrapy.Spider):
    cities = open('cities.json')
    cities = json.load(cities)
    name = "hotel"
    allowed_domains = ["booking.com"]

    def start_requests(self):
        base_url = "https://www.booking.com/searchresults.en-gb.html?ss="
        for city in self.cities:
            url = base_url+city
            yield scrapy.Request(url=url, callback=self.parse, meta={'city': city})

    def parse(self, response):
        city = response.meta['city']  # Retrieve the city name passed from start_requests
        hotel_list = response.xpath('//*[@data-testid="property-card"]')
        for hotel in hotel_list:
            item = BookingItem()
            item['city'] = city
            item['hotel_name'] = hotel.xpath('.//*[@data-testid="title"]/text()').get()
            item['hotel_booking_url'] = hotel.xpath('.//a[contains(@class, "a78ca197d0")]/@href').get()
            item['hotel_rating'] = hotel.xpath('//*[@data-testid="review-score"]/div/text()').get()
            item['hotel_description'] = hotel.xpath('.//div[contains(@class, "abf093bdfe")]/text()').get()
            # item['hotel_coordinates'] = 
            yield item