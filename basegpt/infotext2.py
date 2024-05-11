import json
import logging

import openai


import re

import tiktoken
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

from .prompts import *
from .models import  *


model = "gpt-4-turbo-2024-04-09"
# model = "gpt-3.5-turbo"
client = openai.OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
    )

def count_tokens( messages) -> int:
    """
    Counts the number of tokens required to send the given messages.
    :param messages: the messages to send
    :return: the number of tokens required
    """
    model = "gpt-4-turbo-2024-04-09"

    try:

        encoding = tiktoken.encoding_for_model(model)

    except KeyError as e:

        encoding = tiktoken.get_encoding("gpt-3.5-turbo")


    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            try:
                if type(value) == str:

                    num_tokens += len(encoding.encode(value))
                elif type(value) == list:

                    num_tokens = num_tokens + len(encoding.encode(value[0]['text'])) + 1500

            except Exception as e:

                print(e)
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

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


def get_textv1(context):
    prompt = InfoPrompts()

    textv1 = openai.ChatCompletion.create(
        model=model,
        messages=prompt.get_generator(context),
        max_tokens=4000,
        temperature=1
    ).choices[0].message['content']

    input_tokens = count_tokens(prompt.get_generator(context))
    output_tokens = count_tokens([{"role": "assistant", "content": textv1}])


    return textv1, input_tokens, output_tokens


def get_stopwords(raw_search,textv1):
    prompt = InfoPrompts()
    stopwords = openai.ChatCompletion.create(
        model=model,
        messages=prompt.get_word_search(raw_search['result'], textv1),
        max_tokens=4000,
        temperature=1
    ).choices[0].message['content']
    return stopwords


def get_fixwords(textv1, stopwords, context):
    prompt = InfoPrompts()
    fixwords = openai.ChatCompletion.create(
        model=model,
        messages=prompt.redactor(textv1, stopwords, context),
        max_tokens=4000,
        temperature=1
    ).choices[0].message['content']

    return fixwords


def get_textv2(textv1, fixwords, context):
    prompt = InfoPrompts()
    textv2 = openai.ChatCompletion.create(
        model=model,
        messages=prompt.generator2(textv1, fixwords),
        max_tokens=4000,
        temperature=1
    ).choices[0].message['content']

    input_tok = count_tokens(prompt.generator2(textv1, fixwords))
    output_tok = count_tokens([{"role": "assistant", "content": textv2}])


    return textv2, input_tok, output_tok

def get_textv3(context, textv2):
    prompt = InfoPrompts()
    textv3 = openai.ChatCompletion.create(
        model=model,
        messages=prompt.controller(textv2, context),
        max_tokens=4000,
        temperature=0.0
    ).choices[0].message['content']

    input_tok = count_tokens(prompt.controller(textv2, context))
    output_tok = count_tokens([{"role": "assistant", "content": textv3}])

    return textv3, input_tok, output_tok




def get_info_text(context, user):

    result = Result.objects.create(user=user)

    input_tokens = 0
    output_tokens = 0

    for i in range (1, 3):

        iter = InfoTextIterations.objects.create(result=result)


        if i == 1:

            raw_text = get_raw(context)


            raw_search  = search_stop_words(raw_text)

            iter.rawtext = raw_text
            iter.raw_all_count = raw_search['count_all']
            iter.raw_procent = raw_search['procent']
            iter.raw_rating = raw_search['score']



            textv1, input_tok, output_tok = get_textv1(context)



    
            raw_search  = search_stop_words(textv1)

            iter.textv1 = textv1
            iter.v1_all_count = raw_search['count_all']
            iter.v1_procent = raw_search['procent']
            iter.v1_rating = raw_search['score']

            v1_all_count = raw_search['count_all']
            v1_procent = raw_search['procent']
            v1_rating = raw_search['score']





        stopwords = get_stopwords(raw_search,textv1)



        fixwords = get_fixwords(textv1, stopwords, context)


        logging.info(fixwords)

        textv2, input_tok, output_tok = get_textv2(textv1, fixwords, context)
        input_tokens += input_tok
        output_tokens += output_tok
        search  = search_stop_words(textv2)


        iter.textv2 = textv2
        iter.v2_all_count = search['count_all']
        iter.v2_procent = search['procent']
        iter.v2_rating = search['score']
        v2_all_count = search['count_all']
        v2_procent = search['procent']
        v2_rating = search['score']




        # textv3, input_tok, output_tok = get_textv3(context, textv2)
        #
        # input_tokens += input_tok
        # output_tokens += output_tok
        #
        # search = search_stop_words(textv3)
        # iter.textv3 = textv3
        # iter.v3_all_count = search['count_all']
        # iter.v3_procent = search['procent']
        # iter.v3_rating = search['score']
        iter.loops = i
        iter.save()



        finaltext = textv2
        textv1 = textv2

        response = {

            "result": search['result'],
            "score": search['score'],
            "procent": search['procent'],
            "all_count": search['count_all'],
            "final_text": finaltext,
            "loops": i,
            "raw_all_count": raw_search['count_all'],
            "raw_procent": raw_search['procent'],
            "raw_rating": raw_search['score'],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,

        }

        if v2_all_count < v1_all_count and v2_procent < v1_procent and v2_rating < 5:
            break








    return response, result




def get_raw(context):
    raw_text = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": f'напиши рекламу в информационном стиле о {context}'},

        ],
        max_tokens=4000,
        temperature=1
    ).choices[0].message['content']

    return raw_text
