import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.graph_objs as go
import plotly.io as pio

url = 'https://quotes.toscrape.com/'
base_url = 'https://quotes.toscrape.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
Author_list = []
Quote_list = []
Tag_list = []
for i in range(10):
    req = Request(url,headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage,'html.parser')
    divs = soup.findAll('div',attrs={'class':'quote'})
    for div in divs:
        quote = div.findAll('span')[0].text
        anthor = div.findAll('small')[0].text
        tags = div.findAll('div',attrs={'class':'tags'})[0].findAll('a')
        tag = []
        for a in tags:
            tag.append(a.text)
        Author_list.append(anthor)
        Quote_list.append(quote)
        Tag_list.append(tag)
    if i==9:
        continue
    url = base_url + soup.findAll('li',attrs={'class':'next'})[0].findAll('a')[0].get('href')

Author_dict = {}
for author in Author_list:
    if author in Author_dict:
        Author_dict[author] = Author_dict[author] + 1
    else:
        Author_dict[author] = 1
Author_dict_sort = sorted(Author_dict.items(), key=lambda x: x[1])
print()
print()
print('the number of quotes by each author:')
for k,v in Author_dict.items():
    print(f'author: {k}, number of quotes: {v}')
print(f'most quotes: {Author_dict_sort[-1][0]}, number of quotes: {Author_dict_sort[-1][1]}')
print(f'least quotes: {Author_dict_sort[0][0]}, number of quotes: {Author_dict_sort[0][1]}')
print()
print()

longest_index = 0
shortest_index = 0
longest,shortest = len(Quote_list[0]),len(Quote_list[0])
total_len = 0
for i in range(len(Quote_list)):
    len_now = len(Quote_list[i])
    if len_now>longest:
        longest = len_now
        longest_index = i
    if len_now<shortest:
        shortest = len_now
        shortest_index = i
    total_len += len_now

print(f'average length of quotes: {total_len/len(Quote_list)}')
print(f'longest quotes: {Quote_list[longest_index]}')
print(f'shortest quotes: {Quote_list[shortest_index]}')
print()
print()
tag_dict = {}
tag_num = 0
for tags in Tag_list:
    for tag in tags:
        tag_num += 1
        if tag in tag_dict:
            tag_dict[tag] = tag_dict[tag] + 1
        else:
            tag_dict[tag] = 1
tag_dict_sort = sorted(tag_dict.items(), key=lambda x: x[1])
        
print(f'total tags: {tag_num}, most popular tag is:{tag_dict_sort[-1][0]}, it\'s number is {tag_dict_sort[-1][1]}')

print()
print()

author_name = []
quote_num = []
for i in range(1,11):
    author_name .append(Author_dict_sort[-i][0])
    quote_num.append(Author_dict_sort[-i][1])
trace = go.Bar(x=author_name, y=quote_num, name='top 10 author')
layout = go.Layout(title='Quotes by Authors', xaxis=dict(title='authors'), yaxis=dict(title='Number of Quotes'))
fig = go.Figure(data=[trace], layout=layout)
pio.show(fig)

tag_name = []
tag_num = []
for i in range(1,11):
    tag_name.append(tag_dict_sort[-i][0])
    tag_num.append(tag_dict_sort[-i][1])
trace2 = go.Bar(x=tag_name, y=tag_num, name='top 10 tag')
layout2 = go.Layout(title='Most Popular Tags by Authors', xaxis=dict(title=''), yaxis=dict(title='Count'))
fig = go.Figure(data=[trace2], layout=layout2)
pio.show(fig)