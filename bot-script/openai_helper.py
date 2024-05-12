from __future__ import annotations
from openai import AsyncOpenAI
import logging
import os
import sys
import traceback
from datetime import datetime, timedelta

from dotenv import load_dotenv

from db import Database
import django
from db_analytics import *

# Получаем путь к текущему скрипту
script_path = os.path.abspath(__file__)

# Получаем путь к директории, содержащей текущий скрипт
script_dir = os.path.dirname(script_path)

# Получаем путь к корневой директории проекта (по одному уровню выше)
project_root = os.path.dirname(script_dir)

# Добавляем путь к корневой директории в переменную окружения PYTHONPATH
sys.path.insert(0, project_root)

# Теперь можно импортировать модели из bot.models

# Установите переменную окружения DJANGO_SETTINGS_MODULE для указания файла настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpt.settings")



import tiktoken

import openai

import requests
import json

from calendar import monthrange

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Models can be found here: https://platform.openai.com/docs/models/overview
GPT_3_MODELS = ('gpt-3.5-turbo-1106', "gpt-3.5-turbo", "gpt-3.5-turbo-0613","gpt-3.5-turbo-1106" , "gpt-3.5-turbo-0125","meta-llama/Llama-3-70b-chat-hf")
GPT_3_16K_MODELS = ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613" , "gpt-3.5-turbo-0125", "gpt-3.5-turbo")
GPT_4_MODELS = ("gpt-4", "gpt-4-0314", "gpt-4-0613", "gpt-4-1106-preview", "gpt-4-vision-preview", "gpt-4-turbo","gpt-4-turbo-2024-04-09")
GPT_4_32K_MODELS = ("gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613")
LLAMA_MODELS= ("meta-llama/Llama-3-70b-chat-hf")
GPT_ALL_MODELS = GPT_3_MODELS + GPT_3_16K_MODELS + GPT_4_MODELS + GPT_4_32K_MODELS

def get_price(sub_name):
    price = {}

    if sub_name in LLAMA_MODELS:
        price['input']= 0.0000009
        price['output'] = 0.0000009


    elif sub_name in GPT_3_MODELS:
        price['input']= 0.000001
        price['output'] = 0.000002
    elif sub_name in GPT_4_MODELS:
        price['input']= 0.00001
        price['output'] = 0.00003



    return price


def default_max_tokens(model: str) -> int:
    """
    Gets the default number of max tokens for the given model.
    :param model: The model name
    :return: The default number of max tokens
    """
    base = 1000
    if model in LLAMA_MODELS:
        return base
    elif model in GPT_3_MODELS:
        return base
    elif model in GPT_4_MODELS:
        return base
    elif model in GPT_3_16K_MODELS:
        return base
    elif model in GPT_4_32K_MODELS:


        return base



# Load translations
parent_dir_path = os.path.join(os.path.dirname(__file__), os.pardir)
translations_file_path = os.path.join(parent_dir_path, 'translations.json')
with open(translations_file_path, 'r', encoding='utf-8') as f:
    translations = json.load(f)


def localized_text(key, bot_language):
    """
    Return translated text for a key in specified bot_language.
    Keys and translations can be found in the translations.json.
    """
    try:
        return translations[bot_language][key]
    except KeyError:
        logging.warning(f"No translation available for bot_language code '{bot_language}' and key '{key}'")
        # Fallback to English if the translation is not available
        if key in translations['en']:
            return translations['en'][key]
        else:
            logging.warning(f"No english definition found for key '{key}' in translations.json")
            # return key as text
            return key


