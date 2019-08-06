import requests
import smtplib
import schedule
import time
import csv, random
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

account = '2775083310@qq.com'
password = 'dhxjwtnefadfdece'
receiver = '18339265510@163.com'

#这是爬取豆瓣电影Top250
def movies():
    for x in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(x*25) + '&filter='
        res = requests.get(url)
        bs = BeautifulSoup(res.text, 'html.parser')
        bs = bs.find('ol', class_="grid_view")
        list = []
        for titles in bs.find_all('li'):
            title = titles.find('span', class_="title").text
            list.append(title)
    slice = random.sample(list, 3)
    # return slice

    movies_list = []
    for movie_name in slice:
        url = 'https://www.btbtdy.me/search/'+movie_name+'.html'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        item = soup.find('strong')
        if item != None:
            iteml = item.find('a', title=movie_name)['href']
            urll = 'https://www.btbtdy.me'+iteml
        else:
            urll = '本站没有该片资源'
        m_k = [movie_name, urll]
        movies_list.append(m_k)
    m_link_str = str(movies_list)
    return m_link_str

def send_email(m_link_str):
    global account,password,receiver
    mailhost='smtp.qq.com'
    qqmail = smtplib.SMTP()
    qqmail.connect(mailhost,25)
    qqmail.login(account,password)
    content= m_link_str
    message = MIMEText(content, 'plain', 'utf-8')
    subject = '本周推荐电影TOP3'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        qqmail.sendmail(account, receiver, message.as_string())
        print ('邮件发送成功')
    except:
        print ('邮件发送失败')
    qqmail.quit()

def job():
    print('开始一次任务')
    m_link_str = movies()
    send_email(m_link_str)
    print('任务完成')

schedule.every().day.at("21:11").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
