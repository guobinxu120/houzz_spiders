# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from collections import OrderedDict
import json


class coolstuffinc_comSpider(scrapy.Spider):

	name = "coolstuffinc_com_spider"

	use_selenium = False
	# url = 'https://www.houzz.com/professionals/general-contractor/c/harrisburg--PA/d/25/p/15'
	url = 'https://www.houzz.com/professionals/general-contractor/s/Interior-Designers-%26-Decorators/c/harrisburg%2C-PA/d/25'
	total_count = 0
	categories_data = None
	result_data_list = {}
	custom_settings = {
	    'CONCURRENT_REQUESTS': 2,
	    'DOWNLOAD_DELAY': 1,
	    'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
	    'CONCURRENT_REQUESTS_PER_IP': 2
	}

	headers = ['PageUrl', 'ProductLink', 'ImageLink', 'Rarity', 'ProductTitle', 'NewQty', 'NewPrice', 'NewContent', 'NearMintQty', 'NearMintPrice', 'NearMintContent',
			   'FoilNearMintQty', 'FoilNearMintPrice', 'FoilNearMintContent',
			   'PlayedQty', 'PlayedPrice', 'PlayedContent', 'FoilPlayedQty', 'FoilPlayedPrice', 'FoilPlayedContent', 'SetName']


###########################################################

	def __init__(self, *args, **kwargs):
		super(coolstuffinc_comSpider, self).__init__(*args, **kwargs)
