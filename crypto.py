import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


url = 'https://coinmarketcap.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url,headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage,'html.parser')

coins = soup.findAll('tr',attrs={'style':'cursor:pointer'})
for coin in coins[:5]:
    tds = coin.findAll('td')
    ps = tds[2].findAll('p')
    spans = tds[5].findAll('span')
    increaceOrnot = spans[1]['class']

    coin_name = ps[0].text
    coin_sign = ps[1].text
    prince_now = tds[3].text
    prince_now_float = float(prince_now.strip('$').replace(',',''))
    change24h_float = float(tds[5].text.strip('%'))/100
    if 'icon-Caret-up' in increaceOrnot:
        change24h_float = float(tds[5].text.strip('%'))/100
    else:
        change24h_float = -float(tds[5].text.strip('%'))/100
    corresponding_price = prince_now_float/(1+change24h_float)


    print(f'name: {coin_name}, symbol: {coin_sign}, current_price: {prince_now}, change24h: {change24h_float*100}%, corresponding_price: ${corresponding_price:,.2f}')