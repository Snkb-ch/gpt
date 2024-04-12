import json
import logging

import openai


import re
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

from .prompts import *



def read_stop_words_from_file(file_names):
    stop_words = {}
    for category, file_name in file_names.items():
        with open(file_name, 'r', encoding='utf-8') as file:
            words = [line.lower().strip() for line in file.readlines() if line.strip()]
            stop_words[category] = words
    return stop_words

def search_stop_words(text):
    file_names = {
        "Неопределенность": "static/неопределенность.txt",
        "Оценки": "static/оценки.txt",
        "Штампы": "static/штампы.txt",
        "Слабые" : "static/слабые.txt",
        "Усилители" : "static/усилители.txt",
        "Паразиты" : "static/паразиты.txt",
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
    count_all = sum(category_count.values())
    procent = 0
    if count_all:
        procent = count_all / len(text.split()) * 100
    # count all as x1 but for оценка x2 and sum all
    score = 0
    for category, count in category_count.items():
        if category == 'Оценки':
            score += count * 2
        else:
            score += count






    return {"result": result, "score": score, "procent": procent , "count_all": count_all}

def get_info_text(context):
    prompt = InfoPrompts()

    textv1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = prompt.get_generator(context),
        max_tokens=4000,
        temperature=0.0
    ).choices[0].message['content']


    print(textv1)
    print('______________________')

    raw_search  = search_stop_words(textv1)




    stopwords = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = prompt.get_word_search(raw_search['result'], textv1),
        max_tokens=4000,
        temperature=0.0
    ).choices[0].message['content']

    print(stopwords)
    print('______________________')
    fixwords = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
        messages = prompt.redactor(textv1,stopwords,context),
        max_tokens=4000,
        temperature=0.0
    ).choices[0].message['content']

    print(fixwords)
    print('______________________')

    logging.info(fixwords)
    textv2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = prompt.generator2(textv1,fixwords),
        max_tokens=4000,
        temperature=0.0
    ).choices[0].message['content']


    print(textv2)
    print('______________________')

    # textv3 = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages = prompt.controller(textv2,context),
    #     max_tokens=4000,
    #     temperature=0.0
    # ).choices[0].message['content']

    # print(textv3)

    search  = search_stop_words(textv2)

    finaltext = textv2

    response = {
        "textv1": textv1,
        "textv2": textv2,
        "result": search['result'],
        "score": search['score'],
        "procent": search['procent'],
        "all_count": search['count_all'],
        "final_text": finaltext,
        "loops" : 0,
        "raw_all_count": raw_search['count_all'],
        "raw_procent": raw_search['procent'],
        "raw_rating": raw_search['score'],


    }





    return response






