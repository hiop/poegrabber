#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
# ==========================================
#      				POE LocGrabber
# Данный проект на стадии: "главное это работает"
#
#		█───█─████─████─█──█─███─█──█─████
#		█───█─█──█─█──█─██─█──█──██─█─█
#		█─█─█─████─████─█─██──█──█─██─█─██
#		█████─█──█─█─█──█──█──█──█──█─█──█
#		─█─█──█──█─█─█──█──█─███─█──█─████
#
#
#   ████─████─█─█─█──█─████─████─████─████──███
#   █────█──█─█─█─██─█─█──█─█──█─█──█─█──██─█
#   █─██─█──█─█─█─█─██─█──█─█────█──█─█──██─███
#   █──█─█──█─███─█──█─█──█─█──█─█──█─█──██─█
#   ████─████──█──█──█─████─████─████─████──███
#
# ==========================================
import urllib
import os
import lxml.html as html
from bs4 import BeautifulSoup
import urllib2
import win32clipboard
import re
import cgi
import sys
import codecs
from unidecode import unidecode
import json

def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        st = os.stat(path)
    except os.error:
        return False
    return True

def save_json(data):
	with codecs.open('data.json', mode='w') as outfile:
		json.dump(data, outfile)
def open_json():
	if exists('data.json') == False:
		save_json({"":""})
		
	with codecs.open('data.json', mode='r', encoding='utf-8' ) as data_file:    
		readf = json.load(data_file)
	#for k in readf:
	#	print(k)
	return readf
	
def findMap(mapString):
	global maps
	for k in maps:
		if mapString.find(k) > -1:
			return k
	print ("IS NOT A MAP");
	return 0;

		
def multireplace(str, arr, newstr=''):
	for k in arr:
		str = str.replace(k, newstr)
	return str

def spotItem(str):
	if str.find("Редкий") > -1:
		return 2
	return 1
	
#Настройки
grabbed = open_json();
isKnown = False;
originalItemName = "$empty";

#костыль
maps = ["Карта агоры", "Карта долины джунглей", "Карта кристальной шахты", "Карта пустыни", "Карта фактории", "Карта хибар", "Карта оазиса", "Карта пляжа", "Карта болот", "Карта грота", "Карта канала", "Карта канализации", "Карта пирамиды ваалСокровищница Азири", "Карта пещеры", "Карта высохшего озера", "Карта академии", "Карта помойного пруда", "Карта едких озёр", "Карта подземельяКошмар Актоны", "Карта фантасмагории", "Карта кладбища", "Карта дюн", "Карта ямы", "Карта мыса", "Карта погребальных камер", "Карта паучьего логова", "Карта поместья", "Карта чащи", "Карта города ваал", "Карта пристани", "Карта ипподрома", "Карта карьера", "Карта паучьего лесаСвятилище ОльмекаВакаваируа Туаху", "Карта ущелья", "Карта взморья", "Карта грязевого гейзера", "Карта катакомб", "Карта пепельного леса", "Карта развалин замка", "Карта берега", "Карта арены", "Карта атоллаВихрь хаоса", "Карта причала", "Карта гнезда пауков", "Карта камер", "Карта тропического островаНетронутый рай", "Карта погоста", "Карта трясины", "Карта музея", "Карта бухты", "Карта заросшей обители", "Карта прогулочного паркаЗал великих мастеров", "Карта склепаИспытание труса", "Карта рифаМао Кун", "Карта храмаБогадельня Паршута", "Карта заросшей обители", "Карта фруктового сада", "Карта подворья", "Caer Blaidd.логово стаи", "Карта арсенала", "Карта колоннады", "Карта недр", "Карта террасы","Особняк Просперусов", "Карта подземной реки", "Карта окрестностей", "Карта замка", "Карта подземного моря", "Проклятый клад Обы", "Карта камеры пыток", "Карта базара", "Карта подземного моря", "Карта раскопок", "Карта пустоши", "Карта верфи", "Карта храма из слоновой кости", "Карта некрополиса", "Карта резиденции","Смерть и налоги", "Карта плоскогорья", "Карта хранилища", "Карта крематория", "Карта устья реки", "Площадь Винктара", "Карта серной пустоши", "Карта висячих садов", "Карта водотоков", "Карта теснины", "Карта логова", "Карта скриптория", "Карта площади", "Карта маяка", "Карта родников", "Карта лабиринта", "Карта минеральных озёр", "Карта дворца", "Карта вулкана", "Карта святыни", "Карта храма ваал", "Карта мрачного леса", "Карта бездны", "Карта колизея", "Карта сердца", "Карта логова Гидры", "Карта кузницы Феникса", "Карта лабиринта Минотавра", "Карта ямы Химеры"]

