import requests
import json
import tools
from flask import Flask, redirect


with open("shared.json", "r", encoding="utf-8") as f:
    shared = json.loads(f.read())

with open("config.json", "r", encoding="utf-8") as f:
    file_content = json.loads(f.read())
class config:
    client_id = file_content["client_id"]
    client_secret = file_content["client_secret"]
    access_token = file_content["access_token"]
    share_floder = file_content["share_floder"]
    share_pwd = file_content["default_pwd"]
cfg = config()

app = Flask(__name__, static_url_path='/')

@app.route("/<file>")
def show_pic(file):
    link = shared.get(file,"Nonee")
    # print(link)
    if link != "Nonee":
        url = "https://api.pearktrue.cn/api/123panparse/"
        data = {"url":link,"pwd":cfg.share_pwd}
        request  = (requests.post(url, data=data)).text
        # print(request)
        request = json.loads(request).get("data").get("downloadurl")    
        # print(request)
        return redirect(request)
    else:
        return ""

@app.route("/")
def index():
    return ""
@app.route("/None")
def a():
    return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)