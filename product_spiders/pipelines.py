# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import csv, os
from scrapy.exporters import CsvItemExporter
from email.mime.text import MIMEText
import smtplib

class product_spidersPipeline(object):
    def __init__(self):
        self.exporters = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if spider.name == 'csi':
            self.filename = spider.name + ".csv"

            file = open('output/' + self.filename, mode='w+b', buffering=0 )
            # file = io.open('output/' + self.filename, mode='w', encoding='utf-16', newline='\n',  buffering=1)
            # exporter = CsvItemExporter( file, encoding='utf-16' )
            # exporter = CsvItemExporter( file, encoding='utf-8' )
            exporter = CsvItemExporter(file)

            EXPORT_FIELDS = [

                'ProductLink',
                'ImageLink',
                'Rarity',
                'ProductTitle',
                'NearMintQty',
                'NearMintPrice',
                'PlayedQty',
                'PlayedPrice',
                'SetName',
            ]

            exporter.fields_to_export = EXPORT_FIELDS
            exporter.start_exporting()

            self.exporters['Result'] = exporter

    def spider_closed(self, spider):
        pass
        # if spider.name == 'nastygal_com_au':
        #     dir_path = 'output/{}'.format(spider.name)
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #
        #     for key in spider.result_data_list.keys():
        #         file_name = '{}_{}'.format(spider.name, key)
        #         filepath = '{}/{}_result.csv'.format(dir_path, file_name)
        #         data = spider.result_data_list[key]
        #         headers = spider.headers
        #
        #         f1 = open(filepath, "wb")
        #         writer = csv.writer(f1, delimiter=',',quoting=csv.QUOTE_ALL)
        #         writer.writerow(headers)
        #
        #         for item in data:
        #             d = item.values()
        #             new_d = []
        #             for dd in d:
        #                 try:
        #                     new_d.append(dd.encode('utf-8'))
        #                 except:
        #                     new_d.append(dd)
        #             writer.writerow(new_d)
        #         f1.close()
        #
        #     # send result file through email.
        #     #     fp = open(filepath, 'rb')
        #         # msg = MIMEText(fp.read())
        #         msg = MIMEText('')
        #         # fp.close()
        #
        #         me = 'your email'
        #         you = 'email to send'
        #
        #         msg['Subject'] = 'Scraper Result({}_result.csv)'.format(file_name)
        #         msg['From'] = me
        #         msg['To'] = you
        #         msg.add_header('Content-Disposition', 'attachment', filename=filepath)
        #
        #         server = smtplib.SMTP('smtp.gmail.com', 587)
        #         server.starttls()
        #         server.login(me, 'your password')
        #         server.sendmail(me, [you], msg.as_string())
        #         server.quit()
        #         print "Successfully send result file({}_result.csv) to {}.".format(file_name, you)
        # elif spider.name == 'csi':
        #     for exporter in self.exporters.itervalues():
        #         exporter.finish_exporting()

    def process_item(self, item, spider):
        if spider.name == 'csi':
            self.exporters['Result'].export_item(item)
        return item
