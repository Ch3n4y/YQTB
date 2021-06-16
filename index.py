# -*- coding: utf8 -*-

import base64
import json
import random
import re
import os
import sys
import time
from urllib import parse
import requests
from bs4 import BeautifulSoup
from Parser import Parser1, Parser2
from aip import AipOcr
from requests.adapters import HTTPAdapter

import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler输出到文件
fh = logging.FileHandler('log.txt', encoding='utf-8')
fh.setFormatter(formatter)

# 使用StreamHandler输出到控制台
sh = logging.StreamHandler()
sh.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)

# 连接超时时间
TIMEOUT = 10
# 登录失败时重试的次数
RETRY = 10
# 每次连接的间隔
RETRY_INTERVAL = 10


class YQTB:
    # 初始化参数
    def __init__(self):
        try:
            self.USERNAME = os.environ['USERNAME']  # 学号
            self.PASSWORD = os.environ['PASSWORD']  # 密码
        except Exception as e:
            logger.warning(e)
            logger.warning('无法获取学号和密码，程序终止')
            sys.exit(1)
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

    # 识别验证码
    def defaultOcr(self, image):
        image = base64.encodebytes(image)
        url = "https://api2.chaney.top/release/gzhu"
        payload = {
            'key': 'b42fb9486f3c10e8654072f0648e694f',
            'image': image,
        }
        response = requests.post(url, data=payload, timeout=TIMEOUT).json()
        return response['result']

    # 百度OCR识别验证码
    def ocr(self, image):
        try:
            self.APP_ID = os.environ['APP_ID']
            self.API_KEY = os.environ['API_KEY']
            self.SECRET_KEY = os.environ['SECRET_KEY']
        except:
            logger.info('未配置百度OCR，采用默认验证码识别')
            return self.defaultOcr(image)

        aipClient = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)  # 创建连接
        res = aipClient.numbers(image, options=None)
        vcode = ""
        for tex in res["words_result"]:  # 遍历结果
            vcode += tex["words"]
        return vcode  # 输出内容

    # 获取验证码
    def captcha(self):
        logger.info('验证码识别')
        image = self.client.get(
            url='https://cas.gzhu.edu.cn/cas_server/captcha.jsp', timeout=TIMEOUT)
        return self.ocr(image.content)

    # 登陆账号
    def login(self):
        logger.info('开始登陆')
        res = self.client.get(url="http://yqtb.gzhu.edu.cn/", timeout=TIMEOUT)
        soup = BeautifulSoup(res.text, "html.parser")
        form = soup.find_all('input')
        post_url = soup.find('form')['action']
        post_data = {}
        for row in form:
            post_data[row['name']] = row['value']
        del post_data['reset']
        login_post_url = parse.urljoin(res.url, post_url)

        post_data['username'] = self.USERNAME
        post_data['password'] = self.PASSWORD
        post_data['captcha'] = self.captcha()
        res = self.client.post(url=login_post_url, data=post_data)
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

        if soup.title.string != '广州大学':
            # 账号或密码错误
            msg = soup.select('#msg')[0].text
            if msg == '账号或密码错误':
                logger.warning('账号或密码错误，程序终止')
                self.notify('打卡失败——账号或密码错误')
                # 直接退出程序
                sys.exit(1)
            logger.warning('验证码错误，尝试重新登陆')
            return False
        logger.info('登陆成功')
        return True

    # 准备数据
    def prepare(self):
        logger.info("准备数据")
        res = self.client.get(
            url="http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true", timeout=TIMEOUT)
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
        res = self.client.post(
            url="http://yqtb.gzhu.edu.cn/infoplus/interface/render", headers=headers, data=post_data)
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
        try:
            self.SCKEY = os.environ['SCKEY']
            self.serverNotify(msg)
        except KeyError:
            logger.info('您未提供server酱的SCKEY，取消微信推送消息通知')
        try:
            self.PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
            self.pushNotify(msg)
        except KeyError:
            logger.info('您未提供push+的PUSH_PLUS_TOKEN，取消push+推送消息通知')

    def pushNotify(self, msg):
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": self.PUSH_PLUS_TOKEN,
            "title": '健康打卡',
            "content": msg
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = json.dumps(requests.post(
            url, data=body, headers=headers).json(), ensure_ascii=False)
        datas = json.loads(response)
        if datas['code'] == 200:
            logger.info('push+发送通知消息成功')
        if datas['code'] == 600:
            logger.warning('PUSH_PLUS_TOKEN 错误')
        else:
            logger.warning('push+发送通知调用API失败！！')

    def serverNotify(self, msg):
        url = 'https://sctapi.ftqq.com/' + self.SCKEY + '.send'
        data = {
            'text': msg,
        }
        response = json.dumps(requests.post(
            url, data).json(), ensure_ascii=False)
        datas = json.loads(response)
        if datas['code'] == 0:
            logger.info('server酱发送通知消息成功')
        elif datas['code'] == 40001:
            logger.warning('PUSH_KEY 错误')
        else:
            logger.warning('发送通知调用API失败！！')

    # 开始运行
    def run(self):
        logger.info('开始执行任务')
        res = False
        # 登录失败则重试
        for _ in range(RETRY):
            try:
                res = self.login()
            except Exception as e:
                logger.warning(e)
                time.sleep(RETRY_INTERVAL)
                continue
            if res:
                break
        if res:
            res2 = self.prepare()
            if res2:
                res3 = self.start()
                if res3:
                    self.notify('打卡成功')
                else:
                    self.notify('打卡失败')
                    logger.warning('打卡失败')
                    sys.exit(1)
            else:
                logger.warning('系统错误，程序终止')
                self.notify('系统错误')
                sys.exit(1)
        else:
            logger.warning('登录失败，程序终止')
            self.notify('账号或密码错误')
            sys.exit(1)

        logger.info('任务执行完毕')


# 云函数
def main_handler(event, context):
    logger.info('got event{}'.format(event))
    username = os.getenv('USERNAME')  # 学号
    password = os.getenv('PASSWORD')  # 密码
    YQTB(username, password).run()


# 本地测试
if __name__ == '__main__':
    YQTB().run()
