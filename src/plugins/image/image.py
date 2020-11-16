# import requests
# import random
# from os import path, mkdir


# def getPic():
#     i = random.randint(1, 2)
#     print(i)
#     if i == 1:
#         res = requests.get("http://api.mtyqx.cn/api/random.php", verify=False)
#     elif i == 2:
#         res = requests.get("http://www.dmoe.cc/random.php", verify=False)
#     # elif i == 3:
#         # res = requests.get("https://random.52ecy.cn/randbg.php", verify=False)
#     # elif i == 3:
#         # res = requests.get("http://img.xjh.me/random_img.php", verify=False)

#     # 检查图片存放路径
#     if not path.exists('./pixdata/'):
#         mkdir('./pixdata')
#     # 保存图片
#     with open('./pixdata/x.png', "wb") as f:
#         f.write(res.content)
#         f.close()
#     return True
