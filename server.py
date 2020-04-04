# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2020-03-26 11:20:32
# @Last Modified by:   wangfpp
# @Last Modified time: 2020-04-04 16:31:34
## coding: utf-8

from requests_html import HTMLSession, HTMLResponse
import os, sys, time
import random

curr_path = os.path.dirname(os.path.abspath(__file__))
comm_path = os.path.dirname(curr_path)
if comm_path not in sys.path:
    sys.path.append(comm_path)

class Search:
    def __init__(self):
        self.baseUrl = 'https://www.99zuowen.com'

    def searchFn(self):
        '''寻找主入口的下级标签  并进行分类  返回标签的title href'''
        session = HTMLSession()
        r  = session.get(self.baseUrl, timeout = 10)
        # 寻找入口的html
        navBar = r.html.find('div.mainnav>ul.nav.clearfix>li')
        url_list = []
        length = len(navBar)
        for index in range(1, length):
            catlogDict = {};
            element = navBar[index]
            a_node, sub_node = element.find('a[href]', first=True), element.find('div.sub_nav>a', first=False)
            main_title, main_href = self.fetchTitlandHref(a_node)

            catlogDict["sub"] = []
            sub_node_length = len(sub_node)
            for _index in range(0,sub_node_length):
                title, href = self.fetchTitlandHref(sub_node[_index])
                sub_catlog_dict = {"title": title, "href": href}
                catlogDict["sub"].append(sub_catlog_dict)
            catlogDict["main"] = {"title": main_title, "href": main_href}
            url_list.append(catlogDict)
        return url_list

    def fetchTitlandHref(self,element):
        ''' 把a标签的href和text提取出来'''
        title, href = element.text, list(element.absolute_links)[0]
        return title, href

    def searchTxt(self, dictCatlog, index):
        '''寻找节点内的文本
        dictCatlog = {sub:[{title: String, href: String_Url}], 
                    main: {title: String, href: String_URL}
                }
        '''
        main, sub = dictCatlog["main"], dictCatlog["sub"]
        sublen = len(sub)
        
        # if main:
        #     self.createFolder(main["title"], False)
        # if sublen > 0:
        #     for item in sub:
        #         title, href = item["title"], item["href"]
        #         print(title)
        #         self.createFolder(title, main)
        # return True

    def createFolder(self, title, main):
        '''创建目录 title创建目录的名字  main是否有上级目录'''
        if main:
            folderPath = curr_path + '/txt/' + main["title"] + "/" + title
            pathExsits = self.folderIsExit(folderPath)
            if not pathExsits:
                os.mkdir(folderPath)
        else:
            folderPath = curr_path + '/txt/' + title
            pathExsits = self.folderIsExit(folderPath)
            if not pathExsits:
                os.mkdir(folderPath)
    def folderIsExit(self, path):
        '''判断目录是否存在'''
        return os.path.exists(path)

if __name__ == "__main__":
    result = Search()
    print(result.searchFn())