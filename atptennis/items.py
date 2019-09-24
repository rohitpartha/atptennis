# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class atptennisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    player_name = scrapy.Field()
    surface = scrapy.Field()
    year = scrapy.Field()
    current_ranking = scrapy.Field()
    service_aces = scrapy.Field()
    service_double_faults = scrapy.Field()
    service_first_serve_percent = scrapy.Field()
    service_first_serve_points_won = scrapy.Field()
    service_second_serve_points_won = scrapy.Field()
    service_break_points_faced = scrapy.Field()
    service_break_points_saved = scrapy.Field()
    service_games_played = scrapy.Field()
    service_games_won = scrapy.Field()
    service_percent_points_won = scrapy.Field()

    return_first_serve_points_won_percent = scrapy.Field()
    return_second_serve_points_won_percent = scrapy.Field()
    return_break_point_opportunities = scrapy.Field()
    return_break_points_converted_percent = scrapy.Field()
    return_games_played = scrapy.Field()
    return_games_won_percent = scrapy.Field()
    return_points_won_percent = scrapy.Field()
    return_total_points_won = scrapy.Field()
    url = scrapy.Field()
