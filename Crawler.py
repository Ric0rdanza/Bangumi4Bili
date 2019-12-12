import requests
import json
import re
from bs4 import BeautifulSoup

season = ['1', '4', '7', '10']
part1 = 'https://api.bilibili.com/pgc/season/index/result?season_version=1&area=2&is_finish=-1&copyright=-1&season_status=-1&season_month='
part2 = '&year=-1&style_id=-1&order=4&st=1&sort=0&page='
part3 = '&season_type=1&pagesize=20&type=1'

max_page = 50
VideoLink = []
Score = []
Title = []
BangumiLink = []
Cast = []
Staff = []


for s in range(len(season)):
    VideoLink.clear()
    Score.clear()
    Title.clear()
    BangumiLink.clear()
    Cast.clear()
    Staff.clear()
    breakflag = 0
    for i in range(1, max_page + 1):
        season_url = part1 + season[s] + part2 + str(i) + part3
        html = requests.request('get', season_url)
        jx = json.loads(html.text)
        for j in range(len(jx['data']['list'])):
            if jx['data']['list'][j]['order'] != '':
                VideoLink.append(jx['data']['list'][j]['link'])
                Score.append(float(jx['data']['list'][j]['order'][0: -1]))
                Title.append(jx['data']['list'][j]['title'])
                print(jx['data']['list'][j]['order'])
            else:
                breakflag = 1
                break
        if breakflag == 1:
            break

    print(len(VideoLink))
    print(len(Score))
    print(len(Title))

    for i in range(len(VideoLink)):
        video_url = VideoLink[i]
        html = requests.request('get', video_url)
        soup = BeautifulSoup(html.text, 'lxml')
        x = soup.find(name = 'a', class_ = "media-cover")
        try:
            print(x['href'])
            BangumiLink.append('https:' + str(x['href']))
        except:
            print('FALSE')
            BangumiLink.append('FALSE')

    print(len(BangumiLink))
    '''
    driver = webdriver.Edge()

    for b in range(len(BangumiLink)):
        bangumi_url = BangumiLink[b]
        driver.get(bangumi_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        x = soup.find_all(name = 'span', class_ = '')
        print(x)
        print(len(x))
        Cast.append(list(x))
        Staff.append(x)
        x.clear()
    driver.quit()
    '''
    
    for b in range(len(BangumiLink)):
        bangumi_url = BangumiLink[b]
        if bangumi_url == 'FALSE':
            Cast.append('FALSE')
            Staff.append('FALSE')
            continue
        else:
            html = requests.request('get', bangumi_url)
            soup = BeautifulSoup(html.text, 'lxml')
            x = soup.find(name = 'script', string = re.compile('window.__INITIAL_STATE__'))
            x = str(x)
            cast_start = x.find('"actors":')
            cast_end = x.find(',', cast_start)
            staff_start = x.find('"staff":')
            staff_end = x.find(',', staff_start)
            print(x[cast_start: cast_end].replace('\\n', ',').replace('\\u002F', '/'))
            Cast.append(x[cast_start: cast_end].replace('\\n', ',').replace('\u002F', '/'))
            print(x[staff_start: staff_end].replace('\\n', ',').replace('\\u002F', '/'))
            Staff.append(x[staff_start: staff_end].replace('\\n', ',').replace('\\u002F', '/'))


    print(len(Cast))
    print(len(Staff))

    with open('./Title' + str(s) + '.txt', 'w', encoding = 'utf-8') as ftitle:
        for i in range(len(Title)):
            ftitle.writelines(Title[i] + '\n')
    with open('./Score' + str(s) + '.txt', 'w', encoding = 'utf-8') as fscore:
        for i in range(len(Score)):
            fscore.writelines(str(Score[i]) + '\n')
    with open('./Cast' + str(s) + '.txt', 'w', encoding = 'utf-8') as fcast:
        for i in range(len(Cast)):
            fcast.writelines(str(Cast[i]) + '\n')
    with open('./Staff' + str(s) + '.txt', 'w', encoding = 'utf-8') as fcast:
        for i in range(len(Cast)):
            fcast.writelines(str(Staff[i]) + '\n')