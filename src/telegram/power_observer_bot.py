import telebot
import utils
import subscribers
import timing
from time import sleep
import storage

if __name__ == "__main__":   
    print("[Init] wait for internet")
    utils.wait_for_internet()
    print("[Init] internet is available")

    print("[Init] wait for system time sync")
    utils.wait_for_system_time_sync()
    print("[Init] system time is synchronized")

    print("[Init] get config")
    config = utils.get_config()

    print("[Init] init database")
    db = storage.Database(config["databasefile"])

    print("[Init] create time handler")
    time = timing.Timing(db, config["timedumpdelay"])

    print("[Init] create subscribers handler")
    subs = subscribers.SubscribersHandler(db)

    print("[Init] create bot handler")
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
    
    @bot.message_handler(commands=['subscribe', 'start'])
    def subscribe(message):
        print(f'[{message.from_user.id}] call: subscribe')
        msg = "Something went wrong :("
        if subs.add_subscriber(message.from_user.id):
            msg = "Subscribed"
        bot.send_message(message.from_user.id, msg)
        status(message)

    @bot.message_handler(commands=['unsubscribe'])
    def unsubscribe(message):
        print(f'[{message.from_user.id}] call: unsubscribe')
        msg = "Something went wrong :("
        if subs.remove_subscriber(message.from_user.id):
            msg = "Unsubscribed"
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
        utf8_bulb_emoji = '\U0001F4A1';
        bot.send_message(subscriber, utf8_bulb_emoji)
        bot.send_message(subscriber, msg)

    bot.infinity_polling()
    