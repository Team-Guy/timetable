import requests
from bs4 import BeautifulSoup
from scrapping.Day import Day
from scrapping.Processor import *
from scrapping.Link import Link

def getInfo(link):
    result= requests.get(link)

    soup=BeautifulSoup(result.content,'lxml')

    rows=soup.find_all('tr')
    rows.pop(0)
    rows.pop(0)
    toate=[]
    groups=getGroups(rows.pop(0))
    for day in Day.days.values():
        toate.append(processDay(rows[:12],day,groups))
        rows.pop(0)
        rows=rows[12:]
    # processDay(rows[:12],Day.MONDAY)
    f=open("ore.out","w")
    for zi in toate:
        for ora in zi:
            f.write(str(ora)+'\n')



