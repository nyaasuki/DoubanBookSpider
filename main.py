import csv
import time
from cmd import Cmd

from DoubanSpider.db import Douban, Recording
from DoubanSpider.Spider import DoubanBook


class SpiderMain(Cmd):
    intro = '豆瓣图书爬虫V2.0 ---------- 输入help获取帮助。'

    def __init__(self):
        super().__init__()
        pass

    def do_help(self, arg):
        print('[Help] start  - 开始爬取任务，默认从上次结束的地方开始')
        print('[Help] tag TAG - 添加/爬取 标签下的书籍，TAG是你需要添加的标签')
        print('[Help] tag all - 爬取所有标签下的书籍')
        print('[Help] quit  - 退出程序')


    def do_start(self, arg):
        for row in url_pool():
            douban.get_data(row)
        print('爬取结束！')

    def do_tag(self, arg):
        if arg == "all":
            print("[WAR]请注意，在没有代理池的情况下，此操作通常无法完成！")
            douban.get_tags()
            print('[Spider]标签下所有书籍信息爬取完成！请输入start开始抓取数据！')
        else:
            print(f"[Spider]开始获取{arg}标签下的所有书籍，这需要一定时间！")
            douban.get_url(arg)
            print('[Spider]标签下所有书籍信息爬取完成！请输入start开始抓取数据！')

    def do_quit(self, arg):
        exit()

    def main(self):
        self.cmdloop()


def url_pool():
    if not n:
        print('[Spider]你需要先获取tag数据!')
    else:
        for row in douban.session.query(Douban.url, Douban.tag, Douban.id).all():
            ago = douban.session.query(Recording.data).first()
            if row[2] > ago[0]:
                yield row


if __name__ == '__main__':
    with open("results.csv", "a", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        writer.writerow(["书名", "作者", "上市时间", "价格", "评分", "书籍分类", "内容简介"])
    spider = SpiderMain()
    douban = DoubanBook()
    rec = douban.session.query(Recording.id).all()
    if not rec:
        douban.session.add(Recording(id=1, data=0))
        douban.session.commit()
    n = douban.session.query(Douban.url, Douban.tag).all()
    if not n:
        print('未检测到任何数据，请使用 tag 关键字获取标签数据，输入help获取帮助。')
    else:
        print('检测到现有TAG数据，输入start直接开始抓取...')
    spider.main()
