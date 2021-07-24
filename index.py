# -*- coding: utf8 -*-

from des import *
import base64
import json
import random
import re
import os
import time
from urllib import parse
import requests
from bs4 import BeautifulSoup
from Parser import Parser1, Parser2

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class YQTB:
    # 初始化参数
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.csrfToken = ''
        self.formStepId = ''
        self.formUrl = ''
        self.workflowId = ''
        self.client = requests.session()
        self.boundFields = "fieldSTQKzdjgmc,fieldSTQKjtcyglkssj,fieldCXXXsftjhb,fieldzgzjzdzjtdz,fieldJCDDqmsjtdd," \
                           "fieldSHENGYC,fieldYQJLksjcsj,fieldSTQKjtcyzd,fieldJBXXjgsjtdz,fieldSTQKbrstzk," \
                           "fieldSTQKfrtw,fieldSTQKjtcyqt,fieldCXXXjtfslc,fieldJBXXlxfs,fieldSTQKpcsj,fieldJKHDDzt," \
                           "fieldYQJLsfjcqtbl,fieldYQJLzhycjcsj,fieldSTQKfl,fieldSTQKhxkn,fieldJBXXbz,fieldCXXXsfylk," \
                           "fieldFLid,fieldjgs,fieldSTQKglfs,fieldCXXXsfjcgyshqzbl,fieldSTQKjtcyfx," \
                           "fieldCXXXszsqsfyyshqzbl,fieldJCDDshi,fieldSTQKrytsqkqsm,fieldJCDDs,fieldSTQKjtcyfs," \
                           "fieldSTQKjtcyzljgmc,fieldSQSJ,fieldzgzjzdzs,fieldzgzjzdzq,fieldJBXXnj," \
                           "fieldSTQKjtcyzdkssj,fieldSTQKfx,fieldSTQKfs,fieldYQJLjcdry,fieldCXXXjtfsdb,fieldCXXXcxzt," \
                           "fieldYQJLjcddshi,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldHQRQ,fieldSTQKjtcyqtms," \
                           "fieldCXXXksjcsj,fieldSTQKzdkssj,fieldSTQKjtcyzysj,fieldjgshi,fieldSTQKjtcyxm," \
                           "fieldJBXXsheng,fieldJBXXdrsfwc,fieldqjymsjtqk,fieldJBXXdw,fieldCXXXjcdr," \
                           "fieldCXXXsftjhbjtdz,fieldJCDDq,fieldSTQKjtcyclfs,fieldSTQKxm,fieldCXXXjtgjbc," \
                           "fieldSTQKjtcygldd,fieldzgzjzdzshi,fieldSTQKjtcyzdjgmcc,fieldSTQKzd,fieldSTQKqt," \
                           "fieldCXXXlksj,fieldSTQKjtcyfrsj,fieldCXXXjtfsqtms,fieldSTQKjtcyzdmc,fieldCXXXjtfsfj," \
                           "fieldJBXXfdy,fieldJBXXxm,fieldSTQKzljgmc,fieldCXXXzhycjcsj,fieldCXXXsftjhbq," \
                           "fieldSTQKqtms,fieldYCFDY,fieldJBXXxb,fieldSTQKglkssj,fieldCXXXjtfspc,fieldSTQKbrstzk1," \
                           "fieldYCBJ,fieldCXXXssh,fieldSTQKzysj,fieldJBXXgh,fieldCNS,fieldCXXXfxxq,fieldSTQKclfs," \
                           "fieldSTQKqtqksm,fieldCXXXqjymsxgqk,fieldYCBZ,fieldJBXXxnjzbgdz,fieldSTQKjtcyfl," \
                           "fieldSTQKjtcyzdjgmc,fieldCXXXddsj,fieldSTQKfrsj,fieldSTQKgldd,fieldCXXXfxcfsj," \
                           "fieldJBXXbj,fieldSTQKks,fieldJBXXcsny,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd," \
                           "fieldCXXXjtzzs,fieldJBXXshi,fieldSTQKjtcyfrtw,fieldSTQKjtcystzk1,fieldCXXXjcdqk," \
                           "fieldSTQKzdmc,fieldSTQKjtcyks,fieldSTQKjtcystzk,fieldCXXXjtfshc,fieldCXXXcqwdq," \
                           "fieldSTQKjtcypcsj,fieldJBXXqu,fieldJBXXjgshi,fieldYQJLjcddq,fieldYQJLjcdryjkqk," \
                           "fieldYQJLjcdds,fieldSTQKjtcyhxkn,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs," \
                           "fieldSTQKzdjgmcc,fieldJBXXqjtxxqk,fieldDQSJ,fieldSTQKjtcyglfs," \
                           "fieldJCSJ,fieldYZNSFJCHS,fieldJKMsfwlm,fieldLYYZM"
        self.client.headers = {
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
        }

    # 登陆账号
    def login(self):
        logger.info('开始登陆')
        res = self.client.get(url="http://yqtb.gzhu.edu.cn/")
        soup = BeautifulSoup(res.text, "html.parser")
        lt = soup.find("input", attrs={"name": "lt"})['value']
        execution = soup.find("input", attrs={"name": "execution"})['value']
        post_url = soup.find('form')['action']

        login_post_url = parse.urljoin(res.url, post_url)
        post_data = {
            'rsa': strenc("{}{}{}".format(self.username, self.password, lt), '1', '2', '3'),
            'ul': len(self.username),
            'pl': len(self.password),
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit'
        }
        print(post_data)

        res = self.client.post(url=login_post_url, data=post_data)
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

        if soup.title.string != '广州大学':
            # 账号或密码错误
            msg = soup.select('#msg')[0].text
            if msg == '账号或密码错误':
                logger.warning('账号或密码错误')
                return False
            logger.warning('验证码错误，尝试重新登陆')
            self.login()
        logger.info('登陆成功')
        return True

    # 准备数据
    def prepare(self):
        logger.info("准备数据")
        res = self.client.get(url="http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true")
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
        self.csrfToken = soup.find(attrs={"itemscope": "csrfToken"})['content']
        self.formStepId = re.findall(r"\d+", res.url)[0]
        self.formUrl = res.url
        # 温馨提示
        if self.formStepId == '1':
            self.workflowId = re.findall(r"workflowId = \"(.*?)\"", res.content.decode('utf-8'))[0]
            url = "http://yqtb.gzhu.edu.cn/infoplus/interface/preview"
            payload = {
                'workflowId': self.workflowId,
                'rand': random.uniform(300, 400),
                'width': 1440,
                'csrfToken': self.csrfToken
            }
            headers = {
                'Host': 'yqtb.gzhu.edu.cn',
                'Content-Length': '123',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://yqtb.gzhu.edu.cn',
                'Referer': 'http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
                'Connection': 'close'
            }

            res = self.client.post(url, headers=headers, data=payload)
            formData = Parser2(res.json()).get()

            url = "http://yqtb.gzhu.edu.cn/infoplus/interface/start"
            payload = {
                'idc': 'XNYQSB',
                'release': '',
                'admin': 'false',
                'formData': json.dumps(formData),
                'lang': 'cn',
                'csrfToken': self.csrfToken
            }
            headers = {
                'Host': 'yqtb.gzhu.edu.cn',
                'Content-Length': '4202',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://yqtb.gzhu.edu.cn',
                'Referer': 'http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
                'Connection': 'close'
            }

            res = self.client.post(url, headers=headers, data=payload).json()
            if res['errno']:
                self.notify('system error')
                return False
            else:
                self.formStepId = re.findall(r"\d+", res['entities'][0])[0]

        post_data = {
            'stepId': self.formStepId,
            'instanceId': '',
            'admin': 'false',
            'rand': random.uniform(300, 400),
            'width': 1440,
            'lang': 'zh',
            'csrfToken': self.csrfToken
        }
        headers = {
            'Host': 'yqtb.gzhu.edu.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://yqtb.gzhu.edu.cn',
            'Referer': self.formUrl,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
            'Connection': 'close'
        }
        res = self.client.post(url="http://yqtb.gzhu.edu.cn/infoplus/interface/render", headers=headers, data=post_data)
        self.getDatas = res.json()
        return True

    # 开始执行打卡
    def start(self):
        logger.info("执行打卡")
        formData = Parser1(self.getDatas).get(),

        headers = {
            'Host': 'yqtb.gzhu.edu.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://yqtb.gzhu.edu.cn',
            'Referer': self.formUrl,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
            'Connection': 'close'
        }
        post_data1 = {
            'stepId': self.formStepId,
            'actionId': 1,
            'formData': json.dumps(formData[0]),
            'timestamp': int(time.time()),
            'rand': random.uniform(700, 800),
            'boundFields': self.boundFields,
            'csrfToken': self.csrfToken,
            'lang': 'zh'
        }

        post_data2 = {
            'stepId': self.formStepId,
            'actionId': 1,
            'formData': json.dumps(formData[0]),
            'nextUsers': "{}",
            'timestamp': int(time.time()),
            'rand': random.uniform(700, 800),
            'boundFields': self.boundFields,
            'csrfToken': self.csrfToken,
            'lang': 'zh'
        }

        res1 = self.client.post(url='http://yqtb.gzhu.edu.cn/infoplus/interface/listNextStepsUsers', headers=headers,
                                data=post_data1)
        res2 = self.client.post(url='http://yqtb.gzhu.edu.cn/infoplus/interface/doAction', headers=headers,
                                data=post_data2)

        if res1.json()['errno'] or res2.json()['errno']:
            return False
        return True

    # 消息推送
    def notify(self, msg):
        print(msg)

    # 开始运行
    def run(self):
        logger.info('开始执行任务')
        res = self.login()
        if res:
            res2 = self.prepare()
            if res2:
                res3 = self.start()
                if res3:
                    self.notify('打卡成功')
                else:
                    self.notify('打卡失败')
            else:
                self.notify('系统错误')
        else:
            self.notify('账号或密码错误')

        logger.info('任务执行完毕')


# 云函数
def main_handler(event, context):
    logger.info('got event{}'.format(event))
    username = os.getenv('USERNAME')  # 学号
    password = os.getenv('PASSWORD')  # 密码
    YQTB(username, password).run()


# 本地测试
if __name__ == '__main__':
    username = 'XXX'  # 学号
    password = 'XXX'  # 密码
    YQTB(username, password).run()
