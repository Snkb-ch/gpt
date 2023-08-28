from __future__ import annotations

import asyncio
import asyncio
import json
import logging
import os
import threading
import time
import traceback
from datetime import datetime, timedelta

import schedule
import telegram
import concurrent.futures
import payment
from uuid import uuid4

from yookassa import Configuration, Payment

from telegram import BotCommandScopeAllGroupChats, Update, constants
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle
from telegram import InputTextMessageContent, BotCommand
from telegram.error import RetryAfter, TimedOut
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters, InlineQueryHandler, CallbackQueryHandler, Application, ContextTypes, CallbackContext

from pydub import AudioSegment

from utils import is_group_chat, get_thread_id, message_text, wrap_with_indicator, split_into_chunks, \
    edit_message_with_retry, get_stream_cutoff_values, is_allowed, is_admin, \
    get_reply_to_message_id, error_handler
from openai_helper import OpenAIHelper, localized_text
# from usage_tracker import UsageTracker

from aiogram import Bot, Dispatcher, executor, types
from db import Database
from db_analytics import DBanalytics_for_month, DBanalytics_for_periods

import os
import sys

from asgiref.sync import sync_to_async
from django.forms import model_to_dict

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

# Импортируем и настраиваем Django настройки
import django

django.setup()
from bot.models import User, Subscriptions, Period, AnalyticsForMonth, AnalyticsPeriods


