#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/9/8 8:03
# @Author  : 钟昊天2021280300
# @FileName: auto_login.py
# @Software: PyCharm
import json
from selenium import webdriver

# 定义你的Cookie字符串
cookie_string = """
BIDUPSID=C04C564F13356D994DABA3E3E6EB0B75; PSTM=1712751972; BAIDUID=F4C9CEB6A595F1DD09C750DCE861C0FB:FG=1; H_PS_PSSID=60271_60628_60678_60682_60694_60573; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=F4C9CEB6A595F1DD09C750DCE861C0FB:FG=1; H_WISE_SIDS=60271_60628_60678_60682_60694_60573; BA_HECTOR=012kah0h2g8ka404a12g8001arffi41jdlnrb1v; ZFY=mbmQlx4KCMowAJYsbF2o5sZ23xuhgV3UTMyjKUB0bIo:C; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1725692681,1725693155,1725693206,1725693415; HMACCOUNT=E4929EF0C40A707B; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGkdximGddNRzN/k8jMV5fwkGEimjy3MrXEpSuItnI4KD5D2jfuh+RInKG5l8qaOcCsKUxD4QgTImMHTTY4+nES24R/FnOemjNRCuI1DYLMopx8XUPJGV6+o409dgWc+CNLGgLbz7OSojK1zRbqBESR5Pdk2R9IA3lxxOVzA+Iw1TWLSgWjlFVG9Xmh1+20oPSbrzvDjYtVPmZ+9/6evcXmhcO1Y58MgLozKnaQIaLfWRFwa8A3ZyTRp/cDxRMhYc96TkBN9pNkCOO/1Sub57NVXH3co00Kpvjvb6N616ocq53eTNkbS2el0J2+pbyoXJb1zi9UjY/gyQc84qDeVbq0UqfhwWryYacZfOfIdenDLSkJsc4rBzsbBPyjKAzWGBO7nCxNtgYtDo26K+8ukl31Y+/geIrmTvn+xVA1gAbbf1lkKhylX1zGsOVlJip30kecMEGvjdNWpsel/qfsfe5JBpqDTksMVoBr7nszRboiUHbedcq1mi/UXvX2b3lxbCLv4Mxoy+dFS3Fr9jSAmssiPARPZutqXQT8krr+KVakPUpdbkwv/8CHDu0C/Z5vtDeiYLQpEgFjmQoey69Fz+kM7Y5cg925MGCeBU4jWp2g2g9JPVK2vTTCj0NreDMNm1uAdaJvpBOjUNpfxe7Z//kbxYdBrxFfXZ8kxisvFxYwkIkhpOuhw8bYyjFOBzzWtHbYbSa9AM5B1U28ZEDPBEvSMRPgS91Uw7CJQXNUDxDR+gXJQoG0sQhLOfQ+H6CPhLu1e5pW3qVm6jGndb2e9A44Ff783NoSEXEYa2vz+1inzUGzinVPKXI+oymb7UrF2I+ZEd6VO50CmaP+JD/V8nCK/kazYq146hp/2XIWCky++QvQau87dgPQPBPOdZfELQaEBSLlhBmNwzEBsxOHy7QZw9iAQNcYCK2xfeYf2imATVV3bwYaC8F4XJ12oqlxKXLxUJaJyL/ORX2lW3xKCro0F9iAQNcYCK2xfeYf2imATVYemNDYxCmdd8ZXU4Cg4htkEQSRUz7L4kkhL4CxkTt2IBjr/vyN58BqfauYSxfP9O4KEVJ4njsvVmNwgrtRSkK2MAD23qY0MlH51PwQdoK9bWx4UhpRCqPktHIslB6EWFA==; BDUSS=3BQaDg2andzZnpBdVlCSVR0Tm5HYUFpbVJtaWpWbVhlYU1US3Z6MEFWYU9qQU5uRUFBQUFBJCQAAAAAAAAAAAEAAACDiP570KHM7MzssK7E49~PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI7~22aO~9tmV; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04757062888xtCiRAJl4yCU%2Bj26TvkZCUHP8khgmFsQ8iXW2d%2BJezQRZjrkhqvMnk%2FYfxBYWRFuubA2qjIkQ8J2sJmzRETKRbs4i%2FMlOBTgyG1qj32P%2FMFduomJUde%2FVyY6P7kLHqFUmEXINw4edxB7fGOQAfooZP0GJloaBwKeObyIMj0abjKcqWoZJHYQN%2BKFmlOM7a4jmEXINw4edxB7fGOQAfooZP0GJloaBwKeObyIMj0abjIj51OmzvdGCD%2BG7UQTAq8Pmi4OV1pxYjDdbLfwaR%2BsadMmdgXS6THGxGRaq3lxAd0kwKN7Lw%2FGXQTjrYJDwpWAFZqD9DUD5pvNh7BaZiTySim87YWCP%2B7aLgn0kqTxW24%3D22604821148050261798598229621020; __cas__rn__=475706288; __cas__st__212=51094cab704df4ac667c15b0033d2243586bc3847eeeebbcab26c710a6ce4808e0ce233ebcfe518bc7dd4cee; __cas__id__212=58451636; CPTK_212=1173826277; CPID_212=58451636; bdindexid=bierb1i90jgg178v6r4kceh7m6; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1725697844; ab_sr=1.0.1_ZGIzM2EyNTgzYzgzOWI3ZWM4NmQwZGRmZGE0YWM2YzNjMTFmM2JkZjZmNjg4OWZhOWJiMGQ3NjkzODFiZWRlODU4ODBlZGVhZTRkMDA2YzFkYjI5YjVmMWM0ZDc3MDFkNDI3YWZjNzcxMTIyNWIzNjIxYmE3ZDk1NTU4ZmRlNjczYTk1MzEyOWViNGI3Y2Y3OGQ1M2VhZTUzZDU3NTY4NQ==; BDUSS_BFESS=3BQaDg2andzZnpBdVlCSVR0Tm5HYUFpbVJtaWpWbVhlYU1US3Z6MEFWYU9qQU5uRUFBQUFBJCQAAAAAAAAAAAEAAACDiP570KHM7MzssK7E49~PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI7~22aO~9tmV; RT="z=1&dm=baidu.com&si=d3c7e922-b3c7-439b-b8b6-3b29c91b9a80&ss=m0rs2lr6&sl=w&tt=mym&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2zgjw&ul=3vkbv"
"""

# 将Cookie字符串分割成单独的Cookie项
cookie_items = cookie_string.split('; ')

# 解析每个Cookie项，并创建一个适合Selenium的字典列表
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


browser = webdriver.Chrome()


browser.get('https://index.baidu.com/v2/index.html')


for cookie in cookies:
    try:
        browser.add_cookie(cookie)
    except Exception as e:
        print(f"无法添加cookie: {cookie['name']}, 错误: {e}")


browser.get('https://index.baidu.com/v2/main/index.html#/trend/000001?words=000001')


input("按回车键退出...")
