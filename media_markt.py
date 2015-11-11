#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import os
import heapq
from sys import exit
from termcolor import colored

ID = int(os.environ["CUSTOMER_ID"])

if ID == "":
    exit('Unknown customer id')

serviceURL = 'http://www.serviceconnection.nu/MediaMarkt/servicestatus/View/OrderSummary.aspx?orderRecId={:d}'.format(ID)

logURL = 'http://www.serviceconnection.nu/MediaMarkt/servicestatus/View/EventLog.aspx?orderRecId={:d}'.format(ID)

serviceRequest = requests.get(serviceURL)

soup = BeautifulSoup(serviceRequest.text,"html.parser")

status = soup.find(id="ctl00_Body_OrderstatusLabel").text
date = soup.find(id="ctl00_Body_OrderdateLabel").text

print("Current Status:", status)
print("Current arrival date:", date, end="\n\n")

logRequest = requests.get('http://www.serviceconnection.nu/MediaMarkt/servicestatus/View/EventLog.aspx?orderRecId=221257367')

soup = BeautifulSoup(logRequest.text,"html.parser")

logtable = soup.find(id="ctl00_Body_OrderEventsGridView").find_all('tr')

headers = logtable[0].find_all('th')

tables = []
for i in range(1,len(logtable)):
    data = logtable[i].find_all('td')
    date = data[0].text
    s = data[1].text
    heapq.heappush(tables,(date,s))

tabletitle = colored('Log data','blue')
print("\t",tabletitle)
print(tabulate(tables,headers=[headers[0].text,headers[1].text]))
