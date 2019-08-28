import requests, json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

class BilibiliDynamic:
    def __init__(self, uuid):
        self.baseUrl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=%s&offset_dynamic_id=0' % uuid
        self.contentDict = self._getDict()
        self.lastContent = self._getLastContent()

    def _getDict(self):
        try:
            page = requests.get(self.baseUrl, headers=headers).content.decode('utf-8')
        except Exception as e:
            print('Error occurred when getting dynamic %s' % e)
            return {'-1' : ''}

        json_data = json.loads(page)
        if json_data['data']['has_more'] == 0:
            return {'-1' : ''}

        return json.loads(json_data['data']['cards'][0]['card'])

    def _getLastContent(self):
        if '-1' in self.contentDict:
            return ''
        response = ''
        if 'content' in self.contentDict['item']:
            content = self.contentDict['item']['content']
            response += content
            originContent = self._getOriginDict()
            if originContent != '':
                if 'description' in originContent['item']:
                    response += '\n转发的原文：\n' + originContent['item']['description']
                else:
                    response += '\n转发的原文：\n' + originContent['item']['content']
        else:
            if 'description' in self.contentDict['item']:
                response += self.contentDict['item']['description']
            else:
                response += self.contentDict['item']['content']

        return response

    def _getOriginDict(self):
        try:
            return json.loads(self.contentDict['origin'])
        except KeyError:
            return ''

    def getLastContent(self):
        return self.lastContent
