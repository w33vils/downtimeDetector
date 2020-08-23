#!/usr/bin/env python

from multiping import multi_ping
import datetime
import telegram
import signal
import argparse
import sys


def parse_args(args=(sys.argv[1:])):
    parser = argparse.ArgumentParser(
        description="Monitor host uptime and alert on Telegram",
        prog='python -m dtime_detector'
    )
    parser.add_argument("-H", "--host", dest="host", metavar='', required=True,
                        help="Define host to be monitored")
    parser.add_argument("-t", "--token", dest="token", metavar='', required=True,
                        help="Specify bot token, from Bot Father")
    parser.add_argument("-c", "--chatId", dest="chat_id", metavar='', required=True,
                        help="Specify the Telegram chat ID to send the messages to")
    return parser.parse_args(args)

#Check if the host is up using multi-ping
def check_host(addrs):
    try:
        response, no_response = multi_ping(addrs, timeout=1, retry=2, ignore_lookup_errors=False) #Additional retries attempted within the timeout period
        if response:
            return True
        if no_response:
            return False
    except Exception as e:
        print("str(e)")

def current_timestamp():
    return datetime.datetime.now()

def time_difference(start, end):
    difference = end - start
    secs = str(difference.total_seconds())
    return str(datetime.timedelta(seconds=float(secs))).split(("."))[0]

def botsy(token, chat_id, telegram_message):
    bot = telegram.Bot(token)
    bot.sendMessage(chat_id=chat_id, text=telegram_message)


def monitor_uptime(): #Main code to monitor the host

    message = "✅ Host " +str(addrs[0]) + " is now being monitored."
    print(message)
    botsy(token, chat_id, message)

    while True: #loop through the check host function
        if check_host(addrs):
            continue
        else:
            down_time = current_timestamp()
            message = "☒ Host " +str(addrs[0])+ " is down as at " + str(down_time).split(".")[0]
            print(message)
            botsy(token, chat_id, message)
            counter = 0
            while not check_host(addrs):
                counter += 1
                current_time = current_timestamp()
                message = "☒" + str(addrs[0]) + " Has been down for " + time_difference(down_time,
                                                                                          current_time) + " HH:MM:SS"
                if counter == 600: # Modify the times to suit your needs
                    print(message)
                    botsy(token, chat_id, message)
                if counter == 1800:
                    print(message)
                    botsy(token, chat_id, message)
                if counter == 2700:
                    print(message)
                    botsy(token, chat_id, message)
                if counter == 3600:
                    message = "☒ Host\n" +str(addrs[0]) + " has been down for over an hour. No more alerts will be sent. "
                    botsy(token, chat_id, message)
                    print(message)
                    continue

            up_time = current_timestamp() #Get restoration time
            message = "✅ Host " + str(addrs[0]) + " is now up after " + time_difference(down_time, up_time) + " HH:MM:SS"
            print(message)
            botsy(token, chat_id, message)

if __name__ == "__main__":
    args = parse_args()
    addrs = [args.host]
    chat_id = args.chat_id
    token = args.token
    monitor_uptime()


