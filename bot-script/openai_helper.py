from __future__ import annotations

import logging
import os
import sys
import traceback
from datetime import datetime, timedelta
from db import Database
import django
from db_analytics import DBanalytics_for_month, DBanalytics_for_periods, DBanalytics_for_sessions
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
django.setup()
from bot.models import User, Subscriptions, Period, AnalyticsForMonth, AnalyticsPeriods, Session, Subscriptions_statistics


import tiktoken

import openai

import requests
import json

from calendar import monthrange

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Models can be found here: https://platform.openai.com/docs/models/overview
GPT_3_MODELS = ("gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613")
GPT_3_16K_MODELS = ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613")
GPT_4_MODELS = ("gpt-4", "gpt-4-0314", "gpt-4-0613")
GPT_4_32K_MODELS = ("gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613")
GPT_ALL_MODELS = GPT_3_MODELS + GPT_3_16K_MODELS + GPT_4_MODELS + GPT_4_32K_MODELS

def get_price(sub_name):
    price = {}
    if sub_name in GPT_3_MODELS:
        price['input']= 0.0015
        price['output'] = 0.002
    elif sub_name in GPT_4_MODELS:
        price['input']= 0.03
        price['output'] = 0.06

    elif sub_name in GPT_3_16K_MODELS:
        price['input']= 0.003
        price['output'] = 0.004

    return price