class ChatGPTTelegramBot:
    """
    Class representing a ChatGPT Telegram Bot.
    """

    def __init__(self, config: dict, openai: OpenAIHelper):
        """
        Initializes the bot with the given configuration and GPT bot object.
        :param config: A dictionary containing the bot configuration
        :param openai: OpenAIHelper object
        """

        self.db = Database()
        self.db_analytics_for_month = DBanalytics_for_month()
        self.db_analytics_for_periods = DBanalytics_for_periods()

        self.config = config
        self.openai = openai

        self.status = {}
        bot_language = self.config['bot_language']
        self.commands = [
            BotCommand(command='help', description='Помощь/описание'),
            BotCommand(command='reset', description='Сбросить историю чата'),
            BotCommand(command='buy', description='Купить подписку'),
            BotCommand(command='stats', description='Моя Статистика'),
            BotCommand(command='resend', description='Переслать последний запрос'),

        ]
        self.commands.append(BotCommand(command='role', description='Изменить роль  PRO'))
        self.commands.append(BotCommand(command='temperature', description='Изменить креативность  PRO'))
        self.group_commands = [BotCommand(
            command='chat', description=localized_text('chat_description', bot_language)
        )] + self.commands
        self.disallowed_message = localized_text('disallowed', bot_language)
        self.budget_limit_message = localized_text('budget_limit', bot_language)
        self.usage = {}
        self.last_message = {}
        self.inline_queries_cache = {}
        self.bot = Bot(token=self.config['token'])
        self.dispatcher = Dispatcher(bot=self.bot, loop=asyncio.get_event_loop())

    async def cancel(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text="Отменено",
        )
        user_id = update.message.from_user.id
        self.status[user_id] = 'prompt'

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='''Если возникли вопросы, столкнулись с ошибкой напишите нам brainshtorm@gmail.com
            
После ввода команды /role вы пишете условия, которые нейросеть должна соблюдать. Например, если нужны краткие ответы без пояснений, можно попросить ИИ отвечать только "да" или "нет".

Команда /temperature для того, чтобы регулировать креативность от 0 до 2. Чем меньше температура, тем чаще ИИ повторяется, но уменьшается шанс ошибки.

Подробнее на сайте: brainstormai.ru''',

        )

    async def start(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:

        user_id = update.message.from_user.id
        self.status[user_id] = 'prompt'

        if not await self.db.user_exists(user_id):
            await self.db.add_user(user_id)
            await self.calc_end_time(user_id)

            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='''Добро пожаловать! 

🆓 Активная подписка: Пробный период

⏬ Вам доступно ⏬

✅ Дней: 3 дня
✅ Модель: GPT-3.5
✅ Токенов: 2000''',
            )
            return

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # send message hello
        if await self.is_active(update, context, update.message.from_user.id) == False:
            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='Ваша подписка закончилась, купите подписку',
            )
            return

        remain_tokens = await self.db.get_max_tokens(update.message.from_user.id) - await  self.db.get_used_tokens(
            update.message.from_user.id)

        date = str(await self.db.get_time_sub(update.message.from_user.id))[0:10]
        date = date[8:10] + '.' + date[5:7] + '.' + date[0:4]

        await update.message.reply_text(
            text='Осталось ' + str(
                remain_tokens) + ' токенов' + '\n' + 'Подписка ' + await self.db.get_sub_name_from_user(
                update.message.from_user.id) + '\n' + 'Закончится ' +
                 date,
        )

    async def resend(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Resend the last request
        """
        chat_id = update.effective_chat.id
        if chat_id not in self.last_message:
            logging.warning(f'User {update.message.from_user.name} (id: {update.message.from_user.id})'
                            f' does not have anything to resend')
            await update.effective_message.reply_text(
                message_thread_id=get_thread_id(update),
                text=localized_text('resend_failed', self.config['bot_language'])
            )
            return

        # Update message text, clear self.last_message and send the request to prompt
        logging.info(f'Resending the last prompt from user: {update.message.from_user.name} '
                     f'(id: {update.message.from_user.id})')
        with update.message._unfrozen() as message:
            message.text = self.last_message.pop(chat_id)

        await self.prompt(update=update, context=context)

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Resets the conversation.
        """

        logging.info(f'Resetting the conversation for user {update.message.from_user.name} '
                     f'(id: {update.message.from_user.id})...')

        chat_id = update.effective_chat.id
        reset_content = message_text(update.message)
        self.openai.reset_chat_history(chat_id=chat_id, content=reset_content)
        await update.effective_message.reply_text(
            message_thread_id=get_thread_id(update),
            text='История чата сброшена',
        )

    async def send_to_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await  self.db.is_admin(update.message.from_user.id):
            return
        self.status[update.message.from_user.id] = 'admin_message'
        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Введите сообщение',
        )

    async def send_reminder(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            users = await self.db.get_all_inactive_users()

            for user in users:
                try:
                    await self.bot.send_message(chat_id=user,
                                                text='Привет, ты давно не заходил к нам, наш бот всегда готов помочь, надеемся увидеть тебя снова')
                    await asyncio.sleep(60 * 60 * 60 * 24)
                except:
                    pass
        except Exception as e:
            print(traceback.format_exc())

    async def admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await  self.db.is_admin(update.message.from_user.id):
            return
        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Команды: /send_to_all  , /send_reminder',
        )

    async def buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        user_id = update.message.from_user.id

        sub = await self.db.get_sub_type(user_id)

        if await  self.db.get_status(user_id) == 'active' and sub != 1:
            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='У вас уже есть активная подписка',
            )
            return

        subs = await  self.db.get_subs_for_sale()

        reply_markup_buttons = []  # Здесь будем хранить кнопки для разметки

        try:
            for sub in subs:

                button_text = sub['sub_name'] + ' ' + str(sub['price']) + ' рублей'
                button_callback = sub['sub_id']
                reply_markup_buttons.append([InlineKeyboardButton(text=button_text, callback_data=button_callback)])
        except Exception as e:
            print(traceback.format_exc())
            print(e)


        # Создаем разметку с кнопками из списка reply_markup_buttons
        reply_markup = InlineKeyboardMarkup(reply_markup_buttons)

        # reply_markup = InlineKeyboardMarkup(
        #     [
        #         [
        #             InlineKeyboardButton(
        #                 text='Купить подписку 1',
        #                 callback_data=3
        #             )
        #         ],
        #         [
        #             InlineKeyboardButton(
        #                 text='Купить подписку 2',
        #                 callback_data=4
        #             )
        #
        #         ]
        #     ]
        # )

        await update.effective_message.reply_text(
            message_thread_id=get_thread_id(update),

            text='''Описание подписок:

GPT-3.5 Ultimate
Цена: 90 руб за / дней
Модель: GPT-3.5
100 000 токенов - около 150 стр. А4
Настройка роли и креативности: ❌

GPT-4 Basic 
Цена: 110 руб / 30 дней
Модель: GPT-4
10 000 токенов - около 15 стр. А4
Настройка роли и креативности: ❌

GPT-4 Standart 
Цена: 350 руб / 30 дней
Модель: GPT-4
40 000 токенов - около 60 стр. А4
Настройка роли и креативности: ✅

GPT-4 PRO 
Цена: 700 руб / 30 дней
Модель: GPT-4
100 000 токенов - около 150 стр. А4
Настройка роли и креативности: ✅

Важно🔻
Один токен не равен одному символу. Точного отношения токена к символу нет. Приблизительно 1000 токенов – 300 слов или 2300 символов с пробелами. Проще говоря 1 тыс. равна 1.5 стр. А4.

Подробнее на сайте: brainstormai.ru

Выберите подписку или введите /cancel для отмены
''',
            reply_markup=reply_markup
        )

    async def send_end_of_subscription_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Ваша подписка закончилась, купите подписку',
        )
        await self.buy(update, context)

    async def temperature(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if not await self.db.get_edit_temp(user_id):
            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='Ваша подписка не позволяет изменять температуру',

            )

            return
        if not await self.is_active(update, context, update.message.from_user.id):
            await self.send_end_of_subscription_message(update, context)
            return

        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Введите температуру от 0 до 2. Например, 1.25',
        )
        user_id = update.message.from_user.id
        self.status[user_id] = 'set_temperature'

    async def role(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.db.get_edit_role(update.message.from_user.id):
            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='Ваша подписка не позволяет изменять роль',
            )

            return
        if not await self.is_active(update, context, update.message.from_user.id):
            await self.send_end_of_subscription_message(update, context)
            return

        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='''Придумайте роль или введите /cancel для отмены

После ввода роли история чата автоматически сбросится''',
        )

        user_id = update.message.from_user.id
        self.status[user_id] = 'set_role'

    async def set_role(self, update: Update, context: ContextTypes.DEFAULT_TYPE, role):

        await update.message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Роль изменена',
        )
        user_id = update.message.from_user.id
        self.status[user_id] = 'prompt'
        self.openai.reset_chat_history(chat_id=update.effective_chat.id, content=message_text(update.message))
        self.openai.add_role_to_history(chat_id=update.effective_chat.id, content=role)

        await self.db_analytics_for_month.add_role_edited(await self.db.get_sub_type(user_id))

    async def set_temperature(self, update: Update, context: ContextTypes.DEFAULT_TYPE, temperature):
        try:
            if float(temperature) <= 2.0 or float(temperature) >= 0.0:

                await update.message.reply_text(
                    message_thread_id=get_thread_id(update),
                    text='Температура изменена',
                )
                await self.db.set_custom_temp(update.message.from_user.id, temperature)
                user_id = update.message.from_user.id
                self.status[user_id] = 'prompt'
                await self.db_analytics_for_month.add_temp_edited(await self.db.get_sub_type(user_id))

        except Exception as e:
            await update.message.reply_text(
                message_thread_id=get_thread_id(update),
                text='Введите температуру от 0 до 2 или введите /cancel для отмены',
            )


    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        if await self.db.get_email(update.callback_query.from_user.id) == None:
            await update.effective_message.reply_text(
                message_thread_id=get_thread_id(update),
                text='''Пожалуйста, введите email, на который будет выслан чек. 
                
С политикой кофиденциальности можно ознакомится на сайте https://brainstormai.ru/privacy-policy''',

            )
            user_id = update.callback_query.from_user.id
            self.status[user_id] = 'set_email'
            return
        await update.effective_message.reply_text(
            message_thread_id=get_thread_id(update),
            text='Ожидайте ссылку на оплату',
        )
        query = update.callback_query
        await query.answer()

        Configuration.account_id = self.config['shop_id']
        Configuration.secret_key = self.config['yookassa_key']
        price = await self.db.get_price(query.data)
        sub_name = await self.db.get_sub_name(query.data)
        email = await self.db.get_email(query.from_user.id)

        payment_details =  payment.payment(price, sub_name, email)

        await update.effective_message.reply_text(
            (payment_details['confirmation'])['confirmation_url'])

        if await payment.check_payment(payment_details['id']):
            await update.effective_message.reply_text("Платеж прошел")

            user_id = update.callback_query.from_user.id
            sub_id = query.data
            await self.activate_sub(user_id, query.data)

            await self.db_analytics_for_month.add_income(sub_id, await self.db.get_price(sub_id))
            await self.db_analytics_for_month.add_sold(sub_id)









        else:
            await update.message.reply_text("Платеж не прошёл, попробуйте ещё раз")

    async def activate_sub(self, user_id, sub_id):
        await self.db.set_sub_type(user_id, sub_id)
        await self.db.set_status(user_id, 'active')
        await self.db.set_time_sub(user_id, datetime.now().date())
        await self.calc_end_time(user_id)
        await self.db.set_used_tokens(user_id, 0)
        await self.db.set_custom_temp(user_id, 1)

    async def is_in_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id) -> bool:
        if await self.db.get_sub_type(user_id) == 2:
            return True
        elif await self.db.get_end_time(user_id) < datetime.now().date():
            return False
        else:
            return True

    async def is_active(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
        if await self.db.get_sub_type(user_id) == 2:
            return True
        elif await self.db.get_status(user_id) == 'inactive':
            return False
        elif await self.is_in_time(update, context, user_id) == False:
            sub_type = await self.db.get_sub_type(user_id)
            await self.db.set_inactive(user_id)
            await self.db_analytics_for_month.add_expired(sub_type)
            await self.db_analytics_for_month.add_expired_time(sub_type)

            return False

        else:
            return True

    def is_email(self, email):
        if email.count('@') == 1 and email.count('.') >= 1:
            return True
        else:
            return False

    async def is_in_tokens(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id) -> bool:
        if await self.db.get_sub_type(user_id) == 2:
            return True
        elif await self.db.get_used_tokens(user_id) >= await self.db.get_max_tokens(user_id):
            return False
        else:
            return True

    async def is_input_in_tokens(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id,
                                 tokens_input) -> bool:
        if await self.db.get_sub_type(user_id) == 2:
            return True
        elif await self.db.get_used_tokens(user_id) + tokens_input >= await self.db.get_max_tokens(user_id):

            return False

    async def calc_end_time(self, user_id):
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=await self.db.get_duration_sub(user_id))
        await self.db.set_end_time(user_id, end_date)

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        React to incoming messages and respond accordingly.
        """
        if update.edited_message or not update.message or update.message.via_bot:
            return

        # if not await self.check_allowed_and_within_budget(update, context):
        #     return

        logging.info(
            f'New message received from user {update.message.from_user.name} (id: {update.message.from_user.id})')

        # Добавляем в базу данных

        chat_id = update.effective_chat.id
        user_id = update.message.from_user.id

        prompt = message_text(update.message)
        if user_id not in self.status:
            self.status[user_id] = 'prompt'

        if update.message.text:

            if not await self.is_active(update, context, user_id):
                await self.send_end_of_subscription_message(update, context)
                return

            if self.status[user_id] == 'set_role':
                await self.set_role(update, context, update.message.text)

                return
            elif self.status[user_id] == 'set_temperature':

                await self.set_temperature(update, context, update.message.text)

            elif self.status[user_id] == 'admin_message':

                self.status[user_id] = 'prompt'
                users = await self.db.get_all_users()
                for user in users:
                    try:
                        await self.bot.send_message(chat_id=user, text=update.message.text)
                    except:
                        pass
                return
            elif self.status[user_id] == 'set_email':
                if self.is_email(update.message.text) == False:
                    await update.message.reply_text(
                        message_thread_id=get_thread_id(update),
                        text='Неверный формат email',
                    )
                    return
                await self.db.set_email(user_id, update.message.text)
                await update.message.reply_text(
                    message_thread_id=get_thread_id(update),
                    text='Email установлен, выберите подписку',
                )
                self.status[user_id] = 'prompt'
                await self.buy(update, context)


            elif self.status[user_id] == 'prompt':

                plan = await self.db.get_sub_type(user_id)

                self.last_message[chat_id] = prompt
                model_config = await self.db.get_model_config(update.effective_chat.id)
                tokens_input = self.openai.count_tokens(([{"role": "user", "content": prompt}]), model_config['model'])
                tokens_input += self.openai.get_conversation_stats(chat_id=chat_id, model=model_config['model'])[1]

                if await  self.is_input_in_tokens(update, context, user_id, tokens_input) == False:
                    await update.effective_message.reply_text(
                        message_thread_id=get_thread_id(update),
                        text='Осталось ' + ' ' + str(
                            await self.db.get_max_tokens(user_id) - await self.db.get_used_tokens(
                                user_id)) + ' токенов' + '\n' + 'Ваше сообщение слишком длинное, сократите его',
                    )
                    return

                try:
                    total_tokens = 0

                    if self.config['stream']:
                        async def _reply():
                            nonlocal total_tokens
                            await update.effective_message.reply_chat_action(
                                action=constants.ChatAction.TYPING,
                                message_thread_id=get_thread_id(update)
                            )
                            model_config = await  self.db.get_model_config(update.effective_chat.id)

                            stream_response = self.openai.get_chat_response_stream(chat_id=chat_id, query=prompt,
                                                                                   model_config=model_config)

                            i = 0
                            prev = ''
                            sent_message = None
                            backoff = 0
                            stream_chunk = 0

                            async for content, tokens in stream_response:

                                if len(content.strip()) == 0:
                                    continue

                                stream_chunks = split_into_chunks(content)
                                if len(stream_chunks) > 1:
                                    content = stream_chunks[-1]
                                    if stream_chunk != len(stream_chunks) - 1:
                                        stream_chunk += 1
                                        try:
                                            await edit_message_with_retry(context, chat_id,
                                                                          str(sent_message.message_id),
                                                                          stream_chunks[-2])
                                        except:
                                            pass
                                        try:
                                            sent_message = await update.effective_message.reply_text(
                                                message_thread_id=get_thread_id(update),
                                                text=content if len(content) > 0 else "..."
                                            )
                                        except:
                                            pass
                                        continue

                                cutoff = get_stream_cutoff_values(update, content)
                                cutoff += backoff

                                if i == 0:
                                    try:
                                        if sent_message is not None:
                                            await context.bot.delete_message(chat_id=sent_message.chat_id,
                                                                             message_id=sent_message.message_id)
                                        sent_message = await update.effective_message.reply_text(
                                            message_thread_id=get_thread_id(update),
                                            reply_to_message_id=get_reply_to_message_id(self.config, update),
                                            text=content
                                        )
                                    except:
                                        continue

                                elif abs(len(content) - len(prev)) > cutoff or tokens != 'not_finished':
                                    prev = content

                                    try:
                                        use_markdown = tokens != 'not_finished'
                                        await edit_message_with_retry(context, chat_id, str(sent_message.message_id),
                                                                      text=content, markdown=use_markdown)

                                    except RetryAfter as e:
                                        backoff += 5
                                        await asyncio.sleep(e.retry_after)
                                        continue

                                    except TimedOut:
                                        backoff += 5
                                        await asyncio.sleep(0.5)
                                        continue

                                    except Exception:
                                        backoff += 5
                                        continue

                                    await asyncio.sleep(0.01)

                                i += 1
                                if tokens != 'not_finished':
                                    total_tokens = int(tokens)

                        await wrap_with_indicator(update, context, _reply, constants.ChatAction.TYPING)

                        await self.db.set_used_tokens(user_id, total_tokens + await self.db.get_used_tokens(user_id))

                        await self.db_analytics_for_month.add_input_tokens(plan, tokens_input)
                        await self.db_analytics_for_month.add_total_tokens(plan, total_tokens)
                        await self.db_analytics_for_month.add_output_tokens(plan, total_tokens - tokens_input)
                        await self.db_analytics_for_periods.add(plan, total_tokens)
                        print(tokens_input)
                        print(total_tokens)

                        if await self.is_in_tokens(update, context, user_id) == False:
                            await update.effective_message.reply_text(
                                message_thread_id=get_thread_id(update),
                                text='Ваш лимит токенов закончился, купите подписку',
                            )

                            await self.db.set_inactive(user_id)

                            await  self.db_analytics_for_month.add_expired(plan)
                            await self.db_analytics_for_month.add_expired_tokens(plan)

                            await self.buy(update, context)













                except Exception as e:
                    # traceback

                    print(traceback.format_exc())

                    logging.exception(e)


    async def post_init(self, application: Application) -> None:
        """
        Post initialization hook for the bot.
        """
        await application.bot.set_my_commands(self.group_commands, scope=BotCommandScopeAllGroupChats())
        await application.bot.set_my_commands(self.commands)

    def run(self):

        """
        Runs the bot indefinitely until the user presses Ctrl+C
        """
        application = ApplicationBuilder() \
            .token(self.config['token']) \
            .proxy_url(self.config['proxy']) \
            .get_updates_proxy_url(self.config['proxy']) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()

        application.add_handler(CommandHandler('reset', self.reset))
        application.add_handler(CommandHandler('help', self.help))
        # application.add_handler(CommandHandler('image', self.image))
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('buy', self.buy))
        application.add_handler(CommandHandler('stats', self.stats))
        application.add_handler(CommandHandler('resend', self.resend))
        application.add_handler(CommandHandler('cancel', self.cancel))
        application.add_handler(CommandHandler('role', self.role))
        application.add_handler(CommandHandler('send_to_all', self.send_to_all))
        application.add_handler(CommandHandler('send_reminder', self.send_reminder))
        application.add_handler(CommandHandler('admin', self.admin))

        application.add_handler(CommandHandler('temperature', self.temperature))

        application.add_handler(CallbackQueryHandler(self.button))
        application.add_handler(CommandHandler(
            'chat', self.prompt, filters=filters.ChatType.GROUP | filters.ChatType.SUPERGROUP)
        )
        # application.add_handler(MessageHandler(
        #     filters.AUDIO | filters.VOICE | filters.Document.AUDIO |
        #     filters.VIDEO | filters.VIDEO_NOTE | filters.Document.VIDEO,
        #     self.transcribe))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))
        # application.add_handler(InlineQueryHandler(self.inline_query, chat_types=[
        #     constants.ChatType.GROUP, constants.ChatType.SUPERGROUP, constants.ChatType.PRIVATE
        # ]))
        # application.add_handler(CallbackQueryHandler(self.handle_callback_inline_query))

        application.add_error_handler(error_handler)

        application.run_polling()