class OpenAIHelper:
    """
    ChatGPT helper class.
    """

    def __init__(self, config: dict):
        """
        Initializes the OpenAI helper class with the given configuration.
        :param config: A dictionary containing the GPT configuration
        """
        openai.api_key = config['api_key']
        openai.proxy = config['proxy']
        self.config = config
        self.conversations: dict[int: list] = {}  # {chat_id: history}
        self.last_updated: dict[int: datetime] = {}  # {chat_id: last_update_timestamp}
        self.db_analytics_for_sessions = DBanalytics_for_sub_stat()
        self.db = Database()
        self.db_statistic_by_day = DBstatistics_by_day()

        self.db_admin_stats = DBAdminStats()
        self.type_admin = 'personal'

    def get_conversation_stats(self, chat_id: int, model: str) -> tuple[int, int]:
        """
        Gets the number of messages and tokens used in the conversation.
        :param chat_id: The chat ID
        :return: A tuple containing the number of messages and tokens used
        """
        if chat_id not in self.conversations:
            self.reset_chat_history(chat_id)
        return len(self.conversations[chat_id]), self.count_tokens(self.conversations[chat_id], model)




    async def generate_image(self, quality, size,  prompt):
        try:

            client = AsyncOpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )


            response =await client.images.generate(

                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=1,
                )





            image_url = response.data[0].url
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            image_url = False


        return image_url

    async def get_chat_response_stream(self, chat_id: int, query, model_config: dict, sub_type: int):


        """
        Stream response from the GPT model.
        :param chat_id: The chat ID
        :param query: The query to send to the model
        :return: The answer from the model and the number of tokens used, or 'not_finished'
        """

        # analytics for sessions




        response, input_tokens = await self.__common_get_chat_response(chat_id, query,model_config = model_config, stream=True)

        if response != False:

            answer = ''
            async for item in response:



                answer += item.choices[0].delta.content or ""
                yield answer, 'not_finished'


            answer = answer.strip()

            tokens_in_answer = self.count_tokens([{"role": "assistant", "content": answer}], model_config['model'])
            sub_name = await self.db.get_sub_name_from_user(chat_id)
            if model_config['multimodel_3'] == True:
                await self.db.update_used_tokens(chat_id, int(tokens_in_answer/model_config['multi_k']))
            else:
                await self.db.update_used_tokens(chat_id, tokens_in_answer)



            sub_id = await self.db.get_sub_type(chat_id)
            sub_name = await self.db.get_sub_name_from_user(chat_id)
            model = model_config['model']
            price = get_price(model)
            try:
                if sub_name == 'ultimate admin':
                    await self.db_admin_stats.add(chat_id, input_tokens, tokens_in_answer, price, self.type_admin)
                else:



                    await self.db_statistic_by_day.add(chat_id, input_tokens, tokens_in_answer, price)

                    user_model = await self.db.get_user_model(chat_id)
                    await  self.db_analytics_for_sessions.add_sub_st_model(chat_id, user_model, input_tokens, tokens_in_answer, 1)

            except Exception as e:
                print(e)
                pass

            self.add_to_history(chat_id, role="assistant", content=answer)
            tokens_in_history= self.count_tokens(self.conversations[chat_id], model_config['model'])

            tokens_used = tokens_in_history

            if self.config['show_usage']:

                if model_config['multimodel_3'] == True:
                    tokens_in_history = int(tokens_in_history/model_config['multi_k'])

                remaining_tokens = await self.db.get_max_tokens(chat_id) - await self.db.get_used_tokens(chat_id)

                answer += f"\n\n---\nИстория диалога: {tokens_in_history} \nОсталось токенов: {remaining_tokens}"

            yield answer, tokens_used

        else:
            logging.error(f"Error generating response: {response}")
            yield 'Произошла ошибка при обработке запроса, попробуйте очистить историю или подождите', 0

    # @retry(
    #     reraise=True,
    #     retry=retry_if_exception_type(openai.error.RateLimitError),
    #     wait=wait_fixed(20),
    #     stop=stop_after_attempt(3)
    # )
    async def __common_get_chat_response(self, chat_id: int, query,model_config:dict, stream=False):
        """
        Request a response from the GPT model.
        :param chat_id: The chat ID
        :param query: The query to send to the model
        :return: The answer from the model and the number of tokens used
        """





        bot_language = self.config['bot_language']
        try:
            # if chat_id not in self.conversations or self.__max_age_reached(chat_id):
            #     self.reset_chat_history(chat_id)

            # self.last_updated[chat_id] = datetime.now()


            self.add_to_history(chat_id, role="user", content=query)






            # Summarize the chat history if it's too long to avoid excessive token usage
            token_count = self.count_tokens( self.conversations[chat_id],  model_config['model'])
            exceeded_max_tokens = token_count + default_max_tokens(model=model_config['model']) > self.__max_model_tokens(model_config['model'])
            exceeded_max_history_size = False
            try:
                while exceeded_max_tokens or exceeded_max_history_size:

                    logging.info(f'Chat history for chat ID {chat_id} is too long. Summarising...')


                    # delete from conversation[chat_id] first message from user and assistant
                    self.remove_messages(chat_id)





                    token_count = self.count_tokens(self.conversations[chat_id], model_config['model'])
                    exceeded_max_tokens = token_count + default_max_tokens(
                        model=model_config['model']) > self.__max_model_tokens(model_config['model'])



            except Exception as e:
                logging.error(f"Error summarising chat history: {e}")
                pass


            if model_config['multimodel_3'] == True:

                available_tokens = await self.db.get_max_tokens(chat_id)*model_config['multi_k'] - await self.db.get_used_tokens(chat_id)*model_config['multi_k']

            else:
                available_tokens = await self.db.get_max_tokens(chat_id) - await self.db.get_used_tokens(chat_id)
            if available_tokens < default_max_tokens(model=model_config['model']) and available_tokens > 10:
                max_tokens = available_tokens

            else:
                max_tokens = default_max_tokens(model=model_config['model'])




            input_tokens = self.count_tokens(self.conversations[chat_id], model_config['model'])






            try:
                load_dotenv()
                logging.info(f"Model: {model_config['model']}")

                if model_config['model'] in LLAMA_MODELS:
                    client = AsyncOpenAI(
                        api_key=os.environ.get("TOGETHER_API_KEY"),
                        base_url="https://api.together.xyz/v1",
                        # api_key=os.environ.get("OPENAI_API_KEY"),
                    )
                else:
                    client = AsyncOpenAI(
                        api_key=os.environ.get("OPENAI_API_KEY"),
                    )




                try:

                    result =await client.chat.completions.create(
                        model=model_config['model'],
                        messages=self.conversations[chat_id],
                        temperature=model_config['custom_temp'],
                        n=self.config['n_choices'],
                        max_tokens=int(max_tokens),

                        stream=True,

                    )
                except Exception as e:
                    logging.exception(e)





                if model_config['multimodel_3'] == True:
                    await self.db.update_used_tokens(chat_id, int(input_tokens/model_config['multi_k']))
                else:
                    await self.db.update_used_tokens(chat_id, input_tokens)



                return result, input_tokens
            except Exception as e:



                logging.error(traceback.format_exc())

                return False, 0


        except openai.error.RateLimitError as e:
            raise e

        except openai.error.InvalidRequestError as e:

            raise Exception(f"⚠️ _{localized_text('openai_invalid', bot_language)}._ ⚠️\n{str(e)}") from e

        except Exception as e:
            logging.exception(e)
            print(traceback.format_exc())
            raise Exception


    async def transcribe(self, filename):
        """
        Transcribes the audio file using the Whisper model.
        """
        try:
            with open(filename, "rb") as audio:
                result = await openai.Audio.atranscribe("whisper-1", audio)
                return result.text
        except Exception as e:
            logging.exception(e)


            raise Exception(f"⚠️ _{localized_text('error', self.config['bot_language'])}._ ⚠️\n{str(e)}") from e

    def reset_chat_history(self, chat_id, content=''):
        """
        Resets the conversation history.
        """
        if content == '':
            content = self.config['assistant_prompt']
        self.conversations[chat_id] = [{"role": "system", "content": content}]


    def clean_all_chat_history(self, users):
        """
        Resets the conversation history.
        """
        for chat_id in users:
            self.conversations[chat_id] = [{"role": "system", "content": self.config['assistant_prompt']}]


    def __max_age_reached(self, chat_id) -> bool:
        """
        Checks if the maximum conversation age has been reached.
        :param chat_id: The chat ID
        :return: A boolean indicating whether the maximum conversation age has been reached
        """
        if chat_id not in self.last_updated:
            return False
        last_updated = self.last_updated[chat_id]
        now = datetime.now()
        max_age_minutes = self.config['max_conversation_age_minutes']
        return last_updated < now - timedelta(minutes=max_age_minutes)

    def add_to_history(self, chat_id, role, content):
        """
        Adds a message to the conversation history.
        :param chat_id: The chat ID
        :param role: The role of the message sender
        :param content: The message content
        """
        self.conversations[chat_id].append({"role": role, "content": content})
    def add_role_to_history(self, chat_id, content):

        self.conversations[chat_id] = [{"role": "system", "content": content}]


    async def __summarise(self, conversation) -> str:
        """
        Summarises the conversation history.
        :param conversation: The conversation history
        :return: The summary
        """
        messages = [
            {"role": "assistant", "content": "Summarize this conversation in 700 characters or less"},
            {"role": "user", "content": str(conversation)}
        ]
        response = await openai.ChatCompletion.acreate(
            model=self.config['model'],
            messages=messages,
            temperature=0.4
        )
        return response.choices[0]['message']['content']

    def __max_model_tokens(self, model):
        base = 16000
        if model in LLAMA_MODELS:
            return 8000
        if model in GPT_3_MODELS:
            return base
        if model in GPT_3_16K_MODELS:
            return base * 4
        if model in GPT_4_MODELS:
            return 128000
        if model in GPT_4_32K_MODELS:
            return base * 8


        raise NotImplementedError(
            f"Max tokens for model {self.config['model']} is not implemented yet."
        )


    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def count_tokens(self, messages, model) -> int:
        """
        Counts the number of tokens required to send the given messages.
        :param messages: the messages to send
        :return: the number of tokens required
        """

        try:

            encoding = tiktoken.encoding_for_model(model)

        except KeyError as e:

            encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

        if model in GPT_3_MODELS + GPT_3_16K_MODELS:
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model in GPT_4_MODELS + GPT_4_32K_MODELS:
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")
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

                    logging.error(f"Error encoding message: {e}")
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def remove_messages(self, chat_id):

        for item in self.conversations[chat_id]:
            if item['role'] == 'system':
                pass
            elif item['role'] == 'user' or item['role'] == 'assistant':
                self.conversations[chat_id].remove(item)
                return True
        return False




