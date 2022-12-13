import telebot
import utils
import subscribers
import timing
from time import sleep
import logging

if __name__ == "__main__":
    print("[Init] wait for internet")
    utils.wait_for_internet()
    sleep(5)
    print("[Init] internet is available")

    print("[Init] get config")
    config = utils.get_config()

    print("[Init] create time handler")
    time = timing.Timing(config["timedumpdelay"], config["timedumpfile"])

    print("[Init] create subscribers handler")
    subs = subscribers.SubscribersHandler(config["subscribersfile"])

    print("[Init] create bot handler")
    bot_logger = logging.getLogger('TeleBot')
    bot_logger.setLevel(logging.DEBUG)
    bot = None
    while not bot:
        try:
            bot = telebot.TeleBot(utils.get_token(config["tokenfile"]))
        except:
            print("[Init] bot connection error. Reconnect...")
            sleep(5)
            continue

    print("[Init] set bot commands")
    bot.set_my_commands([
        telebot.types.BotCommand("subscribe", "to get notifications"), 
        telebot.types.BotCommand("unsubscribe", "to not get notifications"), 
        telebot.types.BotCommand("status", "to get current status")
    ])
    
    @bot.message_handler(commands=['subscribe'])
    def subscribe(message):
        print(f'[{message.from_user.id}] call: subscribe')
        subs.add_subscriber(message.from_user.id)
        msg = "Subscribed"
        if not subs.is_subscriber(message.from_user.id):
            msg = "Something went wrong :("
        bot.send_message(message.from_user.id, msg)
        status(message)

    @bot.message_handler(commands=['unsubscribe'])
    def unsubscribe(message):
        print(f'[{message.from_user.id}] call: unsubscribe')
        subs.remove_subscriber(message.from_user.id)
        msg = "Unsubscribed"
        if subs.is_subscriber(message.from_user.id):
            msg = "Something went wrong :("
        bot.send_message(message.from_user.id, msg)

    @bot.message_handler(commands=['status'])
    def status(message):
        print(f'[{message.from_user.id}] call: status')
        msg = f"Uptime: {utils.convert_duration(time.get_uptime())}\n"
        msg += f"Start time: {utils.convert_date(time.get_start_time())}"
        bot.send_message(message.from_user.id, msg)

    print("Running...")
    msg =  f"Power off: {utils.convert_date(time.get_stop_time())}\n"
    msg += f"Power on: {utils.convert_date(time.get_start_time())}\n"
    msg += f"Downtime: {utils.convert_duration(time.get_downtime())}"
    for subscriber in subs.get_list():
        print(f"Sending notification to [{subscriber}]")
        bot.send_message(subscriber, msg)

    bot.infinity_polling()
    