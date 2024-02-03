from typing import Iterable
import scrapy
from scrapy import Request

import re

from scrapy.http import Request

from ..items import RecipeItem

class MarmitonHomeSpider(scrapy.Spider):
    name = "marmiton_home"
    allowed_domains = ["marmiton.org"]
    start_urls = ["https://www.marmiton.org/recettes/index/categorie/aperitif-ou-buffet/", 
                  "https://www.marmiton.org/recettes/index/categorie/entree/",
                  "https://www.marmiton.org/recettes/index/categorie/plat-principal/",
                  "https://www.marmiton.org/recettes/index/categorie/dessert/"
                  ]

    def start_requests(self):
        for url in self.start_urls:
            for i in range(1,600):
                yield scrapy.Request(url+str(i), self.parse)

    def parse(self, response):
        recipes_links = {
            name:response.urljoin(url) for name, url in zip(
                response.css(".recipe-card").css(".recipe-card__title::text").extract(),
                response.css(".recipe-card").css(".recipe-card-link").css("a::attr(href)").extract()
            )
        }

        for link in recipes_links.values():
            yield Request(link, callback=self.parse_recipe)

    def parse_recipe(self, response):
        title = self.clean_spaces(response.css("h1::text").extract_first())

        rating = response.css(".recipe-header__rating-text::text").extract_first()
        
        count_comment_string = response.css("#recipe-reviews-list__container").css(".mrtn-recette_bloc-head-title").extract_first()
        count_comment = re.findall('\((.*?)\)', count_comment_string)[0]

        specs_selector = response.xpath('//div[@class="recipe-primary"]')
        preparation_time = specs_selector.xpath('//div[@class="recipe-primary__item"]/i[@class="icon icon-timer1"]/following-sibling::span[1]/text()').extract_first()
        difficulty = specs_selector.xpath('//div[@class="recipe-primary__item"]/i[@class="icon icon-difficulty"]/following-sibling::span[1]/text()').extract_first()
        price = specs_selector.xpath('//div[@class="recipe-primary__item"]/i[@class="icon icon-price"]/following-sibling::span[1]/text()').extract_first()

        count_portions = dict(
             number = response.css('.mrtn-recette_ingredients-counter::attr(data-servingsnb)').extract_first(),
             unit = response.css('.mrtn-recette_ingredients-counter::attr(data-servingsunit)').extract_first()
        )

        ingredients = []
        cards_ingredient = response.css(".card-ingredient")
        for card in cards_ingredient:
            quantity = card.css(".card-ingredient-quantity")

            ingredient = dict(
                count = quantity.css(".count::text").extract_first(),
                unit = quantity.css(".unit::attr(data-unitsingular)").extract_first(),
                name = self.clean_spaces(card.css(".ingredient-name::text").extract_first())
            )

            ingredients.append(ingredient)

        ustensils = []
        cards_ustensil = response.css(".card-utensil")
        for card in cards_ustensil:
            ustensil = self.clean_spaces(card.css(".card-utensil-quantity::text").extract_first())

            ustensils.append(ustensil)

        steps = []
        div_step = response.css(".recipe-step-list__container")
        count_step = 1

        for div in div_step:
            desc = self.clean_spaces(div.css("p::text").extract_first())

            step = dict(
                step = count_step,
                description = desc
            )

            steps.append(step)

            count_step += 1

        yield RecipeItem (
            title = title,
            rating = rating,
            count_comment = count_comment,
            preparation_time = preparation_time,
            difficulty = difficulty,
            price = price,
            count_portions = count_portions,
            ingredients = ingredients,
            ustensils = ustensils,
            steps = steps
        )

    def clean_spaces(self, string):
            if string:
                return " ".join(string.split())