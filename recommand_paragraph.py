import requests
import bs4
import pandas as pd
import os
import glob
import pathlib
import tkinter as tk



def show_paragraph_on_tkinter():
    baseurl = 'https://tw.voicetube.com/'
    html = requests.get(baseurl)
    sp = bs4.BeautifulSoup(html.text, 'lxml')
    datas1 = sp.find_all('h5', class_='index-thumbnail-title')[i]

    # 建立影片網址變數
    new_vedio = datas1.a['href']
    new_vedio_url = baseurl + new_vedio

    root = requests.get(new_vedio_url).text
    soup = bs4.BeautifulSoup(root, 'lxml')

    datas = soup.find_all('div', class_='captions')

    # 將網路文章寫入資料庫
    df = []
    for data in datas:
        # 只返回英文字幕（有中英文）
        edata = data.text.strip().split('\n')[0]
        df.append(edata)

    df = ' '.join(df)
    if df!="":
        label3.config(text = df)
    else:
        label3.config(text = '網路出現問題')


def show_title():
    # 搜尋還沒有在資料庫文章中出現過的Voicetube文章
    baseurl = 'https://tw.voicetube.com/'
    html = requests.get(baseurl)
    sp = bs4.BeautifulSoup(html.text, 'lxml')
    datas1 = sp.find_all('h5', class_='index-thumbnail-title')[i]
    datas2 = sp.find_all('h5', class_='index-thumbnail-title')[i+1]
    datas3 = sp.find_all('h5', class_='index-thumbnail-title')[i+2]

    # 建立影片網址變數
    new_vedio = datas1.a['href']
    new_vedio_url = baseurl + new_vedio

    # 建立影片Title變數
    title1 = datas1['title'].strip()
    title2 = datas2['title'].strip()
    title3 = datas3['title'].strip()

    label1.config(text = title1)

# 推薦Voicetube的文章於資料庫

def create_paragraph():
    print(str(i)+'-2')
    # 搜尋還沒有在資料庫文章中出現過的Voicetube文章
    baseurl = 'https://tw.voicetube.com/'
    html = requests.get(baseurl)
    sp = bs4.BeautifulSoup(html.text, 'lxml')
    datas1 = sp.find_all('h5', class_='index-thumbnail-title')[i]


    # 建立影片網址變數
    new_vedio = datas1.a['href']
    new_vedio_url = baseurl + new_vedio

    # 建立影片Title變數
    title1 = datas1['title'].strip()

    # 建立資料庫單字串列
    vpath = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Vacabulary/Vacabulary.xlsx'
    vdf = pd.read_excel(vpath)
    vdf = vdf.iloc[:,0]
    vdf = vdf.values

    # 建立文章路徑
    file_dir = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Article'
    exists_file_n = len(glob.glob(file_dir+'/'+'*'+'.xlsx'))
    file_name = "{}_{}".format(exists_file_n+1,title1+'.xlsx')
    file_path = os.path.join(file_dir,file_name)


    #搜尋目標影片字幕
    url = new_vedio_url
    try:
        root = requests.get(url).text
        soup = bs4.BeautifulSoup(root, 'lxml')
        datas = soup.find_all('div', class_='captions')


        # 將網路文章寫入資料庫
        df = []
        for data in datas:
            edata = data.text.strip().split('\n')[0]
            df.append(edata)
        if df!=[]:
            print('新增成功！')
            df = pd.DataFrame(df,columns=['句子'])
            df.to_excel(file_path,index=0)
        else:
            print('搜尋沒有結果')
    except:
        print('sthwrong2')


i=0
n=0
def check_paragraph():
    global n
    global i

    # 以串列傳回資料庫每篇文章標題
    file_dir = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Article'
    exist_file_name = glob.glob(file_dir + '/*.xlsx')
    file_stem = list(map(lambda x: pathlib.Path(x).stem.split('_')[1], exist_file_name))

    # 傳回Voictube第一篇文章標題
    baseurl = 'https://tw.voicetube.com/'
    html = requests.get(baseurl)
    sp = bs4.BeautifulSoup(html.text, 'lxml')
    data = sp.find_all('h5', class_='index-thumbnail-title')[0]['title']
    title = data.strip()

    # 檢查Voicetube文章是否有在資料庫文章\

    if title not in file_stem:
        print(title)
        create_paragraph()

    else:
        while True:
            i += 1
            print(str(i)+'-1')
            baseurl = 'https://tw.voicetube.com/'
            html = requests.get(baseurl)
            sp = bs4.BeautifulSoup(html.text, 'lxml')
            data = sp.find_all('h5', class_='index-thumbnail-title')[i]['title']
            title = data.strip()
            if title not in file_stem:
                # print('這篇還沒看過喔！'.format(title))
                try:
                    create_paragraph()
                    break
                except:
                    print('sthwrong1')


def add():
    show_title()
    show_paragraph_on_tkinter()
    check_paragraph()



# 根視窗
root=tk.Tk()
root.geometry("1000x700")  #設定主視窗解析度
root.title("VacabularyKing")

btnAdd = tk.Button(root, text="Add", command=add)
btnAdd.place(x=20,y=40)

label1 = tk.Label(root, text='', wraplength=600, justify='left')
label1.place(x=150, y=40)

label3 = tk.Label(root, text="",wraplength=600,justify='left')
label3.place(x=150, y=80)


root.mainloop()