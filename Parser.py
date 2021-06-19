# 解析数据，生成提交formData
class Parser1:
    def __init__(self, data):
        self.item_keys = {'_VAR_EXECUTE_INDEP_ORGANIZE_Name': None, '_VAR_ACTION_INDEP_ORGANIZES_Codes': None,
                          '_VAR_ACTION_REALNAME': None, '_VAR_ACTION_ORGANIZE': None, '_VAR_EXECUTE_ORGANIZE': None,
                          '_VAR_ACTION_INDEP_ORGANIZE': None, '_VAR_ACTION_INDEP_ORGANIZE_Name': None,
                          '_VAR_ACTION_ORGANIZE_Name': None, '_VAR_EXECUTE_ORGANIZES_Names': None,
                          '_VAR_OWNER_ORGANIZES_Codes': None, '_VAR_ADDR': None, '_VAR_OWNER_ORGANIZES_Names': None,
                          '_VAR_URL': None, '_VAR_EXECUTE_ORGANIZE_Name': None, '_VAR_RELEASE': None,
                          '_VAR_NOW_MONTH': None,
                          '_VAR_ACTION_USERCODES': None, '_VAR_ACTION_ACCOUNT': None,
                          '_VAR_ACTION_INDEP_ORGANIZES_Names': None,
                          '_VAR_OWNER_ACCOUNT': None, '_VAR_ACTION_ORGANIZES_Names': None, '_VAR_STEP_CODE': None,
                          '_VAR_OWNER_USERCODES': None, '_VAR_EXECUTE_ORGANIZES_Codes': None, '_VAR_NOW_DAY': None,
                          '_VAR_OWNER_REALNAME': None, '_VAR_NOW': None, '_VAR_URL_Attr': None,
                          '_VAR_ENTRY_NUMBER': None,
                          '_VAR_EXECUTE_INDEP_ORGANIZES_Names': None, '_VAR_STEP_NUMBER': None, '_VAR_POSITIONS': None,
                          '_VAR_EXECUTE_INDEP_ORGANIZES_Codes': None, '_VAR_EXECUTE_POSITIONS': None,
                          '_VAR_ACTION_ORGANIZES_Codes': None, '_VAR_EXECUTE_INDEP_ORGANIZE': None,
                          '_VAR_NOW_YEAR': None,
                          'fieldFLid': None, 'fieldHQRQ': None, 'fieldDQSJ': None, 'fieldSQSJ': None,
                          'fieldJBXXxm': None,
                          'fieldJBXXxm_Name': None, 'fieldJBXXgh': None, 'fieldJBXXnj': None, 'fieldJBXXbj': None,
                          'fieldJBXXxb': None, 'fieldJBXXxb_Name': None, 'fieldJBXXlxfs': None, 'fieldJBXXcsny': None,
                          'fieldJBXXdw': None, 'fieldJBXXdw_Name': None, 'fieldJBXXbz': None, 'fieldJBXXbz_Name': None,
                          'fieldJBXXfdy': None, 'fieldJBXXfdy_Name': None, 'fieldjgs': None, 'fieldjgs_Name': None,
                          'fieldjgshi': None, 'fieldjgshi_Name': None, 'fieldJBXXxnjzbgdz': None, 'fieldJBXXJG': None,
                          'fieldJBXXjgs': None, 'fieldJBXXjgs_Name': None, 'fieldJBXXjgshi': None,
                          'fieldJBXXjgshi_Name': None,
                          'fieldJBXXjgq': None, 'fieldJBXXjgq_Name': None, 'fieldJBXXjgsjtdz': None,
                          'fieldJBXXdrsfwc': None,
                          'fieldJBXXsheng': None, 'fieldJBXXshi': None, 'fieldJBXXqu': None, 'fieldJBXXqjtxxqk': None,
                          'fieldSTQKbrstzk1': None, 'fieldSTQKfs': None, 'fieldSTQKks': None, 'fieldSTQKxm': None,
                          'fieldSTQKfl': None, 'fieldSTQKhxkn': None, 'fieldSTQKfx': None, 'fieldSTQKqt': None,
                          'fieldSTQKqtms': None, 'fieldSTQKfrtw': None, 'fieldSTQKfrsj': None, 'fieldSTQKclfs': None,
                          'fieldSTQKzd': None, 'fieldSTQKbrstzk': None, 'fieldSTQKglfs': None, 'fieldSTQKgldd': None,
                          'fieldSTQKglkssj': None, 'fieldSTQKzdjgmc': None, 'fieldSTQKzdmc': None,
                          'fieldSTQKzdkssj': None,
                          'fieldSTQKzljgmc': None, 'fieldSTQKzysj': None, 'fieldSTQKzdjgmcc': None,
                          'fieldSTQKpcsj': None,
                          'fieldSTQKjtcystzk1': None, 'fieldSTQKjtcyfs': None, 'fieldSTQKjtcyks': None,
                          'fieldSTQKjtcyxm': None,
                          'fieldSTQKjtcyfl': None, 'fieldSTQKjtcyhxkn': None, 'fieldSTQKjtcyfx': None,
                          'fieldSTQKjtcyqt': None,
                          'fieldSTQKjtcyqtms': None, 'fieldSTQKjtcyfrtw': None, 'fieldSTQKjtcyfrsj': None,
                          'fieldSTQKjtcyclfs': None,
                          'fieldSTQKjtcyzd': None, 'fieldSTQKjtcystzk': None, 'fieldSTQKjtcyglfs': None,
                          'fieldSTQKjtcygldd': None,
                          'fieldSTQKjtcyglkssj': None, 'fieldSTQKjtcyzdjgmc': None, 'fieldSTQKjtcyzdmc': None,
                          'fieldSTQKjtcyzdkssj': None, 'fieldSTQKjtcyzljgmc': None, 'fieldSTQKjtcyzysj': None,
                          'fieldSTQKjtcyzdjgmcc': None, 'fieldSTQKjtcypcsj': None, 'fieldSTQKrytsqkqsm': None,
                          'fieldCXXXszsqsfyyshqzbl': None, 'fieldCXXXqjymsxgqk': None, 'fieldCXXXsfjcgyshqzbl': None,
                          'fieldCXXXksjcsj': None, 'fieldCXXXzhycjcsj': None, 'fieldJCDDs': None, 'fieldJCDDshi': None,
                          'fieldJCDDq': None, 'fieldJCDDqmsjtdd': None, 'fieldCXXXjcdr': None, 'fieldCXXXjcdqk': None,
                          'fieldYQJLsfjcqtbl': None, 'fieldYQJLksjcsj': None, 'fieldYQJLzhycjcsj': None,
                          'fieldYQJLjcdry': None,
                          'fieldYQJLjcdds': None, 'fieldYQJLjcddshi': None, 'fieldYQJLjcddq': None,
                          'fieldYQJLjcdryjkqk': None,
                          'fieldqjymsjtqk': None, 'fieldCXXXsftjhb': None, 'fieldCXXXsftjhbjtdz': None,
                          'fieldCXXXsftjhbs': None,
                          'fieldCXXXsftjhbq': None, 'fieldCXXXddsj': None, 'fieldCXXXsfylk': None,
                          'fieldCXXXlksj': None,
                          'fieldJKHDDzt': None, 'fieldJKHDDzt_Name': None, 'fieldzgzjzdzq': None,
                          'fieldzgzjzdzjtdz': None, 'fieldzgzjzdzshi': None, 'fieldzgzjzdzs': None,
                          'fieldCXXXcxzt': None,
                          'fieldCXXXjtgjbc': None, 'fieldCXXXjtfsqtms': None, 'fieldCXXXjtfsqt': None,
                          'fieldCXXXjtfslc': None,
                          'fieldCXXXjtfspc': None, 'fieldCXXXjtfsdb': None, 'fieldCXXXjtfshc': None,
                          'fieldCXXXjtfsfj': None,
                          'fieldCXXXfxcfsj': None, 'fieldCXXXcqwdq': None, 'fieldCXXXdqszd': None, 'fieldCXXXssh': None,
                          'fieldCXXXfxxq': None, 'fieldCXXXjtjtzz': None, 'fieldCXXXjtzzq': None,
                          'fieldCXXXjtzzq_Name': None,
                          'fieldCXXXjtzzs': None, 'fieldCXXXjtzzs_Name': None, 'fieldCXXXjtzz': None,
                          'fieldCXXXjtzz_Name': None,
                          'fieldSTQKqtqksm': None, 'fieldSHENGYC': None, 'fieldYCFDY': None, 'fieldYCBZ': None,
                          'fieldYCBJ': None, 'fieldLYYZM': None,
                          }
        self.data = data

    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item
            elif isinstance(v, list):
                for row in v:
                    item = self._finditem(row, key)
                    if item is not None:
                        return item

    def getData(self):
        data = {}
        for k, v in self.item_keys.items():
            re = self._finditem(self.data, k)
            if re is not None:
                data[k] = re
            else:
                print("error", k)
        return data

    def get(self):
        post_data1 = self.getData()
        post_data2 = {
            'fieldJBXXbz_Attr': {"_parent": ""},
            'fieldJBXXfdy_Attr': {"_parent": "%s" % self.data['entities'][0]['data']['fieldYCFDY']},
            'fieldjgshi_Attr': {"_parent": "%s" % self.data['entities'][0]['data']['fieldjgs']},
            'fieldJBXXjgshi_Attr': {"_parent": "%s" % self.data['entities'][0]['data']['fieldJBXXjgs']},
            'fieldJBXXjgq_Attr': {"_parent": "%s" % self.data['entities'][0]['data']['fieldJBXXjgshi']},
            'fieldJBXXsheng_Name': '',
            'fieldJBXXshi_Name': '',
            'fieldJBXXshi_Attr': {"_parent": ""},
            'fieldJBXXqu_Name': '',
            'fieldJBXXqu_Attr': {"_parent": ""},
            'fieldJCDDs_Name': '',
            'fieldJCDDshi_Name': '',
            'fieldJCDDshi_Attr': {"_parent": ""},
            'fieldJCDDq_Name': '',
            'fieldJCDDq_Attr': {"_parent": ""},
            'fieldYQJLjcdds_Name': '',
            'fieldYQJLjcddshi_Name': '',
            'fieldYQJLjcddshi_Attr': {"_parent": ""},
            'fieldYQJLjcddq_Name': '',
            'fieldYQJLjcddq_Attr': {"_parent": ""},
            'fieldCXXXsftjhbjtdz_Name': '',
            'fieldCXXXsftjhbs_Name': '',
            'fieldCXXXsftjhbs_Attr': {"_parent": ""},
            'fieldCXXXsftjhbq_Name': '',
            'fieldCXXXsftjhbq_Attr': {"_parent": ""},
            'fieldzgzjzdzq_Name': '',
            'fieldzgzjzdzq_Attr': {"_parent": ""},
            'fieldzgzjzdzshi_Name': '',
            'fieldzgzjzdzshi_Attr': {"_parent": ""},
            'fieldzgzjzdzs_Name': '',
            'fieldCXXXfxxq_Name': '',
            '_VAR_ENTRY_NAME': '学生健康状况申报_',
            '_VAR_ENTRY_TAGS': '疫情应用,移动端',
            'fieldCNS': True,
            # 针对目前新设置的核酸检测，个人感觉会是临时的，到时候疫情过去这块直接删掉即可。
            'fieldJCSJ': '1623081600',  # 6月8日 核酸检测
            'fieldYZNSFJCHS': '2',  # 一周内是否做过核酸检测 1：是 2：否；若选择否，上面的日期也可不填写
            'fieldJKMsfwlm': '1',  # 健康码是否为绿码 1：是 2：否； 若选择否还需要上传健康码截图
        }
        post_data_info = dict(post_data1, **post_data2)
        return post_data_info