def default_max_tokens(model: str) -> int:
    """
    Gets the default number of max tokens for the given model.
    :param model: The model name
    :return: The default number of max tokens
    """
    base = 1200
    if model in GPT_3_MODELS:
        return base
    elif model in GPT_4_MODELS:
        return base * 2
    elif model in GPT_3_16K_MODELS:
        return base * 4
    elif model in GPT_4_32K_MODELS:
        return base * 8


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
        self.db_analytics_for_sessions = DBanalytics_for_sessions()
        self.db = Database()
        self.db_analytics_for_month = DBanalytics_for_month()

    def get_conversation_stats(self, chat_id: int, model: str) -> tuple[int, int]:
        """
        Gets the number of messages and tokens used in the conversation.
        :param chat_id: The chat ID
        :return: A tuple containing the number of messages and tokens used
        """
        if chat_id not in self.conversations:
            self.reset_chat_history(chat_id)
        return len(self.conversations[chat_id]), self.count_tokens(self.conversations[chat_id], model)






    async def get_chat_response_stream(self, chat_id: int, query: str, model_config: dict, sub_type: int):


        """
        Stream response from the GPT model.
        :param chat_id: The chat ID
        :param query: The query to send to the model
        :return: The answer from the model and the number of tokens used, or 'not_finished'
        """

        # analytics for sessions

        if await self.db.get_sub_name_from_user(chat_id) == 'trial':
            pass


        else:
            keys = len(self.conversations[chat_id])

            if keys == 1 and self.conversations[chat_id][0]['content'] == self.config['assistant_prompt']:
                date = datetime.now()
                try:
                    await self.db_analytics_for_sessions.close_session(chat_id, date)

                    await self.db_analytics_for_sessions.add_session(chat_id, sub_type, date)
                except Exception as e:
                    print(traceback.format_exc())
                    pass

        response = await self.__common_get_chat_response(chat_id, query,model_config = model_config, stream=True)





        answer = ''
        async for item in response:

            if 'choices' not in item or len(item.choices) == 0:
                continue
            delta = item.choices[0].delta
            if 'content' in delta:
                answer += delta.content
                yield answer, 'not_finished'
        answer = answer.strip()

        tokens_in_answer = self.count_tokens([{"role": "assistant", "content": answer}], model_config['model'])
        sub_name = await self.db.get_sub_name_from_user(chat_id)
        try:
            if sub_name == 'trial' or 'admin':
                await self.db_analytics_for_month.add_output_tokens(sub_type, tokens_in_answer)
            else:
                await self.db_analytics_for_sessions.update_session_output(chat_id, tokens_in_answer)
        except Exception as e:
            print(traceback.format_exc())
            pass
        await self.db.update_used_tokens(chat_id, tokens_in_answer)

        self.__add_to_history(chat_id, role="assistant", content=answer)
        tokens_in_history= self.count_tokens(self.conversations[chat_id], model_config['model'])

        tokens_used = tokens_in_history

        if self.config['show_usage']:


            answer += f"\n\n---\nИстория диалога: {tokens_in_history} ток."

        yield answer, tokens_used

    @retry(
        reraise=True,
        retry=retry_if_exception_type(openai.error.RateLimitError),
        wait=wait_fixed(20),
        stop=stop_after_attempt(3)
    )
    async def __common_get_chat_response(self, chat_id: int, query: str,model_config:dict, stream=False):
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


            self.__add_to_history(chat_id, role="user", content=query)


            input_tokens_before_sum = self.count_tokens(self.conversations[chat_id], model_config['model'])


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



                    # try:
                    #     input_sum = self.count_tokens(self.conversations[chat_id], model_config['model'])
                    #
                    #     summary = await self.__summarise(self.conversations[chat_id][:-1])
                    #     output_sum = self.count_tokens([{"role": "assistant", "content": summary}], model_config['model'])
                    #
                    #     logging.debug(f'Summary: {summary}')
                    #     self.reset_chat_history(chat_id, self.conversations[chat_id][0]['content'])
                    #     self.__add_to_history(chat_id, role="assistant", content=summary)
                    #
                    #     self.__add_to_history(chat_id, role="user", content=query)
                    #     sub_name = self.db.get_sub_name_from_user(chat_id)
                    #     try:
                    #         if sub_name == 'trial':
                    #             pass
                    #         else:
                    #             await self.db_analytics_for_sessions.update_session_sum(chat_id, input_sum, output_sum)
                    #     except Exception as e:
                    #         print(traceback.format_exc())
                    #         pass
                    #
                    #
                    # except Exception as e:
                    #     logging.warning(f'Error while summarising chat history: {str(e)}. Popping elements instead...')
                    #     self.conversations[chat_id] = self.conversations[chat_id][-self.config['max_history_size']:]

            except Exception as e:
                print(traceback.format_exc())
                pass



            available_tokens = await self.db.get_max_tokens(chat_id) - await self.db.get_used_tokens(chat_id)
            if available_tokens < default_max_tokens(model=model_config['model']) and available_tokens > 0:
                max_tokens = available_tokens

            else:
                max_tokens = default_max_tokens(model=model_config['model'])

            input_tokens = self.count_tokens(self.conversations[chat_id], model_config['model'])


            try:
                sub_name = await self.db.get_sub_name_from_user(chat_id)
                if sub_name == 'trial' or 'admin':
                    sub_id = await self.db.get_sub_type(chat_id)
                    await self.db_analytics_for_month.add_input_tokens(sub_id, input_tokens)
                else:
                    await self.db_analytics_for_sessions.update_session_input(chat_id, input_tokens, input_tokens_before_sum)
            except Exception as e:
                print(traceback.format_exc())

                pass
            await self.db.update_used_tokens(chat_id, input_tokens)

            return await openai.ChatCompletion.acreate(
                model=model_config['model'],
                messages=self.conversations[chat_id],
                temperature=model_config['custom_temp'],
                n=self.config['n_choices'],
                max_tokens=max_tokens,
                presence_penalty=self.config['presence_penalty'],
                frequency_penalty=self.config['frequency_penalty'],
                stream=stream
            )

        except openai.error.RateLimitError as e:
            raise e

        except openai.error.InvalidRequestError as e:
            print(e)
            raise Exception(f"⚠️ _{localized_text('openai_invalid', bot_language)}._ ⚠️\n{str(e)}") from e

        except Exception as e:
            print(e)
            raise Exception(f"⚠️ _{localized_text('error', bot_language)}._ ⚠️\n{str(e)}") from e


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

    def __add_to_history(self, chat_id, role, content):
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
        base = 4096
        if model in GPT_3_MODELS:
            return base
        if model in GPT_3_16K_MODELS:
            return base * 4
        if model in GPT_4_MODELS:
            return base * 2
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
        except KeyError:
            encoding = tiktoken.get_encoding("gpt-3.5-turbo")

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
                num_tokens += len(encoding.encode(value))
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




