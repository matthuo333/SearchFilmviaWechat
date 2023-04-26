from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from SearchAPP import globalvar as gl

from selenium import webdriver
from lxml import etree
#import requests
import time
import youtube_dl
from os import rename
import re

# Create your views here.

class SearchView(APIView):
    
    def post(self,request,*args,**kwargs):
        
        # Do my job
        
        print(request.data)
        
        
        #Inital for webdriver
        browser = webdriver.Chrome()
        browser.maximize_window()   #设置浏览器大小：全屏
        browser.get('https://www.youtube.com') 

        time.sleep(8)

        #input_box = browser.find_element_by_id('center')
        input_box = browser.find_element_by_tag_name('input')
        try:
             #input_box.clear() #clear last text in inputbox
             #输入内容：video of twitter
             #input_box.send_keys('https://twitter.com/i/status/1484543746205175814')
             input_box.send_keys(request.data['test'])
             print('搜索KEY：',request.data['test'])
        except Exception as e:
             print('fail')

        time.sleep(3)
         #定位搜索按钮
        button = browser.find_element_by_id('search-icon-legacy')
        try:
             #点击搜索按钮
             button.click()
             print('成功搜索')
        except Exception as e:
             print('fail搜索')

        time.sleep(5)
             

        source = browser.page_source

        html = etree.HTML(source)

        urllist = html.xpath('//h3//a[@id="video-title"]/@href')


        searchlist = html.xpath('//a[@id="video-title"]/@title')

        print("searchlist : ")
        
        cop = re.compile(r"[^\u4e00-\u9fa5^a-z^A-Z^0-9^\b^\000^ ^-]")
        
        BuildDic = {'viewid': '',
                    'message': '' 
                    }
        
        BuildArray = []
        searchlist1 = ''
        

        j = 0

        for i in searchlist : 
            newfilename = cop.sub('', searchlist[j])
            searchlist1 = '['+str(j+1)+'] '+newfilename+'\n'
            BuildDic['viewid'] = j
            BuildDic['message'] = searchlist1
            #BuildArray[j] = BuildDic
            BuildArray.append(BuildDic.copy())
            print(searchlist1)
            print(BuildArray[j])
            j += 1

        print("urllist2 : ")
        j = 0

        for i in urllist : 
            print("[",j,"]",urllist[j])
            j += 1
        
        gl.set_value('urllist',urllist)
        gl.set_value('videoname',searchlist)
        
        return Response({"status":"MattTrue","SearchedName": BuildArray })
    
    #    return Response({"status":"MattTrue"})
    
class DLView(APIView):

    def post(self,request,*args,**kwargs):
          
        url = gl.get_value('urllist')
        videoname = gl.get_value('videoname')
        print("get value :",url)
        print("get videoname :",videoname)
        
        OptIndex = int(request.data['test'])
        print("Old Filename :", videoname[OptIndex])

        # Download video using Youtube-dl

        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)

        gl.set_value('percent','0')
        
        def my_hook(d):
            if d['status'] == 'downloading':
                print('percent:{:.0%}'.format(d['downloaded_bytes']/d['total_bytes']))
                gl.set_value('percent',d['downloaded_bytes']/d['total_bytes'])
            
            elif d['status'] == 'finished':
                specialChars = r'\/:*?*<>|"' # refer to https://zhuanlan.zhihu.com/p/343985720
                for specialChar in specialChars:
                    videoname[OptIndex] = videoname[OptIndex].replace(specialChar, '')# refer to https://blog.csdn.net/SeeTheWorld518/article/details/47346143
                print("New Filename :", videoname[OptIndex])
                file_name = r'C:\Users\matt_4215\Search\{}.mp4'.format(videoname[OptIndex])
                rename(d['filename'], file_name)
                print('下载完成{}'.format(file_name))




        ydl_opts = {
        #    'format': 'bestaudio/best',
            'outtmpl': '%(id)s%(ext)s',
            'format': 'best',
        #    'postprocessors': [{
        #        'key': 'FFmpegExtractAudio',
        #        'preferredcodec': 'mp3',
        #        'preferredquality': '192',
        #    }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/{}'.format(url[OptIndex])])
        
        return Response({"DLStatus":"True"})

class ProgressView(APIView):
    
    def get(self,*args,**kwargs):
        
        var = gl.get_value('percent')
        print("enter to Progress view:", var)
        
        return Response({"result":int(var*100)})
        #return Response(float("0.865")*100)
        #var = gl.set_value('percent')
        #if var == 'null' :
        #    return Response()

#set_user(urllist)