# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_booking_url = scrapy.Field()
    hotel_coordinates = scrapy.Field()
    hotel_rating = scrapy.Field()
    hotel_description = scrapy.Field()

    # TODO Continue scraping additional details from 'item['hotel_booking_url']'
    # TODO add more scrapy.Field() lines
    # hotel_more_description = scrapy.Field()