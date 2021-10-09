from bs4 import BeautifulSoup
import requests
import re
def hotline_parser(prod_req):

	url = 'https://hotline.ua/'
	headers = {'user-agent': 'my-app/0.0.1'}
	payload = {'q': prod_req}
	r = requests.get((url + 'sr/'), params=payload, headers=headers)

	soup = BeautifulSoup(r.text,"lxml")

	product_link = soup.find('a', class_='item-img-link')

	try:
		product_url = (url + product_link.get('href'))
		r = requests.get(product_url, headers=headers)
		soup = BeautifulSoup(r.text,"lxml")
		vaule_html = soup.findAll('span', class_='value')
		name = soup.find('h1', datatype="card-title")
		price_with_name = name.text+'\n'+vaule_html[4].text+' грн'
		return price_with_name
	except AttributeError as a:
		try:
			vaule_html = soup.findAll('span', class_="price__value")
			name = soup.find('h1', class_="title__main")
			price_with_name =name.text+'\n'+vaule_html[0].text+'-'+vaule_html[10].text+' грн'
			
			return price_with_name
		except AttributeError as a:
			return 'error'
			#eturn str(a)
def get_wether(city='odessa', country='UA'):
	r = requests.get(url = f'http://api.openweathermap.org/data/2.5/find?q={city},{country}&lang=en&country=UAtype=like&units=metric&APPID=498f58d071127216ae2015b857c4dcae')
	info_main = r.json()
	try:
		info = info_main['list'][0]
	except IndexError:
		return 'error'
	temp = round(info['main']['temp'])
	name = info['name']+','+info['sys']['country']
	weather_type = info['weather'][0]['description']
	all = f'{name}\n{weather_type}\nTemperature: {temp}°C\n'
	return all
def get_btc(value=1):
	r = requests.get('https://blockchain.info/ticker')
	info = r.json()
	price_btc_USD = info['USD']['last']*value
	r = requests.get(f'https://www.xe.com/currencyconverter/convert/?Amount={price_btc_USD}&From=USD&To=UAH')
	price_btc_USD = str('{0:,}'.format(round(price_btc_USD))).replace(',', ' ')+' USD'
	soup = BeautifulSoup(r.text, 'lxml')
	soup = soup.find('p', class_="result__BigRate-sc-1bsijpp-1 iGrAod")
	price_btc_UAH = re.sub(' Ukrainian Hryvni','',soup.text)
	price_btc_UAH = '{0:,}'.format(round(float(re.sub(',','',price_btc_UAH)))).replace(',', ' ') + ' UAH'
	price_btc_all = f'{value} BTC\n{price_btc_USD}\n{price_btc_UAH}'
	return price_btc_all


