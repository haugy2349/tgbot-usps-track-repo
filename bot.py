import telegram
import usps_api
import os

def get_tracker_info(tracking_number):
    usps = usps_api.MailPiece(str(tracking_number))
    return usps.track_summary() 

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the USPS tracking bot! Please enter your tracking number to get started.")

def fetch_tracking_number(update, context):
    tracking_number = update.message.text
    try:
        tracking_info = get_tracker_info(tracking_number)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tracking summary for {tracking_number}:\n {tracking_info}")
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Invalid tracking number.")

if __name__ == '__main__':
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = telegram.ext.Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = telegram.ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    fetch_tracking_number_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text & (~telegram.ext.Filters.command), fetch_tracking_number)
    dispatcher.add_handler(fetch_tracking_number_handler)

    updater.start_polling()
