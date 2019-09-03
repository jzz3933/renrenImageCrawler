# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 13:10:03 2019

@author: Jzz
"""


import requests
import sys
from bs4 import BeautifulSoup
import re
import json
import calendar  #为了确定终止时间是在某个月的几号

import io
import time
import urllib
 
def Login(cookie_str):
    
    #浏览器登录后得到的cookie，一定要是Response Header里 status为200 OK的那个数据里的cookie
#    cookie_str = cookie
    #把cookie字符串处理成字典，以便接下来使用
    cookies = {}
    for line in cookie_str.split(';'):
#        print(line)
        key, value = line.split('=')
        cookies[key] = value
    
    #设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    #在发送get请求时带上请求头和cookies
    #resp = requests.get(url, headers = headers, cookies = cookies) 
    #用get方法，得到的实际是https://www.sui.com/tally/new.do的结果，没有需要的数据
    
    resp = requests.get(url,headers = headers, cookies = cookies)
    print(resp.text)
    #检查是否登录成功        
    if re.compile(r"***").search(resp.text):#自己的人人网的姓名
        print('Login Success')
        requestToken = re.findall("requestToken : '([^']*)',",resp.text) #正则出来是列表
        rtk = re.findall("_rtk : '([^']*)'",resp.text)
#        print(requestToken,rtk)
        return (cookies,1,requestToken[0],rtk[0])
    else:
        print('Login failed')
        return (cookies,0)
 
    
    
def savePic(albumUrl,cookies,requestToken,rtk):
#    try:
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    #在发送get请求时带上请求头和cookies
    
    resp = requests.get(albumUrl,headers = headers, cookies = cookies)
    data = resp.text
#        print(data)
#正则提取   # "albumId":"1083919536"    
    albumIdlist = re.findall('"albumId":"([^"]*)",',data)
#        imglist = re.findall('"url":"([^<]+)"}',data)
    print(albumIdlist)


 ##############根据得到的图片路径URL将图片下载下来保存本地########
    x= 0
    for albumId in albumIdlist:
        #每一个相册的网址
         
#        single_album_url = 'http://photo.renren.com/photo/***/album-%s/v7' %albumId  # 该网址最多只能解析前40张图片，其余的滚动鼠标，通过ajax加载出来的 
        for page_index in range(1,10):
#            print(albumId,str(page_index),requestToken,rtk)
            single_album_single_page_url = 'http://photo.renren.com/photo/***/album-%s/bypage/ajax/v7?page=%s&pageSize=20&requestToken=%s&_rtk=%s'  %(albumId,str(page_index),requestToken,rtk)
            cont = requests.get(single_album_single_page_url,headers = headers, cookies = cookies)
            #相册内部的源代码
#            print(cont.text)
            imglist = re.findall('"url":"([^"]*)"',cont.text)#找到每张图片的ID
    #        print(imglist)
            if imglist !=[]: #如果为空，则终止
                    
                #处理网址去除\
                for index,item in enumerate(imglist):
                    if '\\' in item:
                        imglist[index] = imglist[index].replace('\\','')
#                print(imglist)
                for single_pic_url in imglist:     
                    print(single_pic_url)
                    ##############根据得到的图片路径URL将图片下载下来保存本地########  
                    request = urllib.request.Request(url = single_pic_url, headers=headers)
                    response = urllib.request.urlopen(request)
                    img = response.read()
                    with open('F:\image\miao\miao%s.jpg' %x, 'wb') as fp:
                        fp.write(img)
        #            urllib.request.urlretrieve(single_pic_url,r'D:\image\miao\miao%s.jpg' %x)
                        print('miao%s.jpg done' %x)
                        x+=1

      

#登录后才能访问的网页
url = 'http://www.renren.com/34434***' # 自己的登陆主页
albumUrl = "http://photo.renren.com/photo/***/albumlist/v7?offset=0&limit=40#"# ***为你想下载图片的朋友的人人ID

 
cookie_str = r'***'#为简便起见，利用cookie登陆，火狐浏览器可以利用HttpFox工具查看
login_result = Login(cookie_str)
cookies = login_result[0]


# 
if login_result[1] == 1:
    requestToken = login_result[2]
    rtk = login_result[3]
    savePic(albumUrl,cookies,requestToken,rtk)
