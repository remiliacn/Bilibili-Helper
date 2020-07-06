"""
Python script to get bilibili topic information from a keyword.
"""

from json import loads
from re import findall
from time import time
from requests import get

class BilibiliTopic:
    """
    Set up the base url for a keyword using bilibili topic API.
    """
    def __init__(self, topic):
        self.base_url = 'https://api.vc.bilibili.com/topic_svr/' \
                        f'v1/topic_svr/fetch_dynamics?topic_name={topic}&sortby=2'

        self.content_list = self._get_content()
        self.if_pic = self.check_if_pic()
        self.pic_list = self._get_pic_list()

    def _get_content(self):
        """
        Get content from the base url got from the API.
        :return: dict, content from the bilibili topic API.
        """
        response = get(self.base_url, timeout=10)
        content_dict = response.json()
        if content_dict['code'] != 0:
            return {'-1' : 'Invalid Content'}

        return loads(content_dict['data']['cards'][0]['card'])

    def check_if_pic(self) -> bool:
        """
        Check if there is picture from the content.
        :return: bool, if there is pic in the content.
        """
        if 'item' in self.content_list and 'pictures' in self.content_list['item']:
            if len(self.content_list['item']['pictures']) >= 1:
                return True

        return False

    def _get_pic_list(self) -> list:
        """
        Get a list of path that picture downloaded.
        :return: list, downloaded path for all pictures in a topic.
        """
        img_list = []
        if self.if_pic:
            file_path = 'E:/bTopic/'
            json_data = self.content_list['item']['pictures']
            for pic in json_data:
                try:
                    img_src = pic['img_src']
                    picture_name = findall(r'\w+\.[jpgnif]{3}', img_src)[0]
                    path = file_path + picture_name
                    resp = get(img_src, timeout=10)
                    resp.raise_for_status()
                    with open(path, 'wb') as file_opened:
                        file_opened.write(resp.content)

                    img_list.append(path)

                except Exception as err:
                    print('Error when getting picture: %s' % err)

        return img_list

    def get_last_content(self) -> str:
        """
        Get the last content in str.
        :return: str, the last content.
        """
        response = ''
        upload_time = self.content_list['item']['upload_time']
        current_time = time()
        if current_time - upload_time < 100:
            response += self.get_content()

        return response

    def get_content(self):
        """
        Convert content to readable string.
        :return: str, the content of the topic.
        If there is image, it will be converted to CQ code
        """
        response = ''
        if 'item' in self.content_list:
            if 'description' in self.content_list['item']:
                response += self.content_list['item']['description']

            elif 'content' in self.content_list['item']:
                response += self.content_list['item']['content']

            if self.if_pic:
                for elements in self.pic_list:
                    response += '[CQ:image,file=file:///%s] ' % elements

        return response