###########################################################

	def start_requests(self):
		yield scrapy.Request(
					url=self.url,
					callback=self.parseProductList, meta={'url': self.url})
		# yield scrapy.Request(
		# 			url='https://www.houzz.com/professionals/general-contractor/c/Middletown--PA/d/10/p/1605',
		# 			callback=self.parseProductList)

	# def parse_category(self, response):
    #
	# 	for subcategory_node in response.xpath('//section[@class="product-list"]//a'):
    #
	# 		subcategory_url = subcategory_node.xpath('./@href').extract_first()
	# 		set_name = subcategory_node.xpath('./text()').extract_first()
    #
	# 		if subcategory_url:
	# 			subcategory_url = response.urljoin( subcategory_url )
    #
	# 		yield scrapy.Request( url=subcategory_url, callback=self.parseProductList, meta={'set_name': set_name, 'cat': response.meta['cat'] } )


			####------------- test ----------------###
			# if subcategory_url == 'https://www.coolstuffinc.com/page/449':#?&resultsperpage=25&page=2':
			# 	yield scrapy.Request( url=subcategory_url, callback=self.parseProductList, meta={'set_name': set_name } )
			#####################################################

	def parseProductList(self, response):
		domain = 'https://www.coolstuffinc.com'
		products_list = json.loads(response.body.split('"itemListElement": ')[1].split(']')[0] + ']')
		url_list = []
		for product in products_list:
			try:
				url1 = product['url']
				if not url1:
					continue
				url_list.append(url1)
				yield scrapy.Request(
						url=url1,
						callback=self.parse_ind, meta={'catgory': response.url}, dont_filter=True)
			except:
				continue

		products_list1 = response.xpath('//div[@class="name-info"]/a[1]/@href').extract()

		# flag = True
		for product in products_list1:
			if product.__contains__('javascript') or product in url_list: continue
			url_list.append(product)
			yield scrapy.Request(
					url=product,
					callback=self.parse_ind, meta={'catgory': response.url}, dont_filter=True)

				# break

		nextLink = response.xpath('//*[@class="navigation-button next"]/@href').extract_first()
		if nextLink :
			print nextLink
			yield Request(response.urljoin(nextLink), callback=self.parseProductList, meta=response.meta, dont_filter=True)
		# else:
		# 	i = 0
		# 	pass

	def parse_ind(self, response):
		product = response

		item = OrderedDict()

		item['url'] = response.url

		item['name'] = product.xpath('.//*[@class="profile-full-name"]/text()').extract_first()
		item['phone number'] = product.xpath('.//*[@class="click-to-call-link text-gray-light trackMe"]/@phone').extract_first()
		item['website'] = product.xpath('.//*[@class="proWebsiteLink"]/@href').extract_first()

		item['contact name'] = ''
		item['zipcode'] = ''
		item['state'] = ''
		item['city'] = ''
		item['typical job costs'] = ''
		item['license number'] = ''


		info_list_label = response.xpath('.//*[@class="info-list-label"]')
		for info in info_list_label:
			if info.xpath('./i/@class').extract_first() == 'hzi-font hzi-Man-Outline':
				contact_name = info.xpath('./div/text()').extract_first()
				if contact_name:
					contact_name = contact_name.split(':')[-1]
					item['contact name'] = contact_name.strip()
			elif info.xpath('./i/@class').extract_first() == 'hzi-font hzi-Location':
				address_list = info.xpath('./div/span//text()').extract()

				try:
					zipcode = int(address_list[-1])
					item['zipcode'] = address_list[-1]
				except:
					item['zipcode'] = ''

				item['state'] = address_list[-2]
				item['city'] = info.xpath('./div/span/a/text()').extract_first()
				item['address'] = address_list[0]


				# l = len(address_list)
				# city = ''
				# state = ''
				# zipcode = ''
				# if l == 3:
				# 	zipcode = address_list[l - 2]
				# 	state = address_list[l - 3]
				# elif l == 4:
				# 	zipcode = address_list[l - 2]
				# 	state = address_list[l - 3]
				# 	city = address_list[l - 4]
				# elif l > 4:
				# 	zipcode = address_list[l - 2]
				# 	state = address_list[l - 3]
				# 	city = address_list[l - 4] + ' ' + address_list[l - 5]
				# item['zipcode'] = zipcode.strip()
				# item['state'] = state.strip()
				# item['city'] = city.strip()
				# item['address'] = ''
			elif info.xpath('./i/@class').extract_first() == 'hzi-font hzi-Cost-Estimate':
				cost = info.xpath('./div/span/text()').extract_first()
				if cost:
					cost = cost.split(':')[-1]
					item['typical job costs'] = cost.strip()
			elif info.xpath('./i/@class').extract_first() == 'hzi-font hzi-License':
				val = info.xpath('./div/text()').extract_first()
				if val:
					val = val.split(':')[-1]
					item['license number'] = val.strip()

		# item['zipcode'] = response.xpath('//*[@itemprop="postalCode"]/text()').extract_first()
		# item['state'] = response.xpath('//*[@itemprop="addressRegion"]/text()').extract_first()
		# item['city'] = response.xpath('//*[@itemprop="postalCode"]/a/text()').extract_first()
		# item['address'] = response.xpath('//*[@itemprop="streetAddress"]/text()').extract_first()

		item['review'] = product.xpath('.//*[@class="pro-review-string"]/span/text()').extract_first()

		project_count = product.xpath('.//*[@class="project-section"]/div/a/text()').re(r'[\d.,]+')
		item['project_count'] = ''
		if project_count:
			project_count = project_count[0]
			item['project_count'] = project_count

		profiles = response.xpath('.//div[@class="profile-content-wide about-section"]//div/text()').extract()
		item['description'] = ''
		desc = ''
		for p in profiles:
			p = p.strip()
			if p:
				desc += p + '\n'
		if desc:
			item['description'] = desc

		self.total_count += 1
		print 'total_count: ' + str(self.total_count)
		# print item
		# self.result_data_list[response.meta['cat']].append(item)
		item['category_page_url'] = response.meta['catgory']
		yield item

		# nextLink = response.xpath('//*[@id="nextLink"]/a/@href').extract_first()
		# if nextLink:
		# 	yield Request(response.urljoin(nextLink), callback=self.parseProductList, meta=response.meta)







