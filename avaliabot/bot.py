import requests
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


STATE1 = 1
STATE2 = 2

def welcome(update, context):
    try:
        username = update.message.from_user.username
        firstName = update.message.from_user.first_name
        lastName = update.message.from_user.last_name
        message = 'Olá, ' + firstName + '! Digite /feedback para contar sua opinião'
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        print(str(e))


def feedback(update, context):
    try:
        message = 'Professor, diga oque achou da nossa apresentação!!'
        update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True)) 
        return STATE1
    except Exception as e:
        print(str(e))


def inputFeedback(update, context):
    feedback = update.message.text
    print(feedback)
    if len(feedback) < 10:
        message = """Sua resposta foi muito curtinha... 
                        \nInforma mais pra gente, por favor?"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return STATE1
    else:
        message = "Muito obrigada pela sua contribuição!" \
                "Digite /nota para registrar sua avaliação"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return ConversationHandler.END


def inputFeedback2(update, context):
    feedback = update.message.text
    message = "Muito obrigada pela sua contribuição!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ConversationHandler.END



def askForNota(update, context):
    try:
        question = 'Qual nota você dá para nossa apresentação?'
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("👎 Pessima", callback_data='1'),
              InlineKeyboardButton("Ruim", callback_data='2')],
              [InlineKeyboardButton("🤔 Razoavel", callback_data='3'),
              InlineKeyboardButton("boa", callback_data='4')],
              [InlineKeyboardButton("👍 Excelente", callback_data='5')]])
        update.message.reply_text(question, reply_markup=keyboard)
    except Exception as e:
        print(str(e))


def getNota(update, context):
    try:
        query = update.callback_query
        print(str(query.data))
        message = 'Obrigada pela sua nota: ' + str(query.data) 
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        print(str(e))


def cancel(update, context):
    return ConversationHandler.END


def main():
    try:
        
        token = '1015426963:AAGebg-CxZL93dl1LDJbDgTlFhrvZeW5j_k'
        updater = Updater(token=token, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', welcome))

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('feedback', feedback)],
            states={
                STATE1: [MessageHandler(Filters.text, inputFeedback)],
                STATE2: [MessageHandler(Filters.text, inputFeedback2)]
            },
            fallbacks=[CommandHandler('cancel', cancel)])
        updater.dispatcher.add_handler(conversation_handler)

        updater.dispatcher.add_handler(CommandHandler('nota', askForNota))
        updater.dispatcher.add_handler(CallbackQueryHandler(getNota))

        print("Updater no ar: " + str(updater))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
