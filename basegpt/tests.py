from django.test import TestCase

from rest_framework.test import APIClient

from django.urls import reverse




class TestInfotext(TestCase):


    # variants of input data list of dictionaries

# цикл для проверки разных входных данных

    def test_infotext_post(self):
        input_data = [
            {
                "rawtext": "Интернет магазин продажи кофе",
                "type": "short",
            }, {
                "rawtext": "Интернет магазин продажи кофе",
                "type": "long",
            },

            {

                "rawtext": "Интернет магазин продающий одежду, скидки с 20 мая, летняя коллекция",
                "type": "short",
            }, {

                "rawtext": "Интернет магазин продающий одежду, скидки с 20 мая, летняя коллекция",
                "type": "long",
            },

            {
                "rawtext": "Тг канал с курсами по программированию, курс по питону, курс по джанго, курс по фронтенду",
                "type": "short",
            }, {
                "rawtext": "Тг канал с курсами по программированию, курс по питону, курс по джанго, курс по фронтенду",
                "type": "long",
            },

            {
                "rawtext": "интернет магазина о продажи детских товаров. Описание: игрушки, одежда, все необходимое для ребенка.  Скдики до 20 процентов до 4 мая",
                "type": "short",
            }, {
                "rawtext": "интернет магазина о продажи детских товаров. Описание: игрушки, одежда, все необходимое для ребенка.  Скдики до 20 процентов до 4 мая",
                "type": "long",
            }
            # ,
            #         {
            #             "rawtext":" интернет магазина о продаже электронной техники 'TeStore'. Продаются смартфоны, ноутбуки и тд. Большой выбор, На Samsung скидки до 20 апреля до 30 процентов. Доставка домой или в пункт выдачи. ",
            #             "type": "short",
            #
            #         },{
            #             "rawtext":" интернет магазина о продаже электронной техники 'TeStore'. Продаются смартфоны, ноутбуки и тд. Большой выбор, На Samsung скидки до 20 апреля до 30 процентов. Доставка домой или в пункт выдачи. ",
            #             "type": "long",
            #
            #         },
            #         {
            #             "rawtext": "Интернет-магазин продажи электронных книг. Различные жанры: фантастика, учебники, бизнес-литература.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин продажи электронных книг. Различные жанры: фантастика, учебники, бизнес-литература.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин с косметикой. Продукция для ухода за кожей, декоративная косметика, новинки от ведущих брендов.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин с косметикой. Продукция для ухода за кожей, декоративная косметика, новинки от ведущих брендов.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Сайт с курсами по искусству. Обучение рисованию, скульптуре, цифровому искусству, доступны видеоуроки и мастер-классы.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Сайт с курсами по искусству. Обучение рисованию, скульптуре, цифровому искусству, доступны видеоуроки и мастер-классы.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин автоаксессуаров. Автомобильные коврики, чехлы для сидений, автоэлектроника. Продажа и доставка.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин автоаксессуаров. Автомобильные коврики, чехлы для сидений, автоэлектроника. Продажа и доставка.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин смартфонов",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин смартфонов",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Онлайн магазин спортивного питания",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Онлайн магазин спортивного питания",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Платформа для продажи ручного инструмента",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Платформа для продажи ручного инструмента",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Сайт по продаже домашних растений",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Сайт по продаже домашних растений",
            #             "type": "long"
            #         }
            #         ,
            #         {
            #             "rawtext": "Интернет-магазин женской одежды. Предлагает платья, верхнюю одежду, аксессуары.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин женской одежды. Предлагает платья, верхнюю одежду, аксессуары.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Онлайн-магазин мебели. Продажа офисной и домашней мебели.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Онлайн-магазин мебели. Продажа офисной и домашней мебели.",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Платформа продажи аудиокниг. Большой выбор жанров и авторов.",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Платформа продажи аудиокниг. Большой выбор жанров и авторов.",
            #             "type": "long"
            #         }
            # ,
            #         {
            #             "rawtext": "Интернет-магазин офисных принадлежностей",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Интернет-магазин офисных принадлежностей",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Онлайн-площадка для покупки компьютерных игр",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Онлайн-площадка для покупки компьютерных игр",
            #             "type": "long"
            #         },
            #         {
            #             "rawtext": "Сайт по продаже велосипедов",
            #             "type": "short"
            #         },
            #         {
            #             "rawtext": "Сайт по продаже велосипедов",
            #             "type": "long"
            #         }

        ]
        client = APIClient()

        for i in input_data:
            response = client.post('/adtext/', i)
            self.assertEqual(response.status_code, 200)