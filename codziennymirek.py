#!/usr/bin/python3
# coding=utf-8
import time
import math
import os
import sys
from login import *


desirednumber = 2137
sendtoserver = False
generateimage = False
successMsg = '@{1}: to Ty zajmujesz dzisiaj miejsce #{0} w rankingu! \n#codzienny2137mirek [[faq](https://bouk.pl/codzienny2137mirek/)] #glupiewykopowezabawy'
failMsg = 'Dziś nikt nie ma miejsca #{0} w rankingu ( ͡° ʖ̯ ͡°) \n#codzienny2137mirek [[faq](https://bouk.pl/codzienny2137mirek/)] #glupiewykopowezabawy'
blacklist = ()


svgfile = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="852" height="852" viewBox="0 0 284 284" version="1.1" id="svg8">
    
    <rect style="fill:#2c2c2c" id="graybg" width="284" height="284" x="0" y="0" />
    <rect style="fill:#000000" id="fakebackground" width="284" height="200" x="0" y="0" />
    <image xlink:href="background.jpg" width="284" height="200" preserveAspectRatio="xMidYMid slice" id="background" x="0" y="0" style="display:{isbackground}" />
    <rect style="fill:#ffffff" id="fakeavatar" width="150" height="150" x="67" y="10" />
    <rect style="fill:#2c2c2c" id="midpasek" width="150" height="2" x="67" y="160" />
    <rect style="fill:#{sex}" id="pasek" width="150" height="4" x="67" y="162" />
    <image xlink:href="avatar.jpg" width="150" height="150" preserveAspectRatio="xMidYMid slice" id="avatar" x="67" y="10" style="display:{isavatar}" />
    <rect style="fill:#{color}" id="rankbg" width="75" height="30" x="142" y="121" />
    <text id="rank" x="179.5" y="143" style="text-align:center;text-anchor:middle;font-weight:bold;font-size:20px;font-family:'Liberation Sans';fill:#ffffff">#{rank}</text>
    <flowRoot>
        <flowRegion>
            <rect width="264" height="64" x="10" y="210" />
        </flowRegion>
        <flowPara style="text-align:center;text-anchor:middle;font-weight:bold;font-size:25px;font-family:'Liberation Sans';fill:#{color}">{login}</flowPara>
    </flowRoot>

</svg>'''




def searchranklist():
    bpage = int(math.ceil(desirednumber/25.0))
    hpage = bpage+1
    for j in range(50):
        print('searching page {0}'.format(bpage))
        ranklist = getranklist( bpage)
        #print ( ranklist)
        for i  in ranklist['data']:
            if i['rank'] == desirednumber and i['login'] not in blacklist:
                return i
        print('searching page {0}'.format(hpage))
        ranklist = getranklist( hpage)
        for i in ranklist['data']:
            if i['rank'] == desirednumber and i['login'] not in blacklist:
                return i
        bpage -= 1
        hpage += 1


def getcolors(code):
    colorlist = {
        "0": "339933",
        "1": "ff5917",
        "2": "BB0000",
        "5": "000000",
        "997": "ff5917",
        "998": "593787",
        "999": "bf9b30",
        "1001": "999999",
        "1002": "999999",
        "2001": "3f6fa0"
    }
    if str(code) in colorlist:
        return colorlist[str(code)]
    return 'ff5917'

def getsex(code):
    sexlist = {
        'male':'46ABF2',
        'female':'F246D0'
    }
    if str(code) in sexlist:
        return sexlist[str(code)]
    return 'ffffff'

def downloadimages(data):
  if generateimage or sendtoserver:
    isavatar = isbackground = False
    if 'background' in data:
        isbackground = True
        bgcommand = 'wget {0} -O background.jpg'.format(data['background'].replace(',w',',').replace(',q',','))
        os.system(bgcommand)

    if 'avatar' in data:
        isavatar = True
        bgcommand = 'wget {0} -O avatar.jpg'.format(data['avatar'].replace(',w',',').replace(',q',','))
        os.system(bgcommand)

    svg = svgfile.format(
        login=data['login'],
        rank=data['rank'],
        sex=getsex(data['sex']) if 'sex' in data else 'ffffff',
        color=getcolors(data['color']),
        isbackground='' if 'background' in data else 'none',
        isavatar='' if 'avatar' in data else 'none'
    )
    f = open('profile.svg', 'w')
    f.write(svg)
    f.close()
    os.system('inkscape -z -e {0}.png profile.svg'.format(data['login']))
    os.system('rm -f background.jpg ; rm -f avatar.jpg ; rm -f profile.svg')


def sendmessage(data):
    message = successMsg.format(data['rank'], data['login'])
    filename = '{0}.png'.format(data['login'])
    print(message)
    if sendtoserver:
        setcontent(message,  filename)


def failmessage():
    message = failMsg.format(desirednumber)
    print(message)
    if sendtoserver:
        setcontent(message, False)


if __name__ == "__main__":

    if '-h' in sys.argv:
        print('''Usage: {0} [-g|-s] [NUMBER]
        
    -g \t generate an image
    -s \t generate an image and send to server

    With no arguments the profile in given place is shown. The default number is {1}.
        '''.format(sys.argv[0],desirednumber))
    else:

        for i in sys.argv:
            if i.isnumeric():
                desirednumber = int(i)

        if '-g' in sys.argv:
            generateimage = True

        if '-s' in sys.argv:
            sendtoserver = True

        result = searchranklist()
        if(result):
            downloadimages(result)
            sendmessage(result)
        else:
            failmessage()
            pass

