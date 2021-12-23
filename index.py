# -*- coding: utf8 -*-

from des import *
from config import *
from Parser import *
from urllib import parse
from bs4 import BeautifulSoup
import logging, json, random, re, os, time, requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler输出到文件
fh = logging.FileHandler('log.txt', encoding='utf-8')
fh.setFormatter(formatter)

# 使用StreamHandler输出到控制台
sh = logging.StreamHandler()
sh.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)


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
        self.boundFields = "fieldSTQKzdjgmc,fieldSTQKjtcyglkssj,fieldCXXXsftjhb,fieldJCDDqmsjtdd,fieldYQJLksjcsj," \
                           "fieldSTQKjtcyzd,fieldJBXXjgsjtdz,fieldSTQKbrstzk,fieldSTQKfrtw,fieldSTQKjtcyqt," \
                           "fieldCXXXjtfslc,fieldJBXXlxfs,fieldSTQKxgqksm,fieldSTQKpcsj,fieldJKMsfwlm,fieldJKHDDzt," \
                           "fieldYQJLsfjcqtbl,fieldYQJLzhycjcsj,fieldSTQKfl,fieldSTQKhxkn,fieldJBXXbz,fieldCXXXsfylk," \
                           "fieldFLid,fieldjgs,fieldSTQKglfs,fieldCXXXsfjcgyshqzbl,fieldSTQKjtcyfx," \
                           "fieldCXXXszsqsfyyshqzbl,fieldJCDDshi,fieldSTQKrytsqkqsm,fieldJCDDs,fieldSTQKjtcyfs," \
                           "fieldSTQKjtcyzljgmc,fieldSQSJ,fieldJZDZC,fieldJBXXnj,fieldSTQKjtcyzdkssj,fieldSTQKfx," \
                           "fieldSTQKfs,fieldYQJLjcdry,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldYQJLjcddshi," \
                           "fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldHQRQ,fieldSTQKjtcyqtms,fieldCXXXksjcsj," \
                           "fieldSTQKzdkssj,fieldSTQKfxx,fieldSTQKjtcyzysj,fieldjgshi,fieldSTQKjtcyxm,fieldJBXXsheng," \
                           "fieldZJYCHSJCYXJGRQzd,fieldJBXXdrsfwc,fieldqjymsjtqk,fieldJBXXdw,fieldCXXXjcdr," \
                           "fieldCXXXsftjhbjtdz,fieldJCDDq,fieldSFJZYM,fieldSTQKjtcyclfs,fieldSTQKxm,fieldCXXXjtgjbc," \
                           "fieldSTQKjtcygldd,fieldSTQKjtcyzdjgmcc,fieldSTQKzd,fieldSTQKqt,fieldCXXXlksj," \
                           "fieldSTQKjtcyfrsj,fieldCXXXjtfsqtms,fieldSTQKjtcyzdmc,fieldCXXXjtfsfj,fieldJBXXfdy," \
                           "fieldSTQKjtcyjmy,fieldJBXXxm,fieldJKMjt,fieldSTQKzljgmc,fieldCXXXzhycjcsj," \
                           "fieldCXXXsftjhbq,fieldSTQKqtms,fieldYCFDY,fieldJBXXxb,fieldSTQKglkssj,fieldCXXXjtfspc," \
                           "fieldSTQKbrstzk1,fieldYCBJ,fieldCXXXssh,fieldSTQKzysj,fieldLYYZM,fieldJBXXgh,fieldCNS," \
                           "fieldCXXXfxxq,fieldSTQKclfs,fieldSTQKqtqksm,fieldCXXXqjymsxgqk,fieldYCBZ,fieldSTQKjmy," \
                           "fieldSTQKjtcyxjwjjt,fieldJBXXxnjzbgdz,fieldSTQKjtcyfl,fieldSTQKjtcyzdjgmc,fieldCXXXddsj," \
                           "fieldSTQKfrsj,fieldSTQKgldd,fieldCXXXfxcfsj,fieldJBXXbj,fieldSTQKjtcyfxx,fieldSTQKks," \
                           "fieldJBXXcsny,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldJBXXshi," \
                           "fieldSTQKjtcyfrtw,fieldSTQKjtcystzk1,fieldCXXXjcdqk,fieldSTQKzdmc,fieldSTQKjtcyks," \
                           "fieldSTQKjtcystzk,fieldCXXXjtfshc,fieldCXXXcqwdq,fieldSTQKxjwjjt,fieldSTQKjtcypcsj," \
                           "fieldJBXXqu,fieldSTQKlt,fieldJBXXjgshi,fieldYQJLjcddq,fieldYQJLjcdryjkqk,fieldYQJLjcdds," \
                           "fieldSTQKjtcyhxkn,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs," \
                           "fieldSTQKjtcylt,fieldSTQKzdjgmcc,fieldJBXXqjtxxqk,fieldDQSJ,fieldSTQKjtcyglfs "
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
        logger.info('账号登录')
        res = self.client.get(url="http://yq.gzhu.edu.cn/")
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
        res = self.client.post(url=login_post_url, data=post_data)
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
        if soup.title.string != '广州大学':
            raise RuntimeError('账号或密码错误')

    # 准备数据
    def prepare(self):
        logger.info("准备数据")
        res = self.client.get(url="https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true")
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
        self.csrfToken = soup.find(attrs={"itemscope": "csrfToken"})['content']
        self.formStepId = re.findall(r"\d+", res.url)[0]
        self.formUrl = res.url
        # 温馨提示
        if self.formStepId == '1':
            self.workflowId = re.findall(r"workflowId = \"(.*?)\"", res.content.decode('utf-8'))[0]
            url = "https://yqtb.gzhu.edu.cn/infoplus/interface/preview"
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
                'Origin': 'https://yqtb.gzhu.edu.cn',
                'Referer': 'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
                'Connection': 'close'
            }

            res = self.client.post(url, headers=headers, data=payload)
            formData = Parser2(res.json()).get()

            url = "https://yqtb.gzhu.edu.cn/infoplus/interface/start"
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
                'Origin': 'https://yqtb.gzhu.edu.cn',
                'Referer': 'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start?back=1&x_posted=true',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
                'Connection': 'close'
            }
            res = self.client.post(url, headers=headers, data=payload).json()
            if res['errno']:
                raise RuntimeError('system error')
            else:
                self.formStepId = re.findall(r"\d+", res['entities'][0])[0]
                self.formUrl = "https://yqtb.gzhu.edu.cn/infoplus/form/{}/render?back=2".format(self.formStepId)
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
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://yqtb.gzhu.edu.cn',
            'Referer': self.formUrl,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
            'Connection': 'close'
        }
        res = self.client.post(url="https://yqtb.gzhu.edu.cn/infoplus/interface/render", headers=headers, data=post_data)
        self.getDatas = res.json()

    # 开始执行打卡
    def start(self):
        logger.info("开始打卡")
        formData = Parser1(self.getDatas).get(),
        formData[0]["_VAR_URL"] = self.formUrl
        formData[0]['_VAR_ENTRY_NAME'] = '学生健康状况申报_'
        formData[0]['_VAR_ENTRY_TAGS'] = '疫情应用,移动端'
        headers = {
            'Host': 'yqtb.gzhu.edu.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://yqtb.gzhu.edu.cn',
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
            'rand': random.uniform(300, 500),
            'boundFields': self.boundFields,
            'csrfToken': self.csrfToken,
            'lang': 'zh'
        }
        post_data2 = {
            'stepId': self.formStepId,
            'actionId': 1,
            'formData': json.dumps(formData[0]),
            'timestamp': int(time.time()),
            'rand': random.uniform(300, 500),
            'boundFields': self.boundFields,
            'csrfToken': self.csrfToken,
            'lang': 'zh',
            'nextUsers': '{}',
            'remark': ''
        }
        res1 = self.client.post(url='https://yqtb.gzhu.edu.cn/infoplus/interface/listNextStepsUsers', headers=headers,
                                data=post_data1)
        res2 = self.client.post(url='https://yqtb.gzhu.edu.cn/infoplus/interface/doAction', headers=headers,
                                data=post_data2)
        if res1.json()['errno'] or res2.json()['errno']:
            raise RuntimeError('打卡失败')
        else:
            logger.info('打卡成功')

    # 开始运行
    def run(self):
        self.login()
        self.prepare()
        self.start()


