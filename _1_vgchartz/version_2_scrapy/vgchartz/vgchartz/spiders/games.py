import scrapy


class GamesSpider(scrapy.Spider):
    name = 'games'
    allowed_domains = ['www.vgchartz.com']

    def createUrl(n):
        return f"http://www.vgchartz.com/games/games.php?page={n}&order=Sales&ownership=Both&direction=DESC&showtotalsales={n}&shownasales={n}&showpalsales={n}&showjapansales={n}&showothersales={n}&showpublisher={n}&showdeveloper={n}&showreleasedate={n}&showlastupdate={n}&showvgchartzscore={n}&showcriticscore={n}&showuserscore={n}&showshipped={n}/"
    
    page_list = list(range(1, 1250))
    start_urls = map(createUrl,page_list)


    def parse(self, response):
        rows = response.xpath('//*[@id="generalBody"]/table[1]/tr')
        for row in rows:
            pos = row.xpath('.//td[1]/text()').get()
            gameName = row.xpath('.//td[3]/a/text()').get()
            console = row.xpath('.//td[4]/img/@alt').get()
            publisher = row.xpath('.//td[5]/text()').get()
            developer = row.xpath('.//td[6]/text()').get()
            vgChartzScore = row.xpath('.//td[7]/text()').get()
            criticScore = row.xpath('.//td[8]/text()').get()
            userScore = row.xpath('.//td[9]/text()').get()
            totalShipped = row.xpath('.//td[10]/text()').get()
            totalSales = row.xpath('.//td[11]/text()').get()
            naSales = row.xpath('.//td[12]/text()').get()
            palSales = row.xpath('.//td[13]/text()').get()
            jpSales = row.xpath('.//td[14]/text()').get()
            otherSales = row.xpath('.//td[15]/text()').get()
            releasedDate = row.xpath('.//td[16]/text()').get()
            lastUpdate = row.xpath('.//td[17]/text()').get()
            yield {
                'Position': pos,
                'Game Name': gameName,
                'Console': console,
                'Publisher': publisher,
                'Developer': developer,
                'VGChartz Score': vgChartzScore,
                'Critic Score': criticScore,
                'User Score': userScore,
                'Total Shipped': totalShipped,
                'Total Sales': totalSales,
                'NA Sales': naSales,
                'PAL Sales': palSales,
                'Japan Sales': jpSales,
                'Other Sales': otherSales,
                'Release Date': releasedDate,
                'Last Update': lastUpdate,
            }
