# 123pan

Using openapi by 123 to make it becomeing own cdn

123盘可以直接获取100M以下文件的直链 配合123的[openapi](https://www.123pan.com/developer)可以实现批量文件的上传 这也是使123成为cdn的原理

## 环境

python

```python
pip install requests
pip install flask
```

## 开始

1. 完成环境配置
2. 申请[开发者](https://www.123pan.com/developer) 并将获取的

| **clientID**     |
| ---------------------- |
| **clientSecret** |

填入config.json的内部

3.获取欲作为文件的文件夹id 填入config.json

4.配置分享的密码（需等于4位且无中文）

5.运行tool.py

6.运行main.py即可获得cdn 访问的链接为 0.0.0.0:5000/文件名

enjoy.it
