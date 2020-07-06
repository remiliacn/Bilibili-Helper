"""
Python script to get bilibili user's information by uuid.
"""

import json
import requests

class BilibiliStats:
    """
    Init the base url and data url by using uuid.
    """
    def __init__(self, uuid):
        self.base_url = 'https://api.bilibili.com/x/relation/stat?vmid=%s' % uuid
        self.data_url = 'https://api.bilibili.com/x/space/acc/info?mid=%s' % uuid
        self.uuid = uuid
        self.stats_dict = self._get_stats_dict()

    def _get_stats_dict(self):
        """
        Get stat dict by using json response from the bilibili API.
        :return: dict, user data. If non exist, return {'-1' : '查询内容不存在'}
        """
        page = requests.get(self.base_url).text
        json_data = json.loads(page)
        if 'code' in json_data and json_data['code'] == -400 or json_data['code'] == -404:
            return {'-1' : '查询内容不存在'}

        return json_data['data']

    def get_user_name(self):
        """
        Get user's bilibili nickname.
        :return: str, user's bilibili nickname if applicable
        """
        page = requests.get(self.data_url).text
        json_data = json.loads(page)
        if 'code' in 'json_data' and json_data['code'] == -404 or json_data['code'] == -400:
            return ''

        return json_data['data']['name']

    def get_following(self):
        """
        Get how many following do the user have
        :return: str, following stat in string.
        """
        if '-1' in self.stats_dict:
            return '信息不可用'

        return str(self.stats_dict['following'])

    def get_follower(self):
        """
        Get how many followers do the user have
        :return: str, followers stat in string.
        """
        if '-1' in self.stats_dict:
            return '信息不可用'
        return str(self.stats_dict['follower'])

    def __str__(self):
        """
        Compile all the information to human readable string.
        :return: str, user's information.
        """
        nick_name = self.get_user_name()
        if nick_name == '':
            return '未查到UUID为%s的用户信息' % self.uuid

        return f'UID为{self.uuid}的b站名为{self.get_user_name()}的用户数据如下：\n' \
               f'关注者：{self.get_follower()}人\n' \
               f'正在关注：{self.get_following()}人'
