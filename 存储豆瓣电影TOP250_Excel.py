import requests
import openpyxl
from bs4 import BeautifulSoup

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'TOP250'
sheet['A1'] = '序号'
sheet['B1'] = '电影名'
sheet['C1'] = '评分'
sheet['D1'] = '推荐语'
sheet['E1'] = '电影链接'

for x in range(10):
    url = 'https://movie.douban.com/top250?start=' + str(x*25) + '&filter='
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'html.parser')
    movies = bs.find_all('div', class_="item")
    # print(movies[0])
    for movie in movies:
        num = movie.find('em', class_="").text
        #查找序号
        title = movie.find('span', class_="title").text
        #查找电影名
        if movie.find('span', class_="inq"):
            tes = movie.find('span', class_="inq").text
        else:
            tes = '暂无推荐语'

        #查找推荐语
        comment = movie.find('span', class_="rating_num").text
        #查找评分
        url_movie = movie.find('a')['href']
        #查找电影链接
        print(num + '.' + title + '——' + comment + '\n' + '推荐语：' + tes +'\n' + url_movie)
        a = [num,title,comment,tes,url_movie]
        sheet.append(a)

wb.save('豆瓣TOP250.xlsx')