class Parser2:
    def __init__(self, data):
        self.item_keys = {'fieldCXY': None, '_VAR_ACTION_REALNAME': None, '_VAR_RELEASE': None, '_VAR_NOW_MONTH': None,
                          '_VAR_ACTION_USERCODES': None, '_VAR_ACTION_ACCOUNT': None,
                          '_VAR_ACTION_ORGANIZES_Names': None,
                          '_VAR_URL_Attr': None, '_VAR_POSITIONS': None, '_VAR_ACTION_ORGANIZES_Codes': None,
                          '_VAR_NOW_YEAR': None,
                          '_VAR_ACTION_INDEP_ORGANIZES_Codes': None, '_VAR_ACTION_ORGANIZE': None,
                          '_VAR_ACTION_INDEP_ORGANIZE': None,
                          '_VAR_ACTION_INDEP_ORGANIZE_Name': None, '_VAR_ACTION_ORGANIZE_Name': None,
                          '_VAR_OWNER_ORGANIZES_Codes': None, '_VAR_ADDR': None, '_VAR_OWNER_ORGANIZES_Names': None,
                          '_VAR_URL': None,
                          '_VAR_ACTION_INDEP_ORGANIZES_Names': None, '_VAR_OWNER_ACCOUNT': None,
                          '_VAR_OWNER_USERCODES': None,
                          '_VAR_NOW_DAY': None, '_VAR_OWNER_REALNAME': None, '_VAR_NOW': None,
                          '_VAR_ENTRY_NUMBER': None,
                          '_VAR_ENTRY_NAME': None, '_VAR_ENTRY_TAGS': None}
        self.data = data

    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item
            elif isinstance(v, list):
                for row in v:
                    item = self._finditem(row, key)
                    if item is not None:
                        return item

    def get(self):
        data = {'_VAR_ENTRY_NAME': '', '_VAR_ENTRY_TAGS': ''}
        for k, v in self.item_keys.items():
            re = self._finditem(self.data, k)
            if re is not None:
                data[k] = re
        return data