f = codecs.open('iteminfo.txt')
line = f.readline()
linecount = 0
needLine = None;
oldLine = None;
itemName = None;
rawItemName = None;
itemType = None;
while line:
	if(linecount == 0):
		needLine = spotItem(line);
		itemType = line;
	
	if(linecount == needLine):
		if line.find("--------") > -1:
			line = oldLine;
		
		#print " "+rawItemName
		line = line.replace("\n", "")
		line = line.replace("\r", "")
		rawItemName = line;
		line = line.replace(" ", "_")
		itemName = line;
	linecount = linecount + 1;
	oldLine = line;
	if line.find("пророчество") > -1:
		itemType = "Пророчество"
		#print "Prophecy";
	line = f.readline()
f.close()

	
#print(grabbed.get(rawItemName.decode("utf-8")));
if rawItemName.find("Карта") > -1 and itemType.find("Уникальный") == -1:
	itemName = findMap('u'+rawItemName);
	itemName = itemName.replace(" ", "_");
	rawItemName = itemName;

possibleOrgItemName = grabbed.get(rawItemName.decode("utf-8"));
if possibleOrgItemName != None:
	isKnown = True;
	print ("FIND IT!!11" + possibleOrgItemName);
	originalItemName = possibleOrgItemName.encode("1251");
	
if isKnown == False:
	if itemType != "Пророчество":
		print "Not Prophecy URL"
		DOWNLOAD_URL = "https://pathofexile-ru.gamepedia.com/"+urllib.quote_plus(itemName)
	else:
		print "Prophecy URL"
		DOWNLOAD_URL = "https://pathofexile-ru.gamepedia.com/"+urllib.quote_plus(itemType)
		
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib2.Request(DOWNLOAD_URL, headers=hdr)
	encoding = None;
	page = None;
	try:
		page = urllib2.urlopen(req)
		_, params = cgi.parse_header(page.headers.get('Content-Type', ''))
		encoding = params.get('charset', 'utf-8')

	except urllib2.HTTPError, e:
		#print e.fp.read()
		print "item problem";
		
	if page == None:
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardText("$none")
		win32clipboard.CloseClipboard()
		sys.exit("Страница не найдена")
		
	content = page.read().decode(encoding)
	soup = BeautifulSoup(content, 'lxml')

	#Тут типа ищем
	originalItemName = "$empty";
	#print itemType


	if itemType.find("Гадальная карта") > -1:
		tree = html.fromstring('u'+content)
		originalItemName = tree.xpath(u'//*[@id="mw-content-text"]/p[1]/text()[1]')
		originalItemName = multireplace(originalItemName[0], [u') - это', u'(']);
		originalItemName = originalItemName[1:]
	elif itemType == "Пророчество":
		print("Prophecy handle");
		tree = html.fromstring(content)
		originalItemName = tree.xpath('.//td/text()'.format(None))
		wantedProphecy = False;
		for td in originalItemName:
			if wantedProphecy == True:
				originalItemName = td
				print("Prophecy finded! "+originalItemName);
				wantedProphecy = False;
				break;
			#print rawItemName
			#print rawItemName.decode('utf-8')
			#print type(rawItemName)
			if td.find(rawItemName.decode('utf-8')) > -1:
				wantedProphecy = True;
	else:
		originalItemName = soup.find('span', {'class':'text-color -original'}).getText();
		originalItemName = originalItemName.split('.')[1][1:];

print(originalItemName)
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
if originalItemName == "$empty":
	win32clipboard.SetClipboardText(originalItemName)
else:
	win32clipboard.SetClipboardText("|"+originalItemName)
	grabbed[rawItemName] = originalItemName;
	save_json(grabbed);
win32clipboard.CloseClipboard()
codecs.open('iteminfo.txt', 'w').close()