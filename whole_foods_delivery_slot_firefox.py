import bs4

from selenium import webdriver

import sys
import time
import os
import re
import pickle
from time import gmtime, strftime

max_not_available = 10

def get_now():
   return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def getWFSlot(productUrl):
   driver = webdriver.Firefox()
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   for i in reversed(range(0, 45)):
      time.sleep(1)
      print(f"Waiting {i} more seconds before continuing...")
   # time.sleep(60)
   no_open_slots = True

   while no_open_slots:
      driver.refresh()
      html = driver.page_source
      soup = bs4.BeautifulSoup(html, features="html.parser")
      time.sleep(4)

      slot_patterns = ['Next available', '1-hour delivery windows', '2-hour delivery windows']
      try:
         next_slot_text = soup.find('h4', class_ ='ufss-slotgroup-heading-text a-text-normal').text
         if any(next_slot_text in slot_pattern for slot_pattern in slot_patterns):
            print('SLOTS OPEN!')
            os.system('say "Slots for delivery opened!"')
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         pass

      try:
         slot_opened_text = "Not available"
         all_dates = soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"})
         for each_date in all_dates:
            if slot_opened_text not in each_date.text:
               print('SLOTS OPEN!')
               os.system('say "Slots for delivery opened!"')
               no_open_slots = False
               time.sleep(1400)
      except AttributeError:
         pass

      try:
         regex = re.compile('([0-9]+) items not available')
         button_text = soup.find('button', class_='slotButton').text
         soup.find('button', class_='a-spacing-micro')
         matches = regex.search(button_text)
         sentence = ' '.join(button_text.split())
         os.system(f'say "Slots are opened! {sentence}"')
         print(f"Regex Match: {re.search('([0-9]+) items not available', button_text)}")
         if (matches is not None) and (int(matches.group(1)) < max_not_available):
            no_open_slots = False
            if (int(matches.group(1)) > 0):
               li_items = soup.find_all('li', class_='a-spacing-micro')
               for item in li_items:
                  print(f"Not available: {item.text.strip()}")
                  os.system(f'say "{item.text.strip()} is not available."')
            else:
               os.system(f'say "All items are available!"')
               
            print(f'-----------------------------------------------------')
            print(f'-----------------------------------------------------')
            print(f'{get_now()} SLOT AVAILABLE!!!!')
            print(f'-----------------------------------------------------')
            print(f'-----------------------------------------------------')
            
         for i in reversed(range(0, 240)):
            time.sleep(1)
            print(f"Waiting {i} more seconds before restarting.  Complete your order before a refresh!")
         os.system(f'say "Timed out.  Restarting slot search."')
      except AttributeError: 
            print(f' {get_now()} NO SLOTS OPEN!')


getWFSlot('https://www.amazon.co.uk/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


