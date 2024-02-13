import scrapy
from booking.items import BookingItem
import json
import os
from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from .env
CITIES_PATH = os.getenv('CITIES_PATH') # Path to fetch your list of cities to work on

#* run scrapy crawl hotel -o output.json

class HotelSpider(scrapy.Spider):
    # loading the file with all the cities to scrape for
    with open(CITIES_PATH) as cities_file:
        cities = json.load(cities_file)
    name = "hotel"
    allowed_domains = ["booking.com"]

    # Here is the call back to build all the url to yield a request for each city to be used with self.parse
    #* Scrapy always go to start_requests first and there it sees the callback parse
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
            
            yield item
            
            # TODO Instead of yielding the item above, yield a another request with the url from item['hotel_booking_url']
            # TODO the url will be used with another def called self.parse_hotel_details using call back to handle the response
            #*yield scrapy.Request(url=response.urljoin(item['hotel_booking_url']), callback=self.parse_hotel_details, meta={'item': item})
            #! notice the use of response.urljoin()
    
    #* This method is intended to scrape additional details from each hotel's booking page
    #def parse_hotel_details(self, response):
        #* Retrieve the item passed from the `parse` method
        #item = response.meta['item']

        # TODO Scrape additional details from 'item['hotel_booking_url']'
        #item['hotel_more_description'] = response.xpath('Xpath').get()

        #! yield item marks the end of building the item object
        #! yield scrapy.Request() with a callback make it continue further
        #yield item