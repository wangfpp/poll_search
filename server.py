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
        navBar = r.html.find('div.mainnav>ul.nav.clearfix>li')
        url_list = []
        length = len(navBar)
        for index in range(1, length):
            catlogDict = {};
            element = navBar[index]
            a_node = element.find('a[href]', first=True)
            main_title, main_href = self.fetchTitlandHref(a_node)

            sub_node = element.find('div.sub_nav>a', first=False)
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
        title, href = element.text, list(element.absolute_links)[0]
        return title, href
    def searchTxt(self, url, index):
        print('task {}     start'.format(index))
        time.sleep(random.random())
        print('task {}     end'.format(index))


if __name__ == "__main__":
    result = Search()
    print(result.searchFn())