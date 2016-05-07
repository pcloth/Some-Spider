# -*- coding: utf-8 -*-
'''
获取太平洋摄影部落人像图片 for py3.5

'''
import requests,os

from lxml import html

def get_response(url):
    # 填充请求的头部
    headers = {
        "headers" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    return response

#从人像首页开始获取50个相册。
def get_page():
    start_url = 'http://dp.pconline.com.cn/list/all_t2.html'
    response = get_response(start_url)
    parsed_body = html.fromstring(response.text)
    href = parsed_body.xpath('//div[@class="wtPic"]/a/@href')
    
    return href

def get_this_page(page_urls):
    album_id=0
    for url in page_urls:
        page_id=1
        next_page=url
        album_id+=1
        album=[]
        while True:
            response = get_response(next_page)
            htxt=response.text
            parsed_body = html.fromstring(htxt)
            
            this_pic_url=htxt[htxt.find('J-BigPic'):htxt.find('arrPos arrLeft')]
            this_pic_url=this_pic_url.split('"/></span>')[0]
            this_pic_url=this_pic_url[this_pic_url.find('http://'):] #清洗URL
    
            next_page=htxt[htxt.find('nLink = "'):htxt.find('function bindEvent')]
            next_page=next_page.split('"')[1] #获取并清洗下一页url
            
            title= parsed_body.xpath('//div[@class="dTitInfo"]/strong/@title')
            title= title[0].replace('&nbsp;&nbsp',' ')
            
            photographer=htxt[htxt.find('<i id="Jcamerist"'):htxt.find('<i class="view">')]
            photographer=photographer[photographer.find('blank')+7:photographer.find('</a>')]

            album.append(this_pic_url)
            
            if htxt.find('isLastPage = true')>0:
                print('%d : (%s)相册共计%d张图片,正在下载...'%(album_id,title,page_id))
                get_images(photographer,title,album,page_id)
                break
            page_id+=1
                
# 开始下载图片
def get_images(photographer,title,album,pic_count):

    count = 1
    # 图片的默认存储文件夹
    start_dir = 'E:/pconline/'
    dir_name = (start_dir + title+' ['+str(pic_count)+'p] by '+photographer)
    
    #检测文件夹是否存在，如果存在就跳过下载（如果相册下到一半终止，直接删除文件夹重新下载就好。）
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        for url in album:
            with open(dir_name + '/' + str(count)+'.jpg', 'wb') as f:
                r = get_response(url)
                f.write(r.content)
            count += 1
    else:
        print(title+'已经下载过了。')
    
        
        
if __name__ == '__main__':
    print('获取太平洋摄影部落人像图片...\n\n作者：pcloth\n制作日期：2016-05-07\nemail:pcloth@163.com')
    page_urls=get_page()
    get_this_page(page_urls)
   

