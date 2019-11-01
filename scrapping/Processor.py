from scrapping.ClassType import ClassType
from scrapping.Util import *
from scrapping.MaterieTemp import MaterieTemp

def processMainHour(tag,startHour,groups,column,day):
    attrs=tag.attrs
    classes=checkNotInChild(tag)
    classType=ClassType.getClassType(attrs['class'][0])
    duration=0
    groupsLenght=0
    grupe=[]
    groupsLenght=incrementColumn(groupsLenght,attrs)
    duration=incrementDuration(duration,attrs)
    for i in range(column,column+groupsLenght):
        grupe.append(groups[i])
    ore=[]
    for text in classes:
        x=getDataFromStrangeClasses(text)
        if x:
            ora=[grupe, int(x[0]), int(x[1])-int(x[0]), text,getFrequency(text)]
        else:
            ora=[grupe, startHour, duration, text,getFrequency(text)]
        ora=getGroupForStrangeLabs(ora)
        ora = MaterieTemp(ora[0], ora[1], ora[2], ora[3], ora[4], day,classType)
        ore.append(ora)
    return ore


def processChildHour(tag,startHour,parrentAttrs,groups,column,day):
    attrs = tag.attrs
    text=tag.text.strip('\n').replace('\xa0','')
    classType = ClassType.getClassType(attrs['class'][0])
    duration = 0
    groupsLenght = 0
    grupe = []
    groupsLenght = incrementColumn(groupsLenght, parrentAttrs)
    duration = incrementDuration(duration, parrentAttrs)
    for i in range(column, column + groupsLenght):
        grupe.append(groups[i])
    x = getDataFromStrangeClasses(text)
    if x:
        ora = [grupe, int(x[0]), int(x[1])-int(x[0]), text,getFrequency(text)]
    else:
        ora = [grupe, startHour, duration, text,getFrequency(text)]
    ora = getGroupForStrangeLabs(ora)
    ora=MaterieTemp(ora[0],ora[1],ora[2],ora[3],ora[4],day,classType)
    return ora

def getGroups(groupHeader):
    l=[]
    for x in groupHeader:
        if x!='\n':
            l.append(x.string)
    return l

def processDay(rows,day,groups):
    ore=[]
    for i in range(0,len(rows)):
        startHour=int(rows[i].find(isHour).text.split('-')[0])
        column=0
        for item in rows[i].find_all('td'):
            if item.text!='\xa0':
                for ora in processMainHour(item,startHour,groups,column,day):
                    ore.append(ora)
                for extra in item.find_all('span'):
                    ore.append(processChildHour(extra,startHour,item.attrs,groups,column,day))
            column=incrementColumn(column,item.attrs)


    return ore
