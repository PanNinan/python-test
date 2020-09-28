import os
import time
import requests
from lxml import etree

def get_img_url(url):
	'''
	:param url: 图集url
	:return: 图集名字和图片地址所构成的字典
	'''
	img = {}#空字典，用于放图片url和对应的编号
	html = requests.get(url)#获取页面源码
	html.encoding = 'gb2312'
	data = etree.HTML(html.text)#解析
	title = data.xpath('//div[@class="wrapper clearfix imgtitle"]/h1/text()')[0]#图集名
	page = data.xpath('//div[@class="wrapper clearfix imgtitle"]/h1/span/span[2]/text()')[0]#图集图片数
	img['1'] = data.xpath('//a[@class="down-btn"]/@href')[0]#第一张的图片地址
	for i in range(2,int(page)+1):
		#其余的图片地址
		img_url = etree.HTML(requests.get(url.replace('.html','_%s.html'%str(i))).text).xpath('//a[@class="down-btn"]/@href')[0]
		img['%s'%str(i)] = img_url#写入字典
	return title,img


def downloader(url,path,name,header={}):
	start = time.time()#开始时间
	if os.path.exists(path):  # 判断路径及文件夹是否存在，不存在即创建
		pass
	else:
		os.mkdir(path)
	size = 0
	if header is None:
		response = requests.get(url, stream=True)#stream属性必须带上
	else:
		response = requests.get(url, stream=True,headers=header)#stream属性必须带上
	chunk_size = 1024#每次下载的数据大小
	content_size = int(response.headers['content-length'])#总大小
	if response.status_code == 200:
		print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))#换算单位并print
		with open(path+'\\%s'%name, "ab") as file:
			for data in response.iter_content(chunk_size=chunk_size):
				file.write(data)
				file.flush()#清空缓存
				size += len(data)#已下载文件大小
				#\r指定行第一个字符开始，搭配end属性完成覆盖进度条
				print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size),float(size / content_size * 100)),end='')
	end = time.time()#结束时间
	print('\n'+"%s下载完成！用时%.2f秒"%(name,(end-start)))

if __name__ == '__main__':
	url_list=[]#放入所有页面url
	url = 'http://www.mmonly.cc/mmtp/'
	url_list.append(url)#先放入第一页
	html = requests.get(url)
	html.encoding = 'gb2312'
	page = etree.HTML(html.text).xpath('//a[text()="末页"]/@href')[0].split('_')[-1].split('.')[0]
	for i in range(2,int(page)+1):
		url_list.append(url+'list_9_{}.html'.format(str(i)))#其余页面url，注意第一页和其他页不一样
	for url_i in url_list:
		img_urls = etree.HTML(requests.get(url_i).text).xpath('//div[@class="ABox"]/a/@href')
		for img_url in img_urls:
			title,imgs = get_img_url(img_url)
			for img in imgs.keys():
				path = 'E:\\python\\mn\\%s' % title
				downloader(url= imgs[img],path=path,name='%s.jpg'%(title+img))