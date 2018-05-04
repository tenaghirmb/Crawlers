# -*- coding: utf-8 -*-

# 下载根目录
ROOT_PATH = "/Volumes/SeagateBackupPlusDrive for BXY/Videos/hello_bi"

# 起始url地址
START_URL = 'https://edu.hellobi.com/course/explore?c1=32&page={page_no}'

# lesson list地址
COURSE_URL = 'https://edu.hellobi.com/course/{course_id}/lessons'

# 视频播放页面地址
LESSON_URL = 'https://edu.hellobi.com/course/144/play/lesson/{lesson_id}'

# 默认header
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,\
               application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# 获取lesson_id的header
# 需自定添加'Referer'
LESSON_LIST_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'pgv_pvi=5181074432; pgv_si=s7295301632; sqv__user_login=2M2WkI9cl3GabJlTn5HZ1MmlkaPEpcuXkmKUpMdVa17TxaWlqaDXncOWjJWcx5iUx2aWbJiZmnKanWptyW1nZpqVlGVqlJ5pnZ-X; remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6ImNcL2JTWkJHNEQySE95S0JVVm5CcVd3PT0iLCJ2YWx1ZSI6IjZcL3BUUXhLYVRLWlc5MjlydGdWUmM4VUtyMW40cUxiZ1BVdXFTZVZFRXYxRURsSG90NDRFaFJQQ2lXZDFyK05cL0NcL3poRG9FcFV4ZTBlSDF2VkloS0d5THpMS2xqNVwvN0NcL3JzQ1E3KzFkSzA9IiwibWFjIjoiZjcyOGU1MzFkNTJhMDQ0ZTZjNWNlYTc3OGVhNTM5M2Q5Njg3MTU5OGU1OGZiNzlkNzIxNzBjNjc2YjhmYzYwMyJ9; XSRF-TOKEN=eyJpdiI6Ilc1eFwvMWF6MUZHU1RVQjFjY3prSDFnPT0iLCJ2YWx1ZSI6IlJYVFdTS1RIWVd5eTRlRktYMTZ5QngrVVUwK3NnVDN4aEVFY2djdkVZTTkrVDZuczVyVWJsbUhWT3l2TDk4V0NkM2VLeGNnT2RST3F3Y0g3SVY5V1pRPT0iLCJtYWMiOiI1ZjY0ODU3ZjZlM2QxNWEwNDI4NDc3MDQwNzY3NTMxYWI3NzFiNzJhYmFiOWFjNDY4OTQwYWUxMzRjZmYzYzkwIn0%3D; laravel_session=eyJpdiI6IkRQYmdIelIrRzNSS0J2M0RUQ2ExWnc9PSIsInZhbHVlIjoiWlhnUXlPMmNMaG5rWlBwdGR6YmR6Y3BBXC9XaVVFRmJQcHljcVRsbHVQcVdpRFlNcVc3M2s1NVwvbWNQVXZsdmxRNXFldWY4bXBjeFFhVDdFY0s4b2lUZz09IiwibWFjIjoiYjlmMzM4NGVkNTAyZTlmNjgxZjZlODBlMDJmOTg0YjMyMGUxMTlmYmNiNTRjZDNhNDczOTA5ODJlNjg0YTRkOSJ9; pt_3fae31ac=uid=9Djpb4CFSAVwQx47BtyzFQ&nid=0&vid=-jgD5YzRDwzChi3oqLU9QQ&vn=20&pvn=20&sact=1493282108188&to_flag=0&pl=deOdJpSVVewuuuOM18mySQ*pt*1493282108188; pt_s_3fae31ac=vt=1493282108188&cad=',
    'DNT': '1',
    'Host': 'edu.hellobi.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}

# 请求视频的header
# 需自定添加'Referer'
VIDEO_HEADER = {
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'tsvideo.oss-cn-hangzhou.aliyuncs.com',
    'Pragma': 'no-cache',
    'Range': 'bytes=0-',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}
