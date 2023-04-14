import requests
import json
import os
import random

checkingUrl = f'https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/listNotifications?status=NotificationStatusUnread&type=NotificationTypePopup&is_sort=true'
getGameVersion = f'https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/resource?key=eYd89JmJ&launcher_id=18'
accountState = 'https://api-cloudgame.mihoyo.com/hk4e_cg_cn/wallet/wallet/get'

# 获取当前云原神的版本
version_info = requests.get(getGameVersion, timeout=30).text
version = json.loads(version_info)["data"]["game"]["latest"]["version"]

# 从Action的Environment secrets中获取所填写的Data变量
# playerData = json.loads(os.environ.get('Data'))
dataTemp = open('Data.json')
playerData = json.loads(dataTemp.readline())

headers = {
    "x-rpc-combo_token": playerData["x-rpc-combo_token"],
    "x-rpc-client_type": "2",
    "x-rpc-app_version": str(version),
    "x-rpc-sys_version": str(playerData["x-rpc-sys_version"]),
    "x-rpc-channel": "mihoyo",
    "x-rpc-device_id": playerData["x-rpc-device_id"],
    "x-rpc-device_name": playerData["x-rpc-device_name"],
    "x-rpc-device_model": playerData["x-rpc-device_model"],
    "x-rpc-app_id": str(playerData["x-rpc-app_id"]),
    "Referer": "https://app.mihoyo.com",
    "x-rpc-vendor_id": str(playerData["x-rpc-vendor_id"]),
    "Host": "api-cloudgame.mihoyo.com",
    "Connection": "Keep-Alive",
    "AcceptEncoding": "gzip",
    "UserAgent": "okhttp/4.9.0"
}


def min_transform(value):
    value = int(value)
    m = int(value % 60)
    h = int(value / 60)
    if h:
        return f'{h}时{m}分'
    else:
        return f'{m}分'


def checking():
    # 获取玩家云原神账号状态
    state = json.loads(requests.get(accountState, headers=headers, timeout=30).text)
    free_time = state["data"]["free_time"]["free_time"]
    free_time_limit = state["data"]["free_time"]["free_time_limit"]
    percent = (int(free_time) / int(free_time_limit)) * 100
    coin = state["data"]["coin"]["coin_num"]
    detect = json.loads(requests.get(checkingUrl, headers=headers, timeout=30).text)

    # 签到判断
    if not detect["data"]["list"]:
        if free_time < free_time_limit:
            print(f'签到完成\n')
        if free_time >= free_time_limit:
            print(f'已达到免费时长上限\n')
    else:
        print(f'签到失败\n')

    print(
        f'可用时长：{min_transform(free_time)}/{min_transform(free_time_limit)}({int(percent)}%)\n可用米云币：{coin}|{state["data"]["play_card"]["short_msg"]}月卡')


if __name__ == '__main__':
    checking()
