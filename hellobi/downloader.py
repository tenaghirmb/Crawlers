# -*- coding: utf-8 -*-
import requests
from lxml import html
import logging
from multiprocessing import Pool, cpu_count
import settings
import os
import re

# logger配置
sformat = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(filename='hello_bi.log', format=sformat,
                    datefmt='%a, %d %b %Y %H:%M:%S', level=logging.INFO)
console = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(console)


# 视频下载
def download_video(url, course_title, lesson_name, header):
    change_path(course_title)
    if(os.path.isfile(lesson_name + '.mp4')):
        logger.debug('### 已经存在 ' + course_title + '-' + lesson_name)
    else:
        logger.debug('开始下载' + course_title + '-' + lesson_name)
        r = requests.get(url, headers=header)
        with open(lesson_name + '.mp4', 'wb') as f:
            f.write(r.content)
            logger.info(course_title + '-' + lesson_name + ' 保存成功')


# 名称标准化
def format_name(name):
    return name.replace('：', '-').strip()\
        .replace('/', '_').replace('<', '(')\
        .replace('>', ')').replace('|', '-')


# 变更路径
def change_path(course_title):
    dest = os.path.join(settings.ROOT_PATH, course_title)
    if os.path.exists(dest):
        pass
    else:
        os.mkdir(dest)
        logger.info('创建课程文件夹' + course_title)
    os.chdir(dest)
    logger.debug('切换当前路径至' + dest)


# 获取course id
def get_course_id(pno):
    temp_url = settings.START_URL.format(page_no=str(pno))
    charge_course = requests.get(temp_url)
    charge_list = html.fromstring(charge_course.text)
    course_ids = charge_list.xpath('//h3/a[@href]')
    for cid in course_ids:
        get_id = cid.get('href').split('/')[-1]
        yield get_id


# 获取lesson id
def get_lesson_id(course_id):
    url = settings.COURSE_URL.format(course_id=course_id)
    header = settings.LESSON_LIST_HEADER
    header['Referer'] = url.strip('/lessons')
    lesson_list = requests.get(url, headers=header)
    tree = html.fromstring(lesson_list.text)
    t_title = tree.xpath('//li[@class="active"]')[0].text
    course_title = course_id + '-' + format_name(t_title)
    lessons = tree.cssselect('li.period.lesson-item')
    for lesson in lessons:
        lesson_id = lesson.get('data-id')
        logger.debug('获取到lesson id ' + lesson_id)
        t_lesson_name = lesson.cssselect('span.title')[0].text
        lesson_name = format_name(t_lesson_name)
        video_url = get_video_url(lesson_id, header)
        if video_url:
            if(re.match('https://o7dgrypba.qnssl.com', video_url)):
                my_header = settings.DEFAULT_REQUEST_HEADERS
            else:
                my_header = settings.VIDEO_HEADER
                my_header['Referer'] = settings.LESSON_URL.format(
                    lesson_id=lesson_id)
            yield download_video(video_url, course_title,
                                 lesson_name, my_header)


# 获取视频地址url
def get_video_url(lesson_id, header):
    url = settings.LESSON_URL.format(lesson_id=lesson_id)
    temp = requests.get(url, headers=header)
    logger.debug('正在解析获取视频地址' + url)
    try:
        video_url = 'https' + \
            re.search('url: "https(.*?)"', temp.text).group(1)
        logger.debug('获取到视频地址' + video_url)
    except AttributeError:
        video_url = None
        logger.warn('lesson ' + lesson_id + '还没有视频地址')
    return video_url


# 生成器调用
def distribute(pno):
    for cid in get_course_id(pno):
        logger.debug('获取到课程号' + cid)
        for mission in get_lesson_id(cid):
            mission


# 主函数 按课程页多进程
def main():
    logger.info('--------------------爬虫开始运行--------------------')
    cpu_num = cpu_count()
    pool = Pool(processes=cpu_num)
    pool.map(distribute, list(range(1, 6)))
    pool.close()
    pool.join()
    logger.info('--------------------爬虫运行完毕--------------------')


if __name__ == '__main__':
    main()
