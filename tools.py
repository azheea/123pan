import requests
import json

# 从shared.json文件中加载共享配置
shared = {}
try:
    with open("shared.json", "r", encoding="utf-8") as f:
        shared = json.loads(f.read())
except FileNotFoundError:
    shared = {}

# 设置API基础URL
api_url = "https://open-api.123pan.com"

# 从config.json文件中加载配置信息
try:
    with open("config.json", "r", encoding="utf-8") as f:
        file_content = json.loads(f.read())
except FileNotFoundError:
    raise Exception("配置文件config.json不存在")

# 定义config类用于存储和管理配置信息
class Config:
    def __init__(self, client_id, client_secret, access_token, share_father_floder, share_pwd,share_days):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.share_father_floder = share_father_floder
        self.share_pwd = share_pwd
        self.share_days = share_days

    def save(self):
        with open('./config.json', 'w', encoding='utf-8') as json_file:
            json.dump({
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "access_token": self.access_token,
                "share_father_floder": self.share_father_floder,
                "share_days": self.share_days,
                "default_pwd": self.share_pwd
            }, json_file, ensure_ascii=False, indent=4)

# 实例化config对象
cfg = Config(
    client_id=file_content["client_id"],
    client_secret=file_content["client_secret"],
    access_token=file_content["access_token"],
    share_father_floder=file_content["share_father_floder"],
    share_pwd=file_content["default_pwd"],
    share_days=file_content["share_days"]
)

# 设置请求头信息，包含Authorization和Platform
header = {"Authorization": f"Bearer {cfg.access_token}", "Platform": "open_platform"}

# 定义获取访问令牌的函数
def get_access_token():
    data = {"clientID": cfg.client_id, "clientSecret": cfg.client_secret}
    response = requests.post(url=f"{api_url}/api/v1/access_token", data=data, headers={"Platform": "open_platform"})
    if response.status_code != 200:
        raise Exception("获取访问令牌失败")
    data = json.loads(response.text)
    cfg.access_token = data.get("data").get("accessToken")
    cfg.save()
    return data.get("data")

# 定义获取文件列表的函数
def get_file_list(floder_id):
    data = {"limit": "100", "parentFileId": floder_id}
    response = requests.get(url=f"{api_url}/api/v2/file/list", data=data, headers=header)
    if response.status_code != 200:
        raise Exception("获取文件列表失败")
    return json.loads(response.text).get("data")

# 定义分享文件的函数
def share(fileId, filename):
    data = {"shareName": f"{filename}", "shareExpire": cfg.share_days, "fileIDList": str(fileId), "sharePwd": cfg.share_pwd}
    response = requests.post(url=f"{api_url}/api/v1/share/create", data=data, headers=header)
    if response.status_code != 200:
        raise Exception("分享文件失败")
    return json.loads(response.text).get("data")

# 定义分享所有文件的函数
def share_floder(floder_id):
    files = get_file_list(floder_id)
    for i in files.get("fileList"):
        fileName = i.get("filename")
        fileId = i.get("fileId")
        if i.get("type") == 1:
            share_floder(fileId)
            print("floder",fileId)
            continue
        else:
            if shared.get(fileName) is None:
                key = str(share(fileId, fileName).get("shareKey", "22"))
                shared[fileName] = f"https://www.123pan.com/s/{key}"
                print("file",fileId)

    with open('./shared.json', 'w', encoding='utf-8') as json_file:
        json.dump(shared, json_file, ensure_ascii=False, indent=4)

def share_all():

    pass
# 获取访问令牌
get_access_token()
# 分享所有文件
share_floder(floder_id=cfg.share_father_floder)