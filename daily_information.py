
# 每日資訊
import requests
import bs4

def Voicetube():
    baseurl = 'https://tw.voicetube.com/'

    html = requests.get(baseurl)

    sp = bs4.BeautifulSoup(html.text,'lxml')
    data = sp.find('h5',class_='index-thumbnail-title')

    new_vedio = data.a['href']
    new_vedio_url = baseurl+new_vedio

    title = data.text.strip()
    new_v = "{}\n{}".format(title,new_vedio_url)
    try:
        return new_v
    except:
        return 'Voicetube Vedio發生問題'

def pythonNewslist():
    baseurl = 'https://www.google.com/search?q=python&safe=active&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjFr8WJuebrAhWIBKYKHe9LDD4QpwUIJQ&biw=1250&bih=648&dpr=2.2'
    html = requests.get(baseurl)
    sp = bs4.BeautifulSoup(html.text, 'html.parser')

    infos = sp.find_all('div',class_='kCrYT')

    pythonNewslist=[]
    for i in infos:
        title = i.find('div',class_='BNeawe vvjwJb AP7Wnd')
        href = i.find('a')
        time = sp.find('span',class_='r0bn4c rQMQod').text
        if title!=None:
            h = href['href'].split('=',1)[1]
            h = h.split('&')[0]
            pythonNewslist.append("{}\n{}\n{}".format(title.text,h,time))
    try:
        return pythonNewslist[0]
    except:
        return 'pythonNews發生問題'


def NHkNews():
    html = requests.get('https://www.youtube.com/results?search_query=nhk+%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9+%E3%81%8A%E3%81%AF%E3%82%88%E3%81%86%E6%97%A5%E6%9C%AC&sp=EgIIAg%253D%253D')
    nhk_news_url = html.url
    try:
        return nhk_news_url
    except:
        return 'NHK_News發生問題'

def Notify():
    API = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': "Bearer" + ' ' + 'dh82uCyzUqcM9TNR9Q9zUfaZUoU347WTPtqFi76HDmv',
               'Content-Type': "application/x-www-form-urlencoded"}
    payload = {'message':"\n\n＊ Voicetube ＊\n{}\n\n＊ Recent Python News ＊\n{}\n\n＊ NHK News ＊\n{}".format(Voicetube(),pythonNewslist(),NHkNews())}
    requests.post(API, headers=headers, params=payload)



