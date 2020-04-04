# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2020-03-26 11:20:32
# @Last Modified by:   wangfpp
# @Last Modified time: 2020-04-04 17:29:16
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

    def searchHref(self, dictCatlog, index):
        '''寻找节点内的文本
        dictCatlog = {sub:[{title: String, href: String_Url}....], 
                    main: {title: String, href: String_URL}
                }
        '''
        main, sub = dictCatlog["main"], dictCatlog["sub"]
        sublen = len(sub)
        
        if main:
            self.createFolder(main["title"])
        if sublen > 0:
            for item in sub:
                title, href = item["title"], item["href"]
                path_url = main["title"] + "/" + title
                filePath = self.createFolder(path_url)
                self.searchMainUrl(href, filePath)

    def createFolder(self, path_url):
        '''创建目录 title创建目录的名字  main是否有上级目录'''
        folderPath = curr_path + '/txt/' + path_url
        pathExsits = self.folderIsExit(folderPath)
        if not pathExsits:
            os.mkdir(folderPath)
        return folderPath
    def folderIsExit(self, path):
        '''判断目录是否存在'''
        return os.path.exists(path)

    def searchMainUrl(self, url, pathUrl):
        '''搜索作文的主入口'''
        domStr = 'div#left>div.nj_col>div.tc_l>div.tc_lis>div.tc_llist>ul.pt10>li>a[href]'
        session = HTMLSession()
        r = session.get(url, timeout = 10)
        html_node_list = r.html.find(domStr)
        for a_tag in html_node_list:
            title, href = self.fetchTitlandHref(a_tag)
            self.searchText(href, title, pathUrl)
            
    def searchText(self, url, title, path_url):
        '''
            寻找文章的主函数喽
            url 文章的网址
            title 文章的名字
            path_url 文章要存储的文职
        '''
        domStr = 'div.content>div[style="padding-left:11px;"]>p'
        session = HTMLSession()
        r = session.get(url, timeout = 10)
        p_node_list = r.html.find(domStr)
        pageTxt = ""
        for node in p_node_list:
            pageTxt += node.text
        filePath = path_url + "/" + title + '.txt'
        self.writeTxtFile(pageTxt, filePath)

    def writeTxtFile(self, txt, filePath):
        '''把txt文本写入文件中'''
        with open(filePath, 'w') as f:
            f.write(txt)







































if __name__ == "__main__":
    result = Search()
    print(result.searchFn())