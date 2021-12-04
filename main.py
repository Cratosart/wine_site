import collections
import datetime
import pandas
import argparse

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', help="Путь к файлу", default='wine.xlsx')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

    wines = pandas.read_excel(f'{namespace.n}', na_values=['nan', 'None'], keep_default_na=False).to_dict(
        orient='records')
    production = collections.defaultdict(list)

    for wine in wines:
        production[wine['Категория']].append(wine)

    year_foundation = 1920
    winery_age = datetime.datetime.today().year - year_foundation

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age=f'Уже {winery_age} год с вами',
        production=production
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
