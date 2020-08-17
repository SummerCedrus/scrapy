import scrapy
import json
from ..items import UserRelationItem
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class WeiBoSpider(scrapy.spiders.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    uid = 3623353053

    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'

    # weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'

    # follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'

    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'

    def start_requests(self):
        url = self.user_url.format(uid=self.uid)

        # debug('\033[0;36m {url} \033[0m'.format(url=url))
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        res = json.loads(response.text)

        user_info = res.get('data').get('userInfo')
        # user_item = UserItem()
        # user_item['fans_count'] = user_info.get('followers_count')
        # user_item['follows_count'] = user_info.get('follow_count')
        # debug('\033[0;36m {body} \033[0m'.format(body=user_info.get('id')))
        url = self.fan_url.format(uid=self.uid, page=1)
        debug("Begin Crawling {name}".format(name=user_info.get("id")))
        yield scrapy.Request(url=url, callback=self.parse_fan, meta={'since_id':1})

    def parse_fan(self, response):
        item = UserRelationItem()
        res = json.loads(response.text)
        fans = res.get('data').get('cards')[-1].get('card_group')
        for fan in fans:
            item['id'] = fan.get('user').get('id')
            item['name'] = fan.get('user').get('screen_name')
            item['follow_count'] = fan.get('user').get('follow_count')
            item['followers_count'] = fan.get('user').get('followers_count')
            # debug("Fan {id} {name} {followcnt} {followerscnt}".format(id=item['id'],name=item['name'], followcnt=item['follow_count'],
            #                                                      followerscnt=item['followers_count']))
            yield item
        new_page = response.meta.get('since_id') + 1
        url = self.fan_url.format(uid=self.uid, page=new_page)
        yield scrapy.Request(url=url, callback=self.parse_fan, meta={'since_id':new_page})

def debug(param):
    print('\033[0;36m {param} \033[0m'.format(param=param))
