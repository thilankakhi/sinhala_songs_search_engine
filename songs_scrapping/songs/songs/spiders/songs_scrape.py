import scrapy
from songs.items import SongItem
from datetime import datetime
import re
import os

class Songs(scrapy.Spider):
    name = "my_scraper"

    start_urls = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/"]

    for i in range(1, 22):
        start_urls.append("https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(i) + "")

    def parse(self, response):
        for href in response.xpath('//div[@class="col-md-6 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col"]//a/@href'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        separator = ','
        item = SongItem()

        item['title'] = response.xpath('//span[@class="sinTitle"]/text()').extract()
        item['artist'] = response.xpath('//div[@class="su-row"]//span[@class="entry-categories"]//a/text()').extract()
        item['genre'] = response.xpath('//div[@class="su-row"]//span[@class="entry-tags"]//a/text()').extract()
        item['writer'] = response.xpath('//div[@class="su-row"]//span[@class="lyrics"]//a/text()').extract()
        item['music'] = response.xpath('//div[@class="su-row"]//span[@class="music"]//a/text()').extract()
        visits = response.xpath('//div[@class="tptn_counter"]/text()').extract()
        item['visits'] = separator.join(visits).replace("Visits", "").replace("-", "").strip()
        #item['lyrics'] = response.xpath('//div[@class="entry-content"]//pre/text()').extract()
        songBody = (response.xpath('//div[@class="entry-content"]//pre/text()').extract())
        songBodySplit = []
        for parts in songBody:
            lines = parts.split('\n')
            for line in lines:
                songBodySplit.append(line)

        song = ""
        chords = ""

        for line in songBodySplit:
            if (re.search('[a-zA-Z]', line)):
                chords = chords + line + "\n"
            else:
                if (len(line) != 0):
                    line = line.replace('+', '')
                    line = line.replace('|', '')
                    line.strip()
                    song = song + line + os.linesep

        item['lyrics'] = song
        yield item
