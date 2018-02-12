# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import imgtest
import cxkd
import urllib
import json
import photo
import requests
from lxml import etree

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr = data.echostr
        #自己的token
        token="Wll580411" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if msgType == 'text':
            content = xml.find("Content").text
            if content[0:4] == u"力力密码":

                reply_content = '''xxx'''
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)
            if content[0:4] == u"妈妈密码":

                reply_content = '''xxx'''
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)

            if content[0:2] == u"汇率":
                url_dic = {}
                try:
                    for w in ['HKD', 'USD', 'EUR', 'JPY']:
                        r = requests.get("https://api.fixer.io/latest?base=CNY")
                        url_dic[w] = round(100 / r.json()['rates'][w], 3)
                    res = u'''100港币兑换{}人民币
100美元兑换{}人民币
100欧元兑换{}人民币
100日元兑换{}人民币'''.format(url_dic['HKD'], url_dic['USD'], url_dic['EUR'], url_dic['JPY'])
                    return self.render.reply_text(fromUser, toUser, int(time.time()), res)
                except Exception, e:

                    return self.render.reply_text(fromUser, toUser, int(time.time()), str(e))
            if content[0:2] == u"快递":
                post = str(content[2:])
                kuaidi = cxkd.detect_com(post)
                return self.render.reply_text(fromUser, toUser, int(time.time()), kuaidi)
            else:
                key = 'd6f7efeccc3e43338b0517971bc0833d'  ###图灵机器人的key
                api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
                info = content[0:].encode('UTF-8')
                url = api + info
                page = urllib.urlopen(url)
                html = page.read()
                dic_json = json.loads(html)
                reply_content = dic_json['text']
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)
        elif msgType == 'image':
            try:
                picurl = xml.find('PicUrl').text
                datas = photo.get_info(picurl)
                if datas:
                    data = json.loads(datas)
                    i = 1
                    res = ''
                    for w in data['faces']:
                        res += u'图中右起第{}个为{}性，年龄为{}，颜值分数为{}！'.format(str(i), w['attributes']['gender']['value'].replace(
                            u'Female', u'女').replace(u'Male', u'男'), w['attributes']['age']['value'],
                                                                    str(max(w['attributes']['beauty'].values())))
                        i += 1
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), u'识别失败，换张图片试试吧')
                return self.render.reply_text(fromUser, toUser, int(time.time()), res)
            except Exception, e:
                #return self.render.reply_text(fromUser, toUser, int(time.time()), '识别失败，换张图片试试吧')
                return self.render.reply_text(fromUser, toUser, int(time.time()), str(e))
        else:
            pass