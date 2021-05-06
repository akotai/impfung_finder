#!/usr/bin/env python

# Modules used
import requests
import time
from discord_webhook import DiscordWebhook

################### CONFIGURATION ###################
sleep_between_requests = 30 # [s]
discord_webhook_url = #WEBHOOK_URL


# URL getting availabilities for vaccination. These are just 2 examples, find the Hausarztpraxis providing vaccination closest to you.
urls = [
    'https://www.doctolib.de/availabilities.json?start_date=2021-05-06&visit_motive_ids=2772915&agenda_ids=456933&insurance_sector=public&practice_ids=16818&limit=5',
    'https://www.doctolib.de/availabilities.json?start_date=2021-05-06&visit_motive_ids=2748084&agenda_ids=450406&insurance_sector=public&practice_ids=106858&limit=5', 
]

# The original URL what you can visit to manually check for appointment availability.
original_urls = {}
original_urls[urls[0]] = "https://www.doctolib.de/praxis/muenchen/hausaerzte-in-giesing/booking/availabilities?motiveKey=Erstimpfung+Covid-19+%28AstraZeneca%29-5593&placeId=practice-16818&specialityId=5593&telehealth=false"
original_urls[urls[1]] = "https://www.doctolib.de/praxis/muenchen/hausarztpraxis-muenchen?fbclid=IwAR2cZeDHOkgMNGvX-kVHnyErXbQb8O4gNcB_a3c5_M8HQga2Fw4aqkzlhVU"

################### GET INITIAL REQUEST AND SAVE RESPONSE ###################
url_map = {}
for url in urls:
    print(url)
    response = requests.get(url)
    print(response.content)
    url_map[url] = response.content
    
################### CHECK FOR CHANGES IN RESPNSE ###################
try:
    while(1):
        for url in urls:
            time.sleep(sleep_between_requests)
            response = requests.get(url)
            if (response.content == url_map[url]):
                print("No change... No new appointment...")
            else:
                webhook = DiscordWebhook(url=discord_webhook_url, content='Appointment might be available for vaccination! ' + response.content.decode("utf-8") + original_urls[url])
                response = webhook.execute() 
                print("Old response: " + url_map[url])
                print("New response: " + response.content)
                url_map[url] = response.content
except:
    webhook = DiscordWebhook(url=discord_webhook_url, content='There was an issue with the last request... Please check what happened and restart me!')
    response = webhook.execute() 