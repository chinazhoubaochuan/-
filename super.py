from selenium import webdriver
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from bs4 import BeautifulSoup
import json
import re
root=r"E:\pythontool\myuse\watchclass"
school='youschool'
class superstartload(object):
    def __init__(self,url):
        try:
            self.driver=webdriver.Chrome(r"D:\py\Scripts\chromedriver.exe")
            self.driver.get(url)
            self.driver.implicitly_wait(5)
        except:
            print('link error')
    def loadweb_nocheckcode(self,user,passward):
        userload=self.driver.find_element_by_xpath(r'//input[@id="unameId"]').send_keys(user)
        pwdload=self.driver.find_element_by_xpath(r'//input[@id="passwordId"]').send_keys(passward)
        picweb=self.driver.find_element_by_xpath(r'//img[@id="numVerCode"]')
        self.driver.find_element_by_id("selectSchoolA").click()
        self.driver.find_element_by_id('searchSchool1').send_keys(school)
        self.driver.find_element_by_class_name('zw_t_btn').click()
        time.sleep(0.5)
        self.driver.find_element_by_id('1820').click()
    def savecookies(self):
        cookies=self.driver.get_cookies()   
        jsonCookies = json.dumps(cookies)
        os.chdir(root)
        with open('cookiessave.json', 'w') as f:
            f.write(jsonCookies)
    def readcookies(self):
        os.chdir(root)
        with open('cookiessave.json', 'r') as f:  
            listCookies=json.loads(f.read())      
            return listCookies
    def savefile(self,name,data):
        os.chdir(root)
        with open(name,'w') as f:
            f.write(data)
    def readfile(self,name):
        os.chdir(root)
        with open(name,'r') as f:
            data=f.read()
        return data
    def loadcookies(self,cookies):
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
    def saveweb(self,course):
        iframe=self.driver.find_element_by_xpath(r'//iframe[@name="frame_content"]')
        self.driver.switch_to.frame(iframe)
        pattern=r"//a[@title="+ r'"' + course + r'"' +']'
        wait=WebDriverWait(self.driver,10)
        try:
            webdriver=wait.until(Ec.presence_of_all_elements_located((By.XPATH,pattern)))
        except:
            print('未找到元素！')
            pass
        html=self.driver.find_element_by_xpath(pattern).get_attribute('href')
        self.savefile('web.txt',html)
    def readweb(self):
        return self.readfile('web.txt')
    def str2times(self,listenstr):
        listenstr+=":"
        tempstr=""
        mode=1
        times=0
        for listentemp in listenstr:
            if listentemp == ':':
                times+=int(tempstr)+int(tempstr)*mode*59
                tempstr=""
                mode=0
            else:
                empstr+=listentemp
        return times
    #用途：进入对应章节主页面，并返回根目录,如果根目录不存在，则返回[]
    def __intomainweb(self,url,chapter):
        self.driver.switch_to.default_content()
        self.driver.get(url)
        soup=BeautifulSoup(self.driver.page_source,'lxml')
        temp=soup.find(class_="chapterNumber",text=chapter)
        html=temp.parent.a['href']
        html='https://mooc1-1.chaoxing.com'+html
        self.driver.get(html)
        root=list()
        for temp in range(1,10):
            pattern='dct'+str(temp)
                #第一次等待temp载入
            if temp==1:
                wait=WebDriverWait(self.driver,10)
                try:
                    wait.until(Ec.presence_of_element_located((By.ID,pattern)))#as value write error  except catch word error
                except:
                    return []
            try:
                root.append(self.driver.find_element_by_id(pattern))
            except:
                print("当前有"+str(temp-1)+"个子页面")
                break
        return root
    #用途：进入根目录，并返回下面的视屏列表//PPT列表
    def __intosubweb(self,root):
        root.click()
        wait=WebDriverWait(self.driver,10)
        wait.until(Ec.presence_of_element_located((By.ID,"iframe")))
        iframeroot=self.driver.find_element(By.XPATH,r'//iframe[@id="iframe"]')
        time.sleep(1)
        self.driver.switch_to.frame(iframeroot)
        alliframe=self.driver.find_elements_by_tag_name('iframe')
        count=0
        for ses in alliframe:
            count+=1
        print("当前有"+str(count)+"个子任务")
        return alliframe
    #功能：把视屏列表内的课全部听完
    def __getlistentime(self):
        try:
            timestring=self.driver.find_element_by_xpath(r'//div[@aria-label="进度小节"]').get_attribute('aria-valuetext')
            obj= re.findall("([0-9]{0,2}):([0-9]{0,2})",timestring,re.S)
            time1=int(obj[0][0])*60+int(obj[0][1])
            time2=int(obj[1][0])*60+int(obj[1][1])
            times=time2-time1+1
            return times
        except:
            try:
                time1=int(obj[0][0])*3600+int(obj[0][1])*60+int(obj[1][1])
                time2=int(obj[2][0])*3600+int(obj[2][1])*60+int(obj[3][1])
                times=time2-time1+1
                return times
            except:
                return 1
    def __Drag_process(self):
        print("开始移动：")
        dot=self.driver.find_element_by_xpath(r'//div[@aria-label="进度小节"]')#vjs-play-progress vjs-slider-bar
        operate=ActionChains(self.driver)
        operate.move_to_element_with_offset(dot,645,0)
        operate.click()
        operate.perform()
        print('结束移动')
    def __listenclass(self,video):
            self.driver.switch_to.frame(video)
            try:
                wait=WebDriverWait(self.driver,10)
                wait.until(Ec.presence_of_element_located((By.XPATH,r'//button[@class="vjs-big-play-button"]')))
                element=self.driver.find_element_by_xpath(r'//button[@class="vjs-big-play-button"]')
            except:
                self.driver.switch_to.parent_frame()
                return 1
            mouse=ActionChains(self.driver)
            mouse.move_to_element(element)
            mouse.click()
            mouse.perform()
            #1.得到听课时间
            #time.sleep(1)#my_change
            try:
                element=self.driver.find_element_by_xpath(r'//button[@title="播放"]')
            except:
                pass  
            try:
                for i in range(0,3):
                    operate=self.driver.find_element(By.XPATH,r'//button[@title="播放速度"]').click()
                    time.sleep(0.3)
                try:
                    self.__Drag_process()
                except:
                    print('不能托条')
            except:
                print("该视频没有倍数")
            times=self.__getlistentime()
            if times == 1:
                times=10080
                #开始时load写错位置了
            load=0
                #防止第一次读错数据
            while times!=1:
                time.sleep(3)
                try:
                    temp=self.__getlistentime()
                    if load==0 and temp==1:
                            time.sleep(5)
                            print('可能是游览器卡死,再试一次')
                    else:
                        load=1
                    if times-temp == 0:#vjs-play-control vjs-control vjs-button vjs-playing
                        try:
                            element=self.driver.find_element_by_xpath(r'//button[@title="播放"]')
                        except:
                            pass
                        mouse.move_to_element(element)
                        mouse.click()
                        mouse.perform()
                    times=temp
                except:        
                    print('获取时间失败')
                print(times)
            print('听完一课')    
            time.sleep(2) 
            return 0
    #功能：听课
    def __clickppt(self,ppt):
        self.driver.switch_to.frame(ppt)
        element=self.driver.find_element_by_id('img')
        operate=ActionChains(self.driver)
        operate.move_to_element(element)
        operate.click()
        operate.perform()
        wait=WebDriverWait(self.driver,10)
        try:
            page=self.driver.find_element_by_xpath(r'//span[@class="all"]').text
            index=self.driver.find_element_by_xpath(r'//span[@class="num"]').text
            print(page,index)
            count=0
            while (index != page) :
                time.sleep(1)
                nowindex=self.driver.find_element_by_xpath(r'//span[@class="num"]').text
                if nowindex == index :
                    count+=1
                    print('正在尝试点击......'+str(count) )
                    if count > 8 :
                        print('可能不是点击按钮')
                        return 
                else:
                    count=0
                    index=nowindex
                wait.until( Ec.presence_of_element_located((By.XPATH,r'//div[@title="下一页"]')) )
                element=self.driver.find_element_by_xpath(r'//div[@title="下一页"]')
                operate.move_to_element(element)
                operate.click()
                operate.perform()
            print("测试完成，请参考实物结果进行修改")            
        except:
            print("可能是按完了，请参考实物结果进行修改")
    #功能：把视屏列表内的课全部听完(空目录状态)
    def __findvideo_unroot(self):
        try:
            self.driver.switch_to.default_content()
            wait=WebDriverWait(self.driver,10)
            wait.until(Ec.presence_of_element_located((By.ID,"iframe")))
            #document 定位有误：
            #此处有坑，两个iframe
            iframeroot=self.driver.find_element(By.XPATH,r'//iframe[@id="iframe"]')
            time.sleep(1)
            self.driver.switch_to.frame(iframeroot)
            alliframe=self.driver.find_elements_by_tag_name('iframe')
            count=0
            for ses in alliframe:
                count+=1
                print("当前有"+str(count)+"个子任务")
            return alliframe
        except:
            print('空页面错误！')
            return  [] 
    def listenclass(self,url,chapter):
        roots=self.__intomainweb(url,chapter)
        #没有根目录
        if roots == []:
            subvideo=self.__findvideo_unroot()
            for video in subvideo:
                if self.__listenclass(video) == 1:
                    try:
                        self.driver.switch_to.parent_frame() 
                        self.__clickppt(video)
                    except:
                        print('该页面为题目，请自己做')
                self.driver.switch_to.parent_frame() 
            return
        #有根目录：
        for root in roots:
            #寻找有无视屏：
            subvideo=self.__intosubweb(root)
            if subvideo == []:
                break
            else:
                for video in subvideo:
                    if self.__listenclass(video) == 1:
                        try:
                            self.__clickppt(video)
                        except:
                            print('该页面为题目，请自己做')
                    self.driver.switch_to.parent_frame()
                self.driver.switch_to.parent_frame() 
        self.driver.switch_to.default_content()                   
indexroot='http://i.mooc.chaoxing.com/space/index?t=1574264821050'
#web.listenclass(studyroot,16)
web=superstartload('http://passport2.chaoxing.com/login?fid=&refer=http://i.mooc.chaoxing.com')
classname='youclass'
user='123456789'
passward='123456'
#第一次载入cookies要先输入验证码再采集 
command=input()
todyroot=['1.1','1.2','1.3','1.4','1.5','1.6','1.7']
if command == 'savecookies':
    web.loadweb_nocheckcode(user,passward)
    #在输入网页验证码后按回车
    input()
    web.savecookies()
    web.saveweb(classname)
    studyroot=web.readweb()
    web.listenclass(studyroot,todyroot)
elif command == 'loadcookies':
    #若cookies没过期，第二次登陆时可输入loadcookies，不用重复登录
    print('正在载入cookies资源......')
    cookies=web.readcookies()
    web.loadcookies(cookies)
    print('载入完成！')
    for couse in todyroot:
        try:
            web.listenclass(web.readweb(),couse)
        except:
            print('当前课未知')
