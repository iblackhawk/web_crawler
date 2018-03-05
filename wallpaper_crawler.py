# -*-coding:utf8-*-
# "__author__" = "Black Hawk"
# @Time : 2018/2/27 19:40
# @Software: PyCharm
import requests
import re


for i in range(1,21):#爬取20页的壁纸
    url='https://alpha.wallhaven.cc/toplist?page={}'.format(i)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    pic_list = []  # 收集首页下图片缩略图地址
    pic_download = []  # 保存图片的下载地址

    # url = 'https://alpha.wallhaven.cc/toplist'  # 壁纸网站的精选
    response = requests.get(url=url, headers=headers, stream=True)
    html = response.text
    # print html
    # exit(0)
    res = re.findall(r'<a class="preview" href="(.*?)" ', html)  # 通过re 找寻缩略图地址
    for i in res:
        pic_list.append(i)  # 将地址遍历加入列表
        # print i
    for i in range(len(pic_list)):  # 在缩略图地址内，找寻原图地址
        # https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-621636.jpg
        last_html = requests.get(pic_list[i]).text
        pic_html = re.findall(r'content="//(.*?)" /><link rel=', last_html)
        for index in pic_html:
            pic_download.append(index)  # 将地址遍历加入列表
            # print index
    for i in range(len(pic_download)):
        pic_download[i] = 'https://{}'.format(pic_download[i])  # 给地址加上前戳
        pic_name=re.findall(r'-(.*?).jpg',pic_download[i])
        # print pic_download[i]
        # print pic_name
        # exit(1)
        download = requests.get(url=pic_download[i], headers=headers, stream=True)
        with open('%s.jpg'%pic_name, 'wb') as f:  # 循环写入图片
            for chunk in download.iter_content(512):  # 以512每块进行流传输
                f.write(chunk)


