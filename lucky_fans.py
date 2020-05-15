# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2020 LegHair All Rights Reserved
#
################################################################################
"""
lucky fans 抽奖demo
Authors: leghair(B站：腿毛酱学剪辑）
Date:    2020/02/08
"""
import requests
import json
import tkinter
import random
import threading
import time

from PIL import Image, ImageTk

cookies = {"Cookie": "XXX"}

def get_fans_set(vmid):
    """
    获取up主粉丝id
    :param vimid: up主vimid
    :return:
        fans_set 某页粉丝id集合
    """
    global fans_num
    fans_set = set()
    url = "https://api.bilibili.com/x/relation/followers?vmid=%s&pn=1&ps=20&order=desc&jsonp=jsonp" % vmid
    r = requests.get(url)
    res = r.text
    res = json.loads(res)
    fans_num = res["data"]["total"]
    # 粉丝页数向上取整
    page_num = fans_num // 20 + 1
    for n in range(1, page_num + 1):
        url = "https://api.bilibili.com/x/relation/followers?vmid=%s&pn=%s&ps=20&order=desc&jsonp=jsonp" \
              % (vmid, str(n))
        r = requests.get(url, cookies=cookies)
        res = r.text
        res = json.loads(res)
        if res["data"]["list"] is not None:
            for item in res["data"]["list"]:
                fans_set.add(item["uname"])
    return fans_set


def get_reply_set(oid):
    """
    获取去重后评论列表
    :param oid: 视频id
    :return: reply_fans_set 评论ID
    """
    global reply_num
    reply_fans_set = set()
    url = "http://api.bilibili.com/x/reply?type=1&oid=%s&pn=1" % oid
    r = requests.get(url)
    res = r.text
    res = json.loads(res)
    reply_num = res["data"]["page"]["count"]
    # 评论页数向上取整
    page_num = reply_num // 20 + 1
    for n in range(1, page_num + 1):
        url = "http://api.bilibili.com/x/reply?type=1&oid=%s&pn=%s" % (oid, str(n))
        req = requests.get(url)
        res = req.text
        res = json.loads(res)
        if res["data"]["replies"] is not None:
            for item in res["data"]["replies"]:
                reply_fans_set.add(item["member"]["uname"])
    return reply_fans_set


def switch():
    """
    随机
    :return:
    """
    while root.flag:
        random_num = random.randint(0, len(lottery_list) - 1)
        fans_area["text"] = lottery_list[random_num]
        time.sleep(0.1)


def btn_start():
    """
    开始按钮触发
    :return:
    """
    root.flag = True
    t = threading.Thread(target=switch)
    t.start()


def btn_stop():
    """
    结束按钮触发
    :return:
    """
    root.flag = False


video_oid = "83911522"
vmid = "25306892"

reply_fans_set = get_reply_set(video_oid)
fans_set = get_fans_set(vmid)

# 取粉丝集与评论集交集
lottery_list = list(fans_set.intersection(reply_fans_set))

# 关注并评论的数量
lottery_num = len(lottery_list)

# 初始化窗口
root = tkinter.Tk()
root.title("腿毛酱的粉丝抽奖")
root.geometry("600x500+400+200")
root.resizable(False, False)
root.flag = True

# 布局
btnStart = tkinter.Button(root, text="开始", command=btn_start)
btnStart.place(x=50, y=30, width=80, height=20)

butStop = tkinter.Button(root, text="停止", command=btn_stop)
butStop.place(x=200, y=30, width=80, height=20)

fans_num_area = tkinter.Label(root, text="", font=("宋体", 15, "normal"))
fans_num_area.place(x=350, y=10, width=200, height=20)
fans_num_area["text"] = "卑微up粉丝数：%d" % fans_num

reply_num_area = tkinter.Label(root, text="", font=("宋体", 15, "normal"))
reply_num_area.place(x=350, y=30, width=200, height=20)
reply_num_area["text"] = "去重后参与评论ID数：%d" % reply_num

num_area = tkinter.Label(root, text="", font=("宋体", 15, "normal"))
num_area.place(x=350, y=50, width=200, height=20)
num_area["text"] = "抽奖数(评论且关注)：%d" % lottery_num

fans_area = tkinter.Label(root, text="", font=("宋体", 30, "normal"))
fans_area.place(x=100, y=80, width=300, height=150)

pilImage = Image.open("./leghair.png")
tkImage = ImageTk.PhotoImage(image=pilImage)
image_label = tkinter.Label(image=tkImage)
image_label.place(x=30, y=200, width=600, height=300)

# 启动主程序
root.mainloop()
