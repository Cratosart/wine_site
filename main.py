import datetime
import pandas
import collections


excel_data_wine = pandas.read_excel('wine3.xlsx',na_values=['nan', 'None'], keep_default_na=False)
dict_wine = excel_data_wine.to_dict(orient='records')

production_dict = collections.defaultdict(list)
for wine in dict_wine:
    production_dict[wine['Категория']].append(wine)


from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

event1 = datetime.datetime(year=1920, month=12, day=12, hour=1)
formatted_date_1 = event1.strftime('%Y')
event2 = datetime.datetime.today()
formatted_date_2 = event2.strftime('%Y')
year_time = int(formatted_date_2)-int(formatted_date_1)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    time_found=f'Уже {year_time} год с вами',
    production_dict=production_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
