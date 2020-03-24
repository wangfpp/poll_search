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
        session = HTMLSession()
        r  = session.get(self.baseUrl, timeout = 10)
        navBar = r.html.find('div.spec.clearfix>dl>dd>a[href]')
        url_list = []
        length = len(navBar)
        for index in range(1, length):
            element = navBar[index]
            absolute_link = list(element.absolute_links)[0]
            url_list.append(absolute_link)
        return url_list

    def searchTxt(self, url, index):
        print('task {}     start'.format(index))
        time.sleep(random.random())
        print('task {}     end'.format(index))


if __name__ == "__main__":
    result = Search()
    print(result.searchFn())