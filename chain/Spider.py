import base64
import json
import re

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_news_url():
    now = datetime.now()
    formatted_date = now.strftime('%Y%m%d')
    compare_date = now.strftime('%Y-%m-%d')
    params = [
        (
        "https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_china_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "国内"),
        (
        "https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_world_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "国际"),
        (
        "https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_society_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "社会"),
        (
        "https://top.sports.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=sports_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "体育"),
        (
        "https://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "财经"),
        (
        "https://top.ent.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=ent_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "娱乐"),
        (
        "https://top.tech.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=tech_news_suda&top_time={}&top_show_num=100&top_order=DESC".format(
            formatted_date), "科技"),
        (
        "https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_mil_suda&top_time={}&top_show_num=10&top_order=DESC".format(
            formatted_date), "军事"),
    ]
    res_urls = []
    for param in params:
        res = requests.get(param[0], headers=headers).content.decode("utf-8")
        res = res.replace("var data = ", "")
        res = res.replace(";", "")
        data = json.loads(res)
        count = 0
        for d in data["data"]:
            if count < 5 and d["create_date"] == compare_date:
                res_urls.append((d["url"], param[1]))
                count = count + 1
    return res_urls


def get_news_content():
    contents = []
    url_cats = get_news_url()
    for url_cat in url_cats:
        print(url_cat[0])
        res = requests.get(url_cat[0], headers=headers).content.decode("utf-8")
        soup = BeautifulSoup(res)
        title_div = soup.select("h1.main-title")
        title = None
        if len(title_div) > 0:
            title = title_div[0].text.strip()
        else:
            title = soup.select("h1#artibodyTitle")[0].text.strip()
        content = soup.select("div.article")[0].text.strip().replace(" ", "").replace("\n", "")
        contents.append(title + content)
    return contents


def get_36r_url():
    page_urls = [
        "https://36kr.com/information/AI/",
        "https://36kr.com/information/web_news/latest/",
        "https://36kr.com/information/technology/",
        "https://36kr.com/information/innovate/",
        "https://36kr.com/information/real_estate/",
        "https://36kr.com/information/travel/",
    ]
    all_urls = []
    for page_url in page_urls:
        res = requests.get(page_url, headers=headers).content.decode("utf-8")
        soup = BeautifulSoup(res)
        doms = soup.select("div.article-item-pic-wrapper > a.article-item-pic")[:5]
        sub_list = list(map(lambda d: "https://36kr.com" + d.get("href"), doms))
        all_urls.extend(sub_list)
    return all_urls

def decrypt(data):
    key = b'efabccee-b754-4c'
    encrypted_data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def get_36r_content():
    contents = []
    for url in get_36r_url():
        res = requests.get(url, headers=headers).content.decode("utf-8")
        soup = BeautifulSoup(res)
        json_str = soup.select("body > script")[0].text.replace("window.initialState=","")
        json_str = decrypt(json.loads(json_str)['state'])
        data = json.loads(json_str)
        title = data['articleDetail']['articleDetailData']['data']['widgetTitle']
        contenthtml = data['articleDetail']['articleDetailData']['data']['widgetContent']
        content = BeautifulSoup(contenthtml).text
        contents.append(title + content)
    return contents

