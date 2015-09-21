#!/usr/bin/env pythpn

import urllib.request, re
from collections import OrderedDict

def firefoxSürümleriÇek():
	sonuçlar = dizinleriÇek("https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/")
	
	sonSonuçlar = []
	
	sonuçSözlüğü = OrderedDict()
	for i in sonuçlar:
		try:
			if '/' in i[1] and not 'rc' in i[1] and int(i[1].split('.')[0]+i[1].split('.')[1]) >= 15 and not 'funnelcake' in i[1]:
				sonuçSözlüğü[i[1].split('/')[0]] = "https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/" + i[0] + "win32/tr/"
		except: pass 
	
	for i in sonuçlar:
		if '/' in i:
			sonSonuçlar.append(i.split('/')[0])
	
	çevir = {"https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/0.8/win32/tr": "https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/0.8/win32/tr"}
	
	#for i in sonuçSözlüğü.values():
	#	dizinleriAl = dizinleriÇek(i)
	#	d = []
	#	for i in dizinleriAl:
	#		d.append(i[0])
	
	return sonuçSözlüğü

def dizinleriÇek(adres):
	adresAç = urllib.request.urlopen(adres).read()
	düzenliİfade = 'href\s*=\s*"(.*?)"\s*>(.*?)<'
	sonuçlar = re.findall(düzenliİfade, adresAç.decode("utf-8"))
	return sonuçlar

if __name__ == "__main__":
	print (firefoxSürümleriÇek())