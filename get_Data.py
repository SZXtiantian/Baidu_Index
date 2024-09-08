#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/9/8 8:21
# @Author  : 钟昊天2021280300
# @FileName: get_Data.py
# @Software: PyCharm

import gzip
import json
import zlib

import brotli
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver


def fetch_data(rule, browser, encoding="utf-8", is_json=True):
    result = ""
    for request in reversed(browser.requests):
        if rule in request.url:
            res = request.response
            result = res.body.decode(encoding)
            if is_json:
                result = json.loads(result)
            return result


def decrypt(ptbk, index_data):
    n = len(ptbk) // 2
    a = dict(zip(ptbk[:n], ptbk[n:]))
    return "".join([a[s] for s in index_data])


def get_baidu_index_data(keyword, cookie_string):
    # 解析Cookie字符串
    cookie_items = cookie_string.strip().split('; ')
    cookies = []
    for item in cookie_items:
        if item:
            cookie_name, cookie_value = item.split('=', 1)
            cookies.append({
                'name': cookie_name,
                'value': cookie_value,
                'domain': '.index.baidu.com',
                'path': '/',
                'secure': False,
                'httpOnly': False
            })

    # 启动浏览器
    browser = webdriver.Chrome()
    browser.get('https://index.baidu.com/v2/index.html')

    # 添加cookie到browser
    for cookie in cookies:
        try:
            browser.add_cookie(cookie)
        except Exception as e:
            print(f"无法添加cookie: {cookie['name']}, 错误: {e}")

    # 重新加载页面以使cookie生效
    browser.get('https://index.baidu.com/v2/index.html')

    # 等待搜索输入框出现并执行搜索
    wait = WebDriverWait(browser, 30)
    search_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#search-input-form > input.search-input")))
    search_input.send_keys(Keys.CONTROL + 'a')
    search_input.send_keys(Keys.DELETE)
    search_input.send_keys(keyword + '\n')
    # 使用 XPath 定位到要等待的元素
    element_xpath = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[1]/canvas'
    canvas_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, element_xpath))
    )

    # 创建 ActionChains 对象
    actions = ActionChains(browser)

    # 计算元素的中心位置
    element_size = canvas_element.size
    element_location = canvas_element.location

    # 将鼠标移动到元素的中心位置
    actions.move_to_element_with_offset(canvas_element, 0, 0).perform()

    # 执行所有 ActionChains 中存储的行为
    actions.perform()
    ptbk = fetch_data("Interface/ptbk", browser)['data']
    data = fetch_data("api/SearchApi/index", browser)['data']
    results = {}
    for userIndexe in data['userIndexes']:
        name = userIndexe['word'][0]['name']
        index_data = userIndexe['all']['data']
        r = decrypt(ptbk, index_data)
        results[name] = r
    return results


