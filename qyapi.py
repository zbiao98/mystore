import requests
from requests_toolbelt import MultipartEncoder
import json


class WechatAlert():
  def __init__(self, corpid, corpsecret):
    self.sessions = requests.session()
    self.url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    self.corpid = corpid
    self.corpsecret = corpsecret

  def get_token(self):
    #获取token时，携带企业id和secret(注册企业号时，后台可查)
    url = self.url
    values = {
        'corpid': self.corpid,
        'corpsecret': self.corpsecret,
    }
    self.req = requests.get(url, params=values)
    data = json.loads(self.req.text)
    if data["errcode"] == 0:
        return data["access_token"]
    else:
        raise Exception("获取token出错！")

  def send_msg(self, values):
    #给单个人发送，也可以发送给多个人，但是不是一个群，"touser" : "ZhangYuan","agentid":"1000002",
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token()
    values = {"touser": "ZhengBiao",
              "toparty": "",
              "totag": "",
              "msgtype": "text",
              "agentid": "1000002",
              "text": {
                  "content": values   # 要推送的内容
              },
              "safe": "0"
              }
    self.sessions.post(url, json=values)

  def post_file(self, file, filename):
    post_file_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file".format(
        access_token=self.get_token())
    m = MultipartEncoder(
        fields={'file': (filename, file, 'multipart/form-data')},
    )
    r = self.sessions.post(url=post_file_url, data=m, headers={
                           'Content-Type': m.content_type})
    js = r.json()
    print("upload " + js['errmsg'])
    if js['errmsg'] != 'ok':
        return None
    return js['media_id']

  def send_img(self, _message):
    #给单个人发送，也可以发送给多个人，但是不是一个群，"touser" : "ZhangYuan","agentid":"1000002",
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_token()
    values = {"touser": "ZhengBiao",
              "toparty": "",
              "totag": "",
              "msgtype": "image",
              "agentid": "1000002",
              "image": {
                  "media_id": _message  # 要推送的内容
              },
              "safe": "0"
              }
    self.sessions.post(url, json=values)
