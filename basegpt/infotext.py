import json
import logging

import openai

from gpt.gpt import settings
import re

def start_generate(product, audience,platform,type):
    if product == 'GPT-3':

        openai.api_key = settings.OPENAI_API_KEY
        if audience == 'Developer':
            if platform == 'Python':
                if type == 'Code':
                    return 'import open'


# def read_stop_words_from_file(file_names):
#     stop_words = {}
#     for category, file_name in file_names.items():
#         with open(file_name, 'r', encoding='utf-8') as file:
#             words = set(file.read().lower().splitlines())
#             stop_words[category] = words
#     return stop_words
#
# def search_stop_words(text):
#     file_names = {
#         "Неопределенность": "неопределенность.txt",
#         "Оценки": "оценки.txt"
#     }
#     stop_words = read_stop_words_from_file(file_names)
#     text_words = set(text.lower().split())
#
#     result = {}
#     for category, words_set in stop_words.items():
#         found_words = words_set.intersection(text_words)
#         if found_words:
#             result[category] = list(found_words)
#
#     print(result)
#     return result


def read_stop_words_from_file(file_names):
    stop_words = {}
    for category, file_name in file_names.items():
        with open(file_name, 'r', encoding='utf-8') as file:
            words = [line.lower().strip() for line in file.readlines() if line.strip()]
            stop_words[category] = words
    return stop_words

def search_stop_words(text):
    file_names = {
        "Неопределенность": "неопределенность.txt",
        "Оценки": "оценки.txt",
        "Штампы": "штампы.txt",
        "Слабые" : "слабые.txt",
        "Усилители" : "усилители.txt",
        "Паразиты" : "паразиты.txt",
    }
    stop_words = read_stop_words_from_file(file_names)
    text = text.lower()

    result = {}
    category_count = {}
    for category, words_list in stop_words.items():

        found_words = []
        for word in words_list:
            search_result= re.findall(r'\b' + re.escape(word) + r'\b', text)
            if search_result:


                occurrences = len(search_result)
                category_count[category] = category_count.get(category, 0) + occurrences
                found_words.append(word)

        if found_words:
            result[category] = found_words

    # to json
    result = json.dumps(result, ensure_ascii=False)


    print(result, category_count)
    return result

search_stop_words('''Откройте мир идеального кофе с нашим идеального интернет-магазином. Здесь представлен широкий ассортимент кофе от ведущих мировых производителей. Каждый сорт кофе проходит тщательный отбор и проверку на соответствие стандартам качества. Покупателям доступны подробные описания и характеристики товаров, включая происхождение кофейных зерен, уровень обжарки и рекомендуемые способы заваривания. Мы предлагаем удобные способы доставки по всей стране. Наш интернет-магазин обеспечивает простоту и комфорт при выборе и покупке идеального кофе для дома или офиса.!''')