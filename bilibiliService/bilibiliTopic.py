import requests, re, json, time

class bilibiliTopic:
    def __init__(self, topic):
        self.baseUrl = 'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/fetch_dynamics?topic_name=%s&sortby=2' % topic
        self.contentList = self._getContent()
        self.ifPic = self.checkIfPic()
        self.picList = self._getPicList()

    def _getContent(self):
        response = requests.get(self.baseUrl, timeout=10)
        contentDict = response.json()
        if contentDict['code'] != 0:
            return {'-1' : 'Invalid Content'}

        return json.loads(contentDict['data']['cards'][0]['card'])

    def checkIfPic(self):
        if 'item' in self.contentList and 'pictures' in self.contentList['item']:
            if len(self.contentList['item']['pictures']) >= 1:
                return True
            
        return False

    def _getPicList(self):
        imgList = []
        if self.ifPic:
            filepath = 'E:/bTopic/'
            json_data = self.contentList['item']['pictures']
            for pic in json_data:
                try:
                    img_src = pic['img_src']
                    pictureName = re.findall(r'\w+\.[jpgnif]{3}', img_src)[0]
                    path = filepath + pictureName
                    resp = requests.get(img_src, timeout=10)
                    resp.raise_for_status()
                    with open(path, 'wb') as f:
                        f.write(resp.content)

                    imgList.append(path)

                except Exception as e:
                    print('Error when getting picture: %s' % e)

        return imgList

    def getLastContent(self):
        response = ''
        uploadTime = self.contentList['item']['upload_time']
        import time
        currentTime = time.time()
        if currentTime - uploadTime < 100:
            response += self.getContent()

        return response

    def getContent(self):
        response = ''
        if 'item' in self.contentList:
            if 'description' in self.contentList['item']:
                response += self.contentList['item']['description']

            elif 'content' in self.contentList['item']:
                response += self.contentList['item']['content']

            if self.ifPic:
                for elements in self.picList:
                    response += '[CQ:image,file=file:///%s] ' % elements

        return response