cookie_string = """
BIDUPSID=C04C564F13356D994DABA3E3E6EB0B75; PSTM=1712751972; BAIDUID=F4C9CEB6A595F1DD09C750DCE861C0FB:FG=1; H_PS_PSSID=60271_60628_60678_60682_60694_60573; BAIDUID_BFESS=F4C9CEB6A595F1DD09C750DCE861C0FB:FG=1; H_WISE_SIDS=60271_60628_60678_60682_60694_60573; ZFY=mbmQlx4KCMowAJYsbF2o5sZ23xuhgV3UTMyjKUB0bIo:C; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1725693415,1725709133,1725764148,1725764229; HMACCOUNT=E4929EF0C40A707B; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGkdximGddNRzN/k8jMV5fwkGEimjy3MrXEpSuItnI4KD5D2jfuh+RInKG5l8qaOcCsKUxD4QgTImMHTTY4+nES24R/FnOemjNRCuI1DYLMopx8XUPJGV6+o409dgWc+CNLGgLbz7OSojK1zRbqBESR5Pdk2R9IA3lxxOVzA+Iw1TWLSgWjlFVG9Xmh1+20oPSbrzvDjYtVPmZ+9/6evcXmhcO1Y58MgLozKnaQIaLfWRFwa8A3ZyTRp/cDxRMhYc96TkBN9pNkCOO/1Sub57NVXH3co00Kpvjvb6N616ocq53eTNkbS2el0J2+pbyoXJb1zi9UjY/gyQc84qDeVbq0UqfhwWryYacZfOfIdenDLSkJsc4rBzsbBPyjKAzWGBO7nCxNtgYtDo26K+8ukl31Y+/geIrmTvn+xVA1gAbbf1lkKhylX1zGsOVlJip30kecMEGvjdNWpsel/qfsfe5JBpqDTksMVoBr7nszRboiUHbedcq1mi/UXvX2b3lxbCLv4Mxoy+dFS3Fr9jSAmssiPARPZutqXQT8krr+KVakPUpdbkwv/8CHDu0C/Z5vtDeiYLQpEgFjmQoey69Fz+kM7Y5cg925MGCeBU4jWp2g2g9JPVK2vTTCj0NreDMNm1uAdaJvpBOjUNpfxe7Z//kbxYdBrxFfXZ8kxisvFxYwkIkhpOuhw8bYyjFOBzzWtHbYbSa9AM5B1U28ZEDPBEvSMRPgS91Uw7CJQXNUDxDR+gXJQoG0sQhLOfQ+H6CPhLu1e5pW3qVm6jGndb2e9A44Ff783NoSEXEYa2vz+1inzUGzinVPKXI+oymb7UrF2I+ZEd6VO50CmaP+JD/V8nCK/kazYq146hp/2XIWCky++QvQau87dgPQPBPOdZfELQaEBSLlhBmNwzEBsxOHy7QZw9iAQNcYCK2xfeYf2imATVV3bwYaC8F4XJ12oqlxKXLxUJaJyL/ORX2lW3xKCro0F9iAQNcYCK2xfeYf2imATVYemNDYxCmdd8ZXU4Cg4htkEQSRUz7L4kkhL4CxkTt2IBjr/vyN58BqfauYSxfP9O4KEVJ4njsvVmNwgrtRSkK2MAD23qY0MlH51PwQdoK9bWx4UhpRCqPktHIslB6EWFA==; BDUSS=JneHpZa2tkTWxKSzExRWh1bVlJSHl1Q3R-ek0wUEl1c3BWQmhaWmVhZkVud1JuRUFBQUFBJCQAAAAAAAAAAAEAAACDiP570KHM7MzssK7E49~PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMQS3WbEEt1ma0; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04757767433Cxb5UgIDu2dvF9xulQSLkfO8qDKobIi0RAOIB1YVlgFf4BHq7aXXTM4W2%2F4mQKxHsboRAmOVNP6eqJ0c3fAaN3V8nZH1nrzYmwleEB5p%2Fe2hktxolbOzAQHrr42dAdz0H793Xe1vLNPOrlopbmBS8iTjKvx3pqN6hACFZ4WWDEi8Erd7lPo0yobV8RtOsGh5H793Xe1vLNPOrlopbmBS8iTjKvx3pqN6hACFZ4WWDEj1ccn52czWoicRa3Oq%2BX8tXQ72dQSD4bh74xZZ7NXyeFKA0NAcCK68155mObHYZcPrqdqFtyfkq3i%2Bl1Hd3d1LHljmuod8EDw3km%2FQTzqlt4VMUSZRrFO%2FiEtpvWiOeUk%3D01373639964383455002269596289186; __cas__rn__=475776743; __cas__st__212=4c8c0d0c794c3c1e7dc20c29b52d560048f9721ebf9b031a70d6300811746d0f465436ed3fbcab26c410b7e8; __cas__id__212=58451636; CPTK_212=790803444; CPID_212=58451636; bdindexid=6db9avobhe9gu0sc66epce12c1; RT="z=1&dm=baidu.com&si=d3c7e922-b3c7-439b-b8b6-3b29c91b9a80&ss=m0szexw1&sl=k&tt=au2&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1725764314; ab_sr=1.0.1_ODUzZjFiMTdlZTczOGEwZmZmN2U5NDAzNWQ2MjE4MGYyYmUzOWQ2YTdkZWE3YTk5N2IxNjJjNTlmZmU4NGFjNTlkOTAwNjY0ODhlOTk4NjdiZGI4YjI1MDY5YTg3ZGViYWJhYmE2MTBjNWYzMDkwNzg4NGUzMDI3NWIzMjNlMDZhZmI5MDcxMDhiM2FkMzdkZWZmMjE0NDEwMmI4MjgxMA==; BDUSS_BFESS=JneHpZa2tkTWxKSzExRWh1bVlJSHl1Q3R-ek0wUEl1c3BWQmhaWmVhZkVud1JuRUFBQUFBJCQAAAAAAAAAAAEAAACDiP570KHM7MzssK7E49~PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMQS3WbEEt1ma0
"""
file_path = "./test.txt"

# keywords = ["000062", "000063"]
keywords = []
with open(file_path, 'r') as file:
    for line in file:
        keywords.append(line.strip())

print(keywords)

index_data_all = {}

for keyword in keywords:
    index_data = get_baidu_index_data(keyword + '\n', cookie_string)
    index_data_all[keyword] = index_data
    print(f"百度指数数据 for '{keyword}': {index_data}")

print("所有关键词的百度指数数据:")
print(index_data_all)
