import telebot
import utils
import subscribers
import timing

if __name__ == "__main__":
    config = utils.get_config()

    time = timing.Timing(config["timedumpdelay"], config["timedumpfile"])

    subs = subscribers.SubscribersHandler(config["subscribersfile"])
    bot = telebot.TeleBot(utils.get_token(config["tokenfile"]))

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
    