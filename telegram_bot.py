#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime, date
from uuid import uuid4

from django.conf import settings
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.environment")
import django

django.setup()
from apps.users.models import User, Santa
from django.urls import reverse
from apps.common.helpers import send_html_message
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

REGISTER_USER = 1
EMAIL_WHITE_LIST = ('anya.niculaes@gmail.com',)
valid_email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@(ebs-integrator.com|lead47.com)"


def error(update, context):
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))


def get_user_by_chat_id(chat_id):
    try:
        return User.objects.get(chat_id=chat_id)
    except User.DoesNotExist:
        return None


def start(update, context):
    chat_id = update.message.chat_id
    user = get_user_by_chat_id(chat_id)

    if user:
        try:
            santa = Santa.objects.get(santa=user)
            msg = f'\n🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁\nYou are Santa for {santa.user.name}\n🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁'
        except Santa.DoesNotExist:
            msg = f'Verify you email and use the link for being a Santa!'

        update.message.reply_text(f'You already registered as {user.name}!\n{msg}')
        return ConversationHandler.END

    else:
        update.message.reply_text(
            f'HO HO HO! Do you wanna be Santa? Write your email!\nNote: Email have to end with @ebs-integrator.com or @lead47.com')
        return REGISTER_USER


def register_user(update, context):
    email = update.message.text
    chat_id = update.message.chat_id

    if re.match(valid_email_pattern, email) or email in EMAIL_WHITE_LIST:
        try:
            user = User.objects.get(email=email)
            print(f'{user.name} just registered!')
            token = str(uuid4())
            user.chat_id = chat_id
            user.token = token
            user.save()
            update.message.reply_text(f'Visit {email} and use link from email!')
            send_html_message(user.email, 'Are you really Secret Santa?', 'emails/verify.html', {
                'title': 'Cool! Hope you are great Santa!',
                'link': f"{settings.DOMAIN_ADDRESS}{reverse('user_verify', args=(token,))}",
            })
            return ConversationHandler.END
        except User.DoesNotExist:
            update.message.reply_text('User with this email does not exists! Try again!')
            return REGISTER_USER
    else:
        update.message.reply_text(
            f'HO HO HO! Do you wanna be Santa? Write your email!\nNote: Email have to end with @ebs-integrator.com or @lead47.com')
        return REGISTER_USER


def send_notifications(context):
    ddl = 28
    now = datetime.now()
    today = now.date()
    current_year = now.year
    send = False
    month = 12
    if today == date(current_year, month, ddl - 10):
        msg = '10 days left!'
        send = True
    elif today == date(current_year, month, ddl - 3):
        msg = '3 days left!'
        send = True
    elif today == date(current_year, month, ddl - 1):
        msg = 'AAAAAAAAAAAAAAAAAA! 1 day left!!!!!!!!! Buy some gift!'
        send = True

    if send:
        for user in User.objects.all():
            context.bot.send_message(
                chat_id=user.chat_id,
                text=f'Do not forget to buy a gift till {ddl} December! {msg}'
            )


def notify_santa(context):
    santas = Santa.objects.all()
    for user in User.objects.filter(verified=True, santa_notified=False):
        try:
            santa = santas.get(santa=user)
            context.bot.send_message(
                chat_id=user.chat_id,
                text=f'\n🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁\nYou are Santa for {santa.user.name}\n🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁🎄❄️☃️🎁❄️🎄☃️🎁☃️🎄❄️🎁❄️☃️🎄🎁'
            )
            user.santa_notified = True
            user.save()

        except Santa.DoesNotExist:
            print(f'User {user.name} is not Santa!')


def main():
    updater = Updater('', use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],

        states={
            REGISTER_USER: [MessageHandler(Filters.text, register_user)],
        },
        fallbacks=[
            CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.job_queue.run_repeating(send_notifications, 3600)  # check every 1 hour
    updater.job_queue.run_repeating(notify_santa, 1)  # check every 1 second
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Starting BOT!')
    main()
