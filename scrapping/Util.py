from scrapping.Frequency import *

def isHour(tag):
    return tag.has_attr('nowrap')

def incrementColumn(current,attrs):
    if 'colspan' in attrs.keys():
        return current+int(attrs['colspan'])
    else:
        return current+1

def incrementDuration(current,attrs):
    if 'rowspan' in attrs.keys():
        return current+int(attrs['rowspan'])
    else:
        return current+1

def getDataFromStrangeClasses(text):
    if text.find('ora')==-1:
        return None
    return text[text.find('ora'):len(text)-1].split()[1].split('-')

def checkNotInChild(tag):
    notInChild=[]
    classes=tag.text.strip('\n').replace('\xa0','').split('\n')
    for child in tag.find_all('span'):
        cText=child.text.strip('\n').replace('\xa0','')
        if cText in classes:
            classes.remove(cText)

    return classes

def getFrequency(text):
    if text.find('sapt. 1')!=-1:
        return Frequency.IMPAR
    elif text.find('sapt. 2')!=-1:
        return  Frequency.PAR
    else:
        return Frequency.FULL

def getGroupForStrangeLabs(elem):
    if elem[3].find('sgr.')!=-1:
        elem[0]=[elem[3][4:9]]
    elif elem[3].find('gr.')!=-1:
        elem[0]=[elem[3][3:6]+'/1',elem[3][3:6]+'/2']
    return elem