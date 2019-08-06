import requests
import openpyxl

link = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/')
#先用requests下载链接。
js_link = link.json()
#解析下载得到的内容。
bianhao = int(input('''请输入你选择的词库编号，按Enter确认
1，GMAT  2，考研  3，高考  4，四级  5，六级
6，英专  7，托福  8，GRE  9，雅思  10，任意
>'''))
#让用户选择自己想测的词库，输入数字编号。int()来转换数据类型
ciku = js_link['data'][bianhao-1][0]

headers = {
'cookie': '__utmc=183787513; csrftoken=F6Ht6kO47EuUe4M6uoSoOJ04oZqNTxtL; __utmz=183787513.1564874705.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=183787513.319299905.1564874225.1564874705.1564878503.3',
'pragma': 'no-cache',
'referer': 'https://www.shanbay.com/vocabtest/',
'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}

params={
'category': ciku,
'_':'1564880550122'
}

url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/?'

req = requests.get(url, headers=headers, params=params)
print(req.status_code, '\n')
word_data = req.json()['data']
# print(req.json())
words_knows = []
knows_index = []
not_knows = []
mii = 1
for word in word_data[:5]:
    print('\n第%d个单词:' % mii, word['content'])
    s = input('认识请敲空格，否则敲Enter：')
    if s == ' ':
        words_knows.append(word['content'])
        knows_index.append(word_data.index(word))
    else:
        not_knows.append(word['content'])
    mii += 1
# print('认识%i个' % (len(words_knows)), '\n', '分别为：', '\n', words_knows)
# print('\n', knows_index, '\n')

word_right = []
word_error = {}

for ki in knows_index:
    word_object = word_data[ki]['content']
    word_means = word_data[ki]['definition_choices']
    means = word_data[ki]['pk']

    print('\n', word_object+'的意思是以下哪一个？')
    number_word = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    word_number = {'A': 0, 'B': 1, 'C': 2, 'D':3}
    for wm in word_means:
        print(number_word[word_means.index(wm)] + ':' + wm['definition'])
        if means == wm['pk']:
            w_r_m = wm['definition']

    print('\n')
    w_mb = input('你的选择是：')
    w_mm = word_number[w_mb]
    w_pk = word_means[w_mm]['pk']

    if w_pk == means:
        word_right.append(word_object)
        print('\n', 'You are smart!!', '\n')
    else:
        word_error[word_object] = w_r_m
        print('\n', 'it is wrong!!', '\n')

print('\n', '认识的单词个数：'+str(len(words_knows)))
print('不认识的单词个数：'+str(50-len(words_knows)))
print('掌握的单词个数：'+str(len(word_right)))
print('错误的单词个数：'+str(len(word_error)))

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = '错的单词'

sheet.append(['序号','单词','正确的意思'])

i = 1
for key in word_error:
    sheet.append([i,key,word_error[key]])
    i += 1
wb.save('扇贝单词错题集.xlsx')

