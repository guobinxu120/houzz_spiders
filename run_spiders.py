# -*- coding: utf-8 -*-
#!/usr/bin/python
from multiprocessing import Pool
import os, sys, csv, platform, datetime, glob


def _crawl(spider_name_params=None):
	if spider_name_params:
		print spider_name_params
		print ">>>>> Starting {} spider".format(spider_name_params)
		command = 'scrapy crawl {}'.format(spider_name_params)

		os.system(command)
		print "finished."
	return None

def run_crawler(spider_names):

	for spider_name in spider_names:

		pool = Pool(processes=5)
		pool.map(_crawl, [spider_name])

if __name__ == '__main__':
	spider_names = []
	if len(sys.argv) == 1:
		spider_names = ['nastygal_com_spider', 'coolstuffinc_com_spider', 'theoutnet_com_spider', 'trollandtoad_com_spider']
	elif len(sys.argv) == 2:
		spider_names = [sys.argv[1]]
	run_crawler(spider_names)
