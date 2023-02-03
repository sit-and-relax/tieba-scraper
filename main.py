import re
from fake_useragent import UserAgent
import requests, csv, os

print(
    '为防止造成大量访问量，影响贴吧的运行，本功能仅会读取极少一部分帖子和评论，在正常使用中百度贴吧方也设置了访问频率，让我们一起维护网络的安全与健康！本程序仅供研究使用，请勿使用本程序损害任何方的利益！')
ua = UserAgent()
useragent = ua.random
# print(ua.random)
# keyword = '文学'
keyword = input('请输入贴吧名（不需要带"吧"，如文学吧输入"文学"）:')
for page in range(1,11):
    print(f'page {page}/10')
    text = requests.get(url=f'https://tieba.baidu.com/f?kw={keyword}&ie=utf-8&pn={(page-1)*50}',
                        headers={'User-Agent': useragent, 'Referer': r'https://wappass.baidu.com/','sec-ch-ua-platform':'"Windows"'}).text
    print(text)
    alct = re.findall('<a rel="noopener" href="/p/.*?</a>', text)
    if len(alct) == 0:
        print('你操作频率太快啦！等一下再试吧~')
        exit(114514)
    # print(alct)
    data = []
    for i in range(len(alct)):
        alct[i] = alct[i].replace('8u', '你').replace('吧友', '你').replace('吧u', '你').replace('8友', '你')
        data.append([re.findall('title=".*?"', alct[i])[0][7:-1], re.findall('href="/p/.*?"', alct[i])[0][6:-1]])
    print(data)
    for i in range(len(data)):
        dt = requests.get(url=f'https://tieba.baidu.com{data[i][1]}', headers={'User-Agent': useragent,
                                                                               'Referer': f'https://tieba.baidu.com/f?kw={keyword.encode("utf-8").decode("latin1")}&ie=utf-8'}).text
        # print(dt)
        part = re.findall(r'l_post l_post_bright j_l_post clearfix.*?core_reply j_lzl_wrapper', dt,re.S)
        print(part)
        real_det = []
        if len(part) == 0:
            print('你操作频率太快啦！等一下再试吧~')
            exit(114515)
        for j in range(len(part)):
            det = re.findall('<div id="post_content_.*?</div>', part[j],re.S)[0]
            det = re.findall('>.*</div>', det)[0][1:-6].replace('<br>', '\n').lstrip()
            if '<' in det and '>' in det:
                index = 0
                flag = 0
                while index < len(det):
                    if det[index] == '<' or flag == 1:
                        flag = 1
                        det = det[:index] + det[index + 1:]
                        if det[index] == '>':
                            det = det[:index] + det[index + 1:]
                            flag = 0
                    else:
                        index += 1
            det = det.strip('\n')
            cmt = re.findall('<span class="lzl_content_main".*?</span>', part[j],re.S)
            # print(cmt)
            cmtlist = []
            for k in cmt:
                cmtlist.append(re.findall('>.*</span>', k)[0][1:-7].replace('<br>', '\n').strip('\n'))
            det = [det, cmt]
            # print(det)
            if not det == '':
                real_det.append(det)
                print(f'->{j}/{len(det)}')
        # print(real_det)
        data[i].append(real_det)
        print(f'{i}/{len(data)}')
    print(data)
    with open('train_lccc.csv', 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f, delimiter='\t')
        for i in data:
            for j in i[2]:
                writer.writerow([i[0], j[0], 1])
                for k in j[1]:
                    writer.writerow([j[0], k, 1])
