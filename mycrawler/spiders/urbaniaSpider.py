
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import time
from random import uniform
import logging

logging.basicConfig(
    filename='logs/spider.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

class Departamento(Item):
    nombre = Field()
    direccion = Field()

class UrbaniaSpider(CrawlSpider):
  handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
  name = 'UrbaniaSpider'

  # Establecemos la configuracion del spider
  custom_settings = {
    'LOG_FILE': 'archive/UrbaniaSpider.log',
    'LOG_LEVEL': 'INFO',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'logs/urbania.csv',
    'DOWNLOAD_DELAY': 3,
    'USER_AGENT': 'MiSpider1/1.0 (+https://miweb.com)',
  }

  # Establecemos las url del sitio
  start_urls = [
    'https://urbania.pe/buscar/proyectos-propiedades?page=1',
    'https://urbania.pe/buscar/proyectos-propiedades?page=2'
  ]

  # Seleccionamos los dominios permitidos 
  allowed_domains = ['urbania.pe']
  download_delay = 1

  # Generamos las reglas para los scrolling
  rules = (
      Rule(
          LinkExtractor(
              allow=r'/proyecto/',
          ), follow=True, callback='parse_depa'),
  )

  def parse_depa(self, response):
    sel = Selector(response)

    # Se cargan los campos
    item = ItemLoader(Departamento(),sel)

    # Se establecen los XPath del texto
    item.add_xpath('nombre','//*[@id="article-container"]/h1/text()')
    item.add_xpath('direccion','//*[@id="ref-map"]/text()')

    # Cargamos los item capturados
    departamento = item.load_item()

    # Limpiamos la respuesta
    nombre = departamento['nombre'][0].strip() if departamento['nombre'] else ''
    direccion = departamento['direccion'][0].strip() if departamento['direccion'] else ''

    # Generamos log de la captura
    logging.info(f"Departamento: {nombre}, Dirección: {direccion}")

    # Esperamos para simular peticiones humanas
    time.sleep(uniform(1, 3))

    # Retornamos la linea para el archivo
    return {'nombre': nombre, 'direccion': direccion}