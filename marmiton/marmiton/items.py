# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from traceback import print_exc
import scrapy
from scrapy import Item, Field

class RecipeItem(Item):
    #global data
    title = Field()
    rating = Field()
    count_comment = Field()

    #specific data
    preparation_time = Field()
    difficulty = Field()
    price = Field()
    count_portions = Field()
    ingredients = Field()
    ustensils = Field()
    steps = Field()
    
    ## TODO

    # commentaires # utilisateur, note, texte