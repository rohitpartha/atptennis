from scrapy import Spider, Request
from atptennis.items import atptennisItem
import time
from scrapy.shell import inspect_response
class atptennisSpider(Spider):
    name = 'atptennis_spider'
    allowed_urls = ['https://www.atptour.com/']
    start_urls = ['https://www.atptour.com/en/rankings/singles']

    def parse(self, response):
        ##get current date

        current_date = response.xpath('//ul[@data-value="rankDate"]/li[@class="current"]/@data-value').extract_first()
        #print(current_date)
        ##scraping rank 1-500
        rank_ranges = ["0-100", "101-200", "201-300", "301-400", "401-500"]
        ##list comprehension to construct url for pages to crawl to
        ranking_urls = ['https://www.atptour.com/en/rankings/singles/?rankDate={0}&rankRange={1}'.format(current_date,x)
                        for x in rank_ranges]



        # Yield the requests to different ranking urls,
        # using parse_ranking_page function to parse the response.
        for ranking_url in ranking_urls:
           yield Request(url=ranking_url, callback=self.parse_ranking_page)

    def parse_ranking_page(self, response):
        #get links to player pages

        player_urls = response.xpath('//div[@class="table-rankings-wrapper"]//td[@class="player-cell"]/a/@href').extract()
        #change overview to player-stats
        player_urls = list(map(lambda x: x.replace("overview", "player-stats"), player_urls))

        #get the rankings
        rankinglist = response.xpath('//div[@class="table-rankings-wrapper"]//td[@class="rank-cell"]/text()').extract()
        rankinglist = list(map(lambda x: x.strip(), rankinglist))

        #get the player names
        player_names = response.xpath('//div[@class="table-rankings-wrapper"]//td[@class="player-cell"]/a/text()').extract()

        #zip the info into a tuple
        player_infos = list(zip(player_urls, rankinglist, player_names))

        for player_info in player_infos:
            yield Request(url='https://www.atptour.com' + player_info[0], callback=self.parse_playerstats_page,
                          meta={'url': response.url, 'player_name': player_info[2],'current_ranking': player_info[1]})


    def parse_playerstats_page(self, response):
        ##get the tables with the player data on the career page
        #service_table = response.xpath('//table[@class="mega-table"]')[0]
        #time.sleep(10)
        #inspect_response(response,self)


        #get list of years
        years = response.xpath('//ul[@data-value="year"]/li/@data-value').extract()
        #get list of surfaces
        surfaces = response.xpath('//ul[@data-value="surfaceType"]/li/@data-value').extract()
        print(surfaces)
        #loop through years and surfaces to scrape all data
        for year in years:
            for surface in surfaces:
                url = response.url + "?year={0}&surfaceType={1}".format(year,surface)
                yield Request(url=url,
                              callback=self.parse_playerstatsdetails_page, meta={'year': year, 'surface': surface,
                                                                                 'url': response.meta['url'],
                                                                                  'player_name': response.meta['player_name'],
                                                                                  'current_ranking': response.meta['current_ranking']})


    def parse_playerstatsdetails_page(self, response):


        #check if table exists
        try:
            service_table = response.xpath('//table[@class="mega-table"]')[0]
            return_table = response.xpath('//table[@class="mega-table"]')[1]
        except IndexError:
            item = atptennisItem()
            item['current_ranking'] = response.meta['current_ranking']
            item['player_name'] = response.meta['player_name']
            item['year'] = response.meta['year']
            item['surface'] = response.meta['surface']
            item['service_aces'] = ""
            item['service_double_faults'] = ""
            item['service_first_serve_percent'] = ""
            item['service_first_serve_points_won'] = ""
            item['service_second_serve_points_won'] = ""
            item['service_break_points_faced'] = ""
            item['service_break_points_saved'] = ""
            item['service_games_played'] = ""
            item['service_games_won'] = ""
            item['service_percent_points_won'] = ""

            item['return_first_serve_points_won_percent'] = ""
            item['return_second_serve_points_won_percent'] = ""
            item['return_break_point_opportunities'] = ""
            item['return_break_points_converted_percent'] = ""
            item['return_games_played'] = ""
            item['return_games_won_percent'] = ""
            item['return_points_won_percent'] = ""
            item['return_total_points_won'] = ""
            item['url'] = response.meta['url']
            return item


        ##loop through service table rows to pick off information
        servicelist = []
        returnlist = []
        for row in service_table.xpath('.//tbody//tr'):
            #for each row, get the td tags with the info
            tdtext = row.xpath('.//td/text()').extract()
            servicelist.append(tdtext[1].strip('\r\n\t\t'))

        ##loop through return table rows to pick off information
        for row in return_table.xpath('.//tbody//tr'):
            #for each row, get the td tags with the info
            tdtext = row.xpath('.//td/text()').extract()
            returnlist.append(tdtext[1].strip('\r\n\t\t'))

        item = atptennisItem()
        item['current_ranking'] = response.meta['current_ranking']
        item['player_name'] = response.meta['player_name']
        item['year'] = response.meta['year']
        item['surface'] = response.meta['surface']
        item['service_aces'] = servicelist[0]
        item['service_double_faults'] = servicelist[1]
        item['service_first_serve_percent'] = servicelist[2]
        item['service_first_serve_points_won'] = servicelist[3]
        item['service_second_serve_points_won'] = servicelist[4]
        item['service_break_points_faced'] = servicelist[5]
        item['service_break_points_saved'] = servicelist[6]
        item['service_games_played'] = servicelist[7]
        item['service_games_won'] = servicelist[8]
        item['service_percent_points_won'] = servicelist[9]

        item['return_first_serve_points_won_percent'] = returnlist[0]
        item['return_second_serve_points_won_percent'] = returnlist[1]
        item['return_break_point_opportunities'] = returnlist[2]
        item['return_break_points_converted_percent'] = returnlist[3]
        item['return_games_played'] = returnlist[4]
        item['return_games_won_percent'] = returnlist[5]
        item['return_points_won_percent'] = returnlist[6]
        item['return_total_points_won'] = returnlist[7]
        item['url'] = response.meta['url']
        return item