# 消息推送
def pushNotify():
    pushToken = (PUSH_PLUS_TOKEN if PUSH_PLUS_TOKEN else os.getenv('PUSH_PLUS_TOKEN'))
    with open("log.txt", "r") as f:
        msg = f.read()
    os.remove("log.txt")
    if not pushToken:
        return logger.info('【Push+】PUSH_PLUS_TOKEN 未配置')
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": pushToken,
        "title": '健康打卡',
        "content": msg
    }
    response = requests.post(url, data=data).json()
    if response['code'] == 200:
        logger.info('【Push+】发送通知消息成功')
    elif response['code'] == 600:
        logger.warning('【Push+】PUSH_PLUS_TOKEN 错误')
    else:
        logger.warning('【Push+】发送通知调用API失败！！')


# 云函数
def main_handler(event, context):
    username = (USERNAME if USERNAME else os.getenv('USERNAME'))
    password = (PASSWORD if PASSWORD else os.getenv('PASSWORD'))
    if not username or not password:
        raise RuntimeError("无法获取学号和密码")

    for _ in range(RETRY):
        try:
            YQTB(username, password).run()
            break
        except Exception as e:
            logger.warning(e)
    pushNotify()


# 本地测试
if __name__ == '__main__':
    username = (USERNAME if USERNAME else os.getenv('USERNAME'))
    password = (PASSWORD if PASSWORD else os.getenv('PASSWORD'))
    if not username or not password:
        raise RuntimeError("无法获取学号和密码")

    for _ in range(RETRY):
        try:
            YQTB(username, password).run()
            break
        except Exception as e:
            logger.warning(e)
    pushNotify()
