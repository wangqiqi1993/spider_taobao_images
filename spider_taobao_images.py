'''
given keywords,scrapy matched img on taobao
'''
import requests
import json
import time
import os
import datetime
import uuid
from hashlib import md5
img_path='taobaoimages'
if not os.path.exists(img_path):
    os.makedirs(img_path)
def getImageUrl(url):
    imgslist=[]
    response=requests.get(url).text
    jd=json.loads(response)
    imgs_list=jd['mods']['itemlist']['data']['auctions']
    for img_list in imgs_list:
        img_url=img_list['pic_url']
        imgslist.append(img_url)
    return imgslist
def save_images(list):
    for imgurl in list:
        if not imgurl.startswith('http:'):
            imgurl='http:'+imgurl
        img_name=str(uuid.uuid1()).replace('-', '_' )+'.jpg'
        down_name=os.path.join(img_path,img_name)
        if os.path.exists(md5(requests.get(imgurl).content).hexdigest()):
            continue
        with open(down_name,'wb') as fp:
            fp.write(requests.get(imgurl).content)
if __name__=='__main__':
    #q=input()#keyword
    q='儿童座椅'
    start_url='https://s.taobao.com/search?data-key=s&data-value={0}&ajax=true&_ksTS={1}&q={2}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_{3}&ie=utf8&s={4}'
    for page in range(0,1000,44):
        ksTS=str(time.time()*1000).replace('.','_')
        now=datetime.datetime.now().strftime('%Y%m%d')
        url=start_url.format(str(page+44),ksTS,q,now,str(page))
        list=getImageUrl(url)
        save_images(list)
