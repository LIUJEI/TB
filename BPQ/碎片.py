from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base.spider import Spider
import requests
import json
import time
import random
import binascii

class Spider(Spider):
    
    def __init__(self):
        self.host = "https://free-api.bighotwind.cc"
        self.res_api = "https://speed.howdbm.com/papaya/papaya-file/files/download/"
        self.cache_token_key = 'com.sha.fragment_token'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; 22041211A Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Safari/537.36",
            "Accept-Encoding": "gzip",
            "authorization": "",
            "uuid": ""
        }
        self.player_headers = {
            'User-Agent': 'com.android.chrome/131.0.6778.200 (Linux;Android 9) AndroidXMedia3/1.8.0'
        }

    def getName(self):
        return "首页"

    def init(self, extend):
        self.login()

    def login(self):
        try:
            uuid_key = 'com.sha.fragment_uuid'
            u = self.getCache(uuid_key)
            if u:
                u = u.lstrip("value=")
            if not u:
                u = self.generate_android_id()
                self.setCache(uuid_key, u)
            
            t = self.getCache(self.cache_token_key)
            if t:
                t = t.lstrip("value=")
            if not t:
                h = self.headers.copy()
                h['key'] = self.encrypt(str(int(time.time() * 1000)))
                h['content-type'] = 'application/json; charset=utf-8'
                
                r = requests.post(f'{self.host}/papaya/papaya-api/oauth2/uuid', 
                                data=json.dumps({"openId": u}), headers=h)
                r.encoding = "utf-8"
                data = r.json()
                t = data['data']['token']
                if t:
                    self.setCache(self.cache_token_key, t)
            
            self.headers['authorization'] = t
            self.headers['uuid'] = u
        except Exception:
            self.host = None

    def re_login(self):
        self.delCache(self.cache_token_key)
        self.login()

    def encrypt(self, plaintext):
        cipher = AES.new("p0sfjw@k&qmewu#w".encode('utf-8'), AES.MODE_ECB)
        data_bytes = plaintext.encode('utf-8')
        bs = AES.block_size
        pad_data = pad(data_bytes, bs)
        enc_bytes = cipher.encrypt(pad_data)
        return binascii.hexlify(enc_bytes).decode('utf-8')

    def generate_android_id(self):
        return ''.join(random.choice('0123456789abcdef') for _ in range(16))

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {"class": []}
        
        if not self.host:
            return result

        url = f'{self.host}/papaya/papaya-api/theater/tags'
        try:
            detail = requests.get(url=url, headers=self.headers)
            detail.encoding = "utf-8"
            data = detail.json()
            
            if data.get('code') == 401:
                self.re_login()
                return self.homeContent(filter)
                
            for vod in data['data']:
                result["class"].append({
                    "type_id": vod['id'], 
                    "type_name": "集多🌠" + vod['text_val']
                })
                
        except Exception:
            pass
            
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, cid, pg, filter, ext):
        videos = []

        if not self.host:
            return {'list': videos, 'page': pg, 'pagecount': 1, 'limit': 90, 'total': 0}

        page = int(pg) if pg else 1
        url = f'{self.host}/papaya/papaya-api/videos/page?type=5&tagId={cid}&pageNum={page}&pageSize=12'
        
        try:
            detail = requests.get(url=url, headers=self.headers)
            detail.encoding = "utf-8"
            data = detail.json()
            
            if data.get('code') == 401:
                self.re_login()
                return self.categoryContent(cid, pg, filter, ext)
                
            for vod in data['list']:
                videos.append({
                    "vod_id": f"{vod['itemId']}@{vod['videoCode']}@{vod.get('content','未知')}@{vod.get('tags','未知')}",
                    "vod_name": vod['title'],
                    "vod_pic": f"{self.res_api}{vod['imageKey']}/{vod['imageName']}",
                    "vod_remarks": '集多▶️' + vod.get('tags','未知')
                })
                
        except Exception:
            pass

        return {
            'list': videos,
            'page': pg,
            'pagecount': 9999,
            'limit': 90,
            'total': 999999
        }

    def detailContent(self, ids):
        videos = []
        
        if not self.host:
            return {'list': videos}

        did = ids[0]
        fenge = did.split("@")
        
        if len(fenge) < 4:
            itemId, videoCode, content, tags = fenge[0], fenge[1], fenge[2] if len(fenge) > 2 else '未知', '未知'
        else:
            itemId, videoCode, content, tags = fenge[0], fenge[1], fenge[2], fenge[3]

        url = f'{self.host}/papaya/papaya-api/videos/info?videoCode={videoCode}&itemId={itemId}'
        
        try:
            detail = requests.get(url=url, headers=self.headers)
            detail.encoding = "utf-8"
            data = detail.json()
            
            if data.get('code') == 401:
                self.re_login()
                return self.detailContent(ids)
                
            episodes_data = data['data']['episodesList']
            bofang = ''
            
            for vod in episodes_data:
                file_info = vod['resolutionList'][0]
                bofang += f"{vod['episodes']}${self.res_api}{file_info['fileKey']}/{file_info['fileName']}#"

            bofang = bofang[:-1]
            
            videos.append({
                "vod_id": did,
                "vod_content": '集多为您介绍剧情📢📢' + content,
                "type_name": tags,
                "vod_remarks": f"全{len(episodes_data)}集",
                "vod_play_from": '碎片专线',
                "vod_play_url": bofang
            })
            
        except Exception:
            pass

        return {'list': videos}

    def playerContent(self, flag, id, vipFlags):
        return {
            "parse": 0,
            "playUrl": '',
            "url": id,
            "header": self.player_headers
        }

    def searchContentPage(self, key, quick, pg):
        videos = []

        if not self.host:
            return {'list': videos, 'page': pg, 'pagecount': 1, 'limit': 90, 'total': 0}

        page = int(pg) if pg else 1
        url = f'{self.host}/papaya/papaya-api/videos/page?type=5&search={key}&pageNum={page}&pageSize=12'
        
        try:
            detail = requests.get(url=url, headers=self.headers)
            detail.encoding = "utf-8"
            data = detail.json()
            
            if data.get('code') == 401:
                self.re_login()
                return self.searchContentPage(key, quick, pg)
                
            for vod in data['list']:
                videos.append({
                    "vod_id": f"{vod['itemId']}@{vod['videoCode']}@{vod.get('content','未知')}@{vod.get('tags','未知')}",
                    "vod_name": vod['title'],
                    "vod_pic": f"{self.res_api}{vod['imageKey']}/{vod['imageName']}",
                    "vod_remarks": '集多▶️' + vod.get('tags','未知')
                })
                
        except Exception:
            pass

        return {
            'list': videos,
            'page': pg,
            'pagecount': 9999,
            'limit': 90,
            'total': 999999
        }

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, pg)
