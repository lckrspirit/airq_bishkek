#!/bin/python3

import requests
import json
import settings
import telebot

class GetAirInfo:
    def __init__(self, url, bot_token, channel):
        self.url = url
        self.channel = channel
        self.bot = telebot.TeleBot(bot_token, parse_mode='MARKDOWN')


    def get_info(self):
        request = requests.get(self.url)
        req_to_dict = json.loads(request.text)
        if req_to_dict['status'] == 'ok':
            return req_to_dict['data']
        else:
            ## TODO:Alert in private chat
            pass


    def get_wttr(self):
        return (requests.get("http://wttr.in/Bishkek?format=3")).text


    def last_airq(self, req):
        with open('/tmp/airq', 'r+') as file:
            last_req = file.read()
            if int(last_req) == req:
                return False
            elif req > int(last_req):
                return "⤴️"
            elif req < int(last_req):
                return "⤵️"


    def get_level(self, airq):
        if int(airq) <= 50:
            return "🍀", "Good"
        elif int(airq) <= 100:
            return "⚠️", "Moderate"
        elif int(airq) < 150:
            return "‼️", "Unhealthy"
        elif int(airq) < 200:
            return "‼️", "Unhealthy"
        elif int(airq) < 300:
            return "🤢", "Very Unhealthy"
        elif int(airq) > 350:
            return "☠️", "Hazardous"


    def notify(self, airq, updown, wttr):
        lvl, status = self.get_level(airq)
        body = F"*Bishkek Air Quality* {lvl}\n--\n"
        body += f"{updown} {str(airq)} ({status})\n--\n"
        body += f"{wttr}"
        self.bot.send_message(self.channel, body)
        with open('/tmp/airq', 'w') as tmp:
            tmp.write(str(airq))


    def run(self):
        req = self.get_info()
        last_req = self.last_airq(req['aqi'])
        if last_req:
            wttr = self.get_wttr()
            #self.notify(req['aqi'], last_req, wttr)
            print(req['aqi'], wttr)


app = GetAirInfo(settings.URL, settings.BOT_TOKEN, settings.CHANNEL)
app.run()
