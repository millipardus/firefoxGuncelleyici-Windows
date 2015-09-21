#!/usr/bin/env python

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import qInstallMessageHandler, QSize

from PyQt5.QtCore import *

import os, re
import TümSürümleriÇek

import urllib.request
import sys
import configparser
import winreg

class FirefoxGuncelleyici (QWidget):
    def __init__(self):
        super().__init__()
        
        self.resim = QPixmap(os.path.join("kaynaklar", "güncelle.png"))
        self.resim2 = QPixmap(os.path.join("kaynaklar", "güncel.png"))
        self.resim3 = QPixmap(os.path.join("kaynaklar", "İndir.png"))

        
        self.firefoxGüncelleyici = güncellemeİşlemleri()
        self.firefoxGüncelleyici.bitti[int].connect(self.sinyalAl)
        
        ffSS = FireFoxSonSürüm()
        ffSS.komut[str].connect(self.sonSurumGetir)
        ffSS.start()
        
        self.sürümleriGetirSınıf = SürümleriGetir()
        self.sürümleriGetirSınıf.gonder[dict].connect(self.Yukle)
        self.sürümleriGetirSınıf.start()
        
        
        
        #QObject.connect(self.firefoxGüncelleyici, SIGNAL("1"), lambda: self.sinyalAl(1))
        #QObject.connect(self.firefoxGüncelleyici, SIGNAL("2"), lambda: self.sinyalAl(2))
        
        #self.firefoxGüncelleyici.bitti.connect(lambda: self.sinyalAl(1))
        
        self.gorunum = QVBoxLayout(self)
        
        self.ayarAyracı = configparser.ConfigParser()
        
        self.resize(300, 70)
        self.ortala(self)
        self.setWindowTitle("Firefox Güncelleyici")
        self.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        
        self.firefoxDiziniTespit()
        self.firefoxSurumAl()
        #self.firefoxSonSürümTespit()
        
        
        self.guncellemeDugmesi = Dugme("Firefox'u Güncelleyin !", self)
        self.guncellemeDugmesi.sinyalDugme[int].connect(self.dugmeIslemleri)
        self.guncellemeDugmesi.setIcon(QIcon(self.resim))
        
        #self.guncellemeDugmesi = QPushButton("Firefox'u Güncelleyin !", self)
        #self.guncellemeDugmesi.setIcon(QIcon(self.resim))
        
        
        self.firefoxSurumu_      = QLabel("Firefox Sürümü: "+self.firefoxSurumu, self)
        #label.fontMetrics().boundingRect(label.text()).width()
        self.firefoxSurumu_.setMaximumWidth(self.firefoxSurumu_.fontMetrics().boundingRect(self.firefoxSurumu_.text()).width()+1)
        self.firefoxSurumYenile  = QLabel("| <a href='#'>Yenile</a>", self)
        self.firefoxSurumYenile.linkActivated.connect(self.SurumYenile)
        self.firefoxDiziniEtiket = QLabel("Firefox Dizini: " + self.firefoxDizini, self)
        self.firefoxSonSürümü    = QLabel("Firefox Son Sürümü: ", self)
        self.firefoxSurumSecimi  = QComboBox(self)
        #self.firefoxSurumSecimi.addItems(self.firefoxunTumSurumleri.keys())
        self.SeçilenSurumuİndir = QPushButton("Kur", self)
        self.SeçilenSurumuİndir.setMaximumWidth(75)
        self.SeçilenSurumuİndir.setIcon(QIcon(self.resim3))
        self.SeçilenSurumuİndir.clicked.connect(self.SecilenSurumKur)
        
        
        self.guncellemeDugmesi.clicked.connect(self.firefoxGuncelle)

        self.alt_gorunum = QHBoxLayout(self)
        self.alt_gorunum.addWidget(self.firefoxSurumSecimi)
        self.alt_gorunum.addWidget(self.SeçilenSurumuİndir)       
        
        self.alt_gorunum2 = QHBoxLayout(self)
        self.alt_gorunum2.addWidget(self.firefoxSurumu_)
        self.alt_gorunum2.addWidget(self.firefoxSurumYenile)
        
        #self.setLayout(self.gorunum)

        self.gorunum.addWidget(self.guncellemeDugmesi)
        self.gorunum.addWidget(self.firefoxSonSürümü)
        self.gorunum.addLayout(self.alt_gorunum2)
        self.gorunum.addWidget(self.firefoxDiziniEtiket)
        self.gorunum.addLayout(self.alt_gorunum)
    
    def dugmeIslemleri(self, i):
        try:
            if i == 1:
                if self.firefoxSonSurum == self.firefoxSurumu:
                    self.guncellemeDugmesi.setText("Yine De İndirmek İstiyorum !")
                    self.guncellemeDugmesi.setEnabled(True)
                    self.guncellemeDugmesi.setIcon(QIcon(self.resim3))
            elif i == 2:
                if self.firefoxSonSurum == self.firefoxSurumu:
                    self.guncellemeDugmesi.setText("Firefox En Yeni Sürümde !")
                    self.guncellemeDugmesi.setEnabled(False)
                    self.guncellemeDugmesi.setIcon(QIcon(self.resim2))
        except:
            pass
    
    def sonSurumGetir(self, katar):
        self.firefoxSonSurum = katar
        self.firefoxSonSürümü.setText("Firefox Son Sürümü: "+self.firefoxSonSurum)
        if self.firefoxSonSurum == self.firefoxSurumu:
            self.guncellemeDugmesi.setText("Firefox En Yeni Sürümde !")
            self.guncellemeDugmesi.setIcon(QIcon(self.resim2))
            self.guncellemeDugmesi.setEnabled(False)
            
            #self.guncellemeDugmesi.enterEvent(self.yineDeYukle)
        else: 
            self.guncellemeDugmesi.setText("Firefox'u Güncelleyin !")
            self.guncellemeDugmesi.setIcon(QIcon(self.resim))
    
    def Yukle(self, bilgi):
        self.firefoxSurumSecimi.addItems(bilgi.keys())
        self.firefoxunTumSurumleri = bilgi
    
    def SecilenSurumKur(self):
        self.sürümKurBelirteç = seçilenSürümKur(self.firefoxSurumSecimi.currentText(), self.firefoxunTumSurumleri)
        self.sürümKurBelirteç.sinyal[int].connect(self.sinyalAl)
        self.sürümKurBelirteç.sinyal2[str].connect(self.dosyaCalistir)
        self.sürümKurBelirteç.start()
        
        
        """try:
            urllib.request.urlretrieve("https://download.mozilla.org/?product=firefox-{}&os=win&lang=br".format(self.firefoxSurumSecimi.currentText()), "firefoxKur.exe")
        except:
            urllib.request.urlretrieve("https://download.mozilla.org/?product=firefox-{}-SSL&os=win&lang=br".format(self.firefoxSurumSecimi.currentText()), "firefoxKur.exe")
        
        os.startfile("firefoxKur.exe")"""
        
        #os.startfile(exeAdı)

    
        
    
    def yineDeYukle(self):
        self.guncellemeDugmesi.setText("Yine De Yüklemek İçin Tıklayın !")
        self.guncellemeDugmesi.setEnabled(True)
    
    def firefoxSonSürümTespit(self):
        adresKod = urllib.request.urlopen("https://www.mozilla.org/en-US/firefox/all/").read()
        
        duzenli_ifade ='data-latest-firefox="(.*?)"'
        self.firefoxSonSürüm = re.findall(duzenli_ifade, adresKod.decode())[0]
        
    def dosyaCalistir(self, dosya):
        
        os.startfile(dosya) 
    
    def firefoxGuncelle(self):
        self.firefoxGüncelleyici.start()
        """self.pencereBirÇiz()
    
        exeDosyaları = TümSürümleriÇek.dizinleriÇek("https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/")
        dosyaAdres = ""
        dosyaAd = ""
        
        for i in exeDosyaları:
            if 'Setup' in i[1] and 'Stub' in i[1]:
                dosyaAdres = "https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/" + i[0]
                dosyaAd = i[1]
        
        if dosyaAd == "":
            for i in exeDosyaları:
                if i[1].endswith('.exe'):
                    dosyaAdres = "https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/" + i[0]
                    dosyaAd = i[1]
        
        urllib.request.urlretrieve(dosyaAdres, dosyaAd)
        
        
        
        #urllib.request.urlretrieve("https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=tr", "firefoxKurulum.exe")
        #os.startfile("firefoxKurulum.exe")
        
        self.pencereİkiÇiz()
        os.startfile(dosyaAd)
        
        
        
        #firefoxGüncelleyici = güncellemeİşlemleri()
        #self.firefoxGüncelleyici.start()
        """
    
    def SurumYenile(self):
        try:
            self.firefoxSurumAl()
            self.firefoxSurumu_.setText("Firefox Sürümü: "+self.firefoxSurumu)
            self.firefoxSurumu_.setMaximumWidth(self.firefoxSurumu_.fontMetrics().boundingRect(self.firefoxSurumu_.text()).width()+1)
            if self.firefoxSonSurum == self.firefoxSurumu:
                self.guncellemeDugmesi.setText("Firefox En Yeni Sürümde !")
                self.guncellemeDugmesi.setEnabled(False)
                self.guncellemeDugmesi.setIcon(QIcon(self.resim2))
        except: pass
    
    def firefoxSurumAl(self):
        if self.firefoxDizini != "Bulunamadı":
            if 'platform.ini' in os.listdir(self.firefoxDizini):
                self.ayarAyracı.read(self.firefoxDizini+os.sep+"platform.ini")
                self.firefoxSurumu = self.ayarAyracı["Build"]["Milestone"]
            else:
                self.firefoxSurumu = "Bulunamadı"
        else:
            self.firefoxSurumu = "Bulunamadı"
    
    def firefoxDiziniTespit(self):
        #uygulamaDosyaları = os.popen("echo %ProgramFiles%").read().strip()
        anahtar = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Mozilla")
        #deger = winreg.QueryValueEx(anahtar, "(Varsayılan)")[0]
        #print (deger)
        
        dizinler = self.listele(anahtar)
        
        
        İçindeFirefoxOlanlar = []
        for i in dizinler:
            if 'mozilla' in i.lower() or 'firefox' in i.lower():
                İçindeFirefoxOlanlar.append(i)
        
        if not 'Mozilla Firefox' in İçindeFirefoxOlanlar:
            self.firefoxDizini = self.dizindenTespit()
        else:
            try:
                anahtar = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Mozilla\\Mozilla Firefox\\")
                anahtar2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Mozilla\\Mozilla Firefox\\"+self.listele(anahtar)[0]+"\\Main")
                deger = winreg.QueryValueEx(anahtar2, "Install Directory")[0]
                self.firefoxDizini = deger
            except:
                self.firefoxDizini = self.dizindenTespit()

    def dizindenTespit(self):
        firefoxDizini = "Bulunamadı"
        
        uygulamalarDizini = os.popen("echo %ProgramFiles%").read().strip()
        İçindeFirefoxOlanlar = []
        
        for i in os.listdir(uygulamalarDizini):
            if 'firefox' in i.lower():
                İçindeFirefoxOlanlar.append(i)
        
        if len(İçindeFirefoxOlanlar) > 1:
            yeniİçindeFirefoxOlanlar = []
            for i in İçindeFirefoxOlanlar:
                if 'mozilla' in i.lower():
                    yeniİçindeFirefoxOlanlar.append(i)
            if yeniİçindeFirefoxOlanlar == [] or len(yeniİçindeFirefoxOlanlar) > 1:
                firefoxDizini = "Bulunamadı"
            else:
                firefoxDizini = yeniİçindeFirefoxOlanlar[0]
        
        else:
            firefoxDizini = İçindeFirefoxOlanlar[0]
            
        return firefoxDizini
    
    def listele(self, anahtar):
        i = 0
        dizinler = []
        while 1:
            try:
                anahtar_al = winreg.EnumKey(anahtar, i)
                dizinler.append(anahtar_al)
                i += 1
            except WindowsError:
                break
        
        return dizinler
    
    #@pyqtSlot(int)
    def sinyalAl(self, i):
        if i == 1:
            self.pencereBirÇiz()
        elif i == 2:
            self.pencereİkiÇiz()
        elif i == 3:
            self.pencereÜçÇiz()
        elif i == 4:
            self.pencereDörtÇiz()
        elif i == 5:
            self.pencere1.close()
        elif i == 6:
            self.pencere2.close()
        elif i == 7:
            self.pencere3.close()
        elif i == 8:
            self.pencere4.close()
        elif i == 11:
            self.pencereÜçÇiz("")
        elif i == 12:
            self.pencereİkiÇiz("")
    
    def ortala(self, penc):
        a = QDesktopWidget().availableGeometry().center()
        b = penc.frameGeometry()
        b.moveCenter(a)
        penc.move(b.topLeft())
    
    def pencereBirÇiz(self):
        self.pencere1 = QDialog()
        self.pencere1.setFixedSize(140, 30)
        self.ortala(self.pencere1)

        gorunum_ = QHBoxLayout(self.pencere1)
        self.pencere1.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        self.pencere1.setWindowTitle("Firefox Güncelleniyor")
        
        resim = QLabel(self.pencere1)
        resim.setPixmap(QPixmap(os.path.join("kaynaklar", "güncelle.png")))
        
        etk1 = QLabel("Güncelleme dosyası indiriliyor...", self.pencere1)
        
        gorunum_.addWidget(resim)
        gorunum_.addWidget(etk1)
        self.pencere1.show()
    def pencereİkiÇiz(self, komut=None):
        self.pencere2 = QDialog()
        self.pencere2.resize(140, 30)
        self.ortala(self.pencere2)
        gorunum_ = QHBoxLayout(self.pencere2)
        self.pencere2.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        if komut == None:
            self.pencere2.setWindowTitle("Firefox Güncelleniyor")
        else:
            self.pencere2.setWindowTitle("Dosya Zaten Var")

        resim = QLabel(self.pencere2)
        resim.setPixmap(QPixmap(os.path.join("kaynaklar", "güncelle.png")))
        if komut == None:
            etk2 = QLabel("Güncelleme dosyası başarıyla indirildi !\nGüncelleme dosyası çalıştırılıyor...", self.pencere2)
        else:
            etk2 = QLabel("Aranan güncelleme dosyası zaten mevcut !\nGüncelleme dosyası çalıştırılıyor...", self.pencere2)
        gorunum_.addWidget(resim)
        gorunum_.addWidget(etk2)
        self.pencere2.show()
    
    def pencereÜçÇiz(self, komut=None):
        self.pencere3 = QDialog()
        self.pencere3.resize(140, 30)
        self.ortala(self.pencere3)
        gorunum_ = QHBoxLayout(self.pencere3)
        self.pencere3.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        if komut== None:
            self.pencere3.setWindowTitle("Firefox İndiriliyor")
        else:
            self.pencere3.setWindowTitle("Dosya Zaten Var")
        resim = QLabel(self.pencere3)
        resim.setPixmap(QPixmap(os.path.join("kaynaklar", "İndir.png")))
        if komut == None:
            etk2 = QLabel("Kurulum dosyası başarıyla indirildi !\nKurulum dosyası çalıştırılıyor...", self.pencere3)
        else:
            etk2 = QLabel("Aranan kurulum dosyası zaten mevcut !\nKurulum dosyası çalıştırılıyor...", self.pencere3)
        gorunum_.addWidget(resim)
        gorunum_.addWidget(etk2)
        self.pencere3.show()
    
    def pencereDörtÇiz(self):
        
        self.pencere4 = QDialog()
        self.pencere4.resize(140, 30)
        self.ortala(self.pencere4)
        gorunum_ = QHBoxLayout(self.pencere4)
        self.pencere4.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        self.pencere4.setWindowTitle("Firefox İndiriliyor")
        
        resim = QLabel(self.pencere4)
        resim.setPixmap(QPixmap(os.path.join("kaynaklar", "İndir.png")))
        etk1 = QLabel("Kurulum dosyası indiriliyor...", self.pencere4)
        
        gorunum_.addWidget(resim)
        gorunum_.addWidget(etk1)

        self.pencere4.show()

class güncellemeİşlemleri(QThread):
    bitti = pyqtSignal(int)
    
    def __init__(self, ust=None):
        super(QThread, self).__init__(ust)
        
    def run(self):

        #self.pencereBirÇiz()
    
        exeDosyaları = TümSürümleriÇek.dizinleriÇek("https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/")
        dosyaAdres = ""
        dosyaAd = ""

        
        
        for i in exeDosyaları:
            if 'Setup' in i[1] and 'Stub' in i[1]:
                dosyaAdres = "https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/" + i[0]
                dosyaAd = i[1]

        if dosyaAd == "":
            for i in exeDosyaları:
                if i[1].endswith('.exe'):
                    dosyaAdres = "https://ftp.mozilla.org/pub/firefox/releases/latest/win32/tr/" + i[0]
                    dosyaAd = i[1]
        try:
            if not dosyaAd in os.listdir('.'):
                self.bitti.emit(1)
                urllib.request.urlretrieve(dosyaAdres, dosyaAd)
                self.bitti.emit(5)
                self.bitti.emit(2) #self.pencereİkiÇiz()
                self.sleep(2)
                self.bitti.emit(6)
            else:
                self.bitti.emit(12)
                self.sleep(2)
                self.bitti.emit(6)
            
            os.startfile(dosyaAd)
        except: pass

class Dugme(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        
    sinyalDugme = pyqtSignal(int)
    
    def enterEvent(self, QEvent):
        self.sinyalDugme.emit(1)
        
    def leaveEvent(self, QEvent):
        self.sinyalDugme.emit(2)
        

class seçilenSürümKur(QThread):
    sinyal = pyqtSignal(int)
    sinyal2 = pyqtSignal(str)
    def __init__(self, seçilenSürüm, firefoxunTumSurumleri):
        super(QThread, self).__init__()
        self.seçilenSürüm = seçilenSürüm
        self.firefoxunTumSurumleri = firefoxunTumSurumleri
    
    def run(self):
        adr = self.firefoxunTumSurumleri[self.seçilenSürüm]
        #print (adr)
        adresKod = TümSürümleriÇek.dizinleriÇek(adr)
        

        for i in adresKod:
            if i[1].endswith(".exe") and not 'stub' in i[1].lower():
                exeDosyası = i[0]
                exeAdı = i[1]


        if not exeAdı in os.listdir('.'):
            #print(self.firefoxunTumSurumleri[self.seçilenSürüm]+exeDosyası, exeAdı)
            self.sinyal.emit(4) # firefox dosyası indiriliyor...
            urllib.request.urlretrieve(self.firefoxunTumSurumleri[self.seçilenSürüm]+exeDosyası, exeAdı)
            self.sinyal.emit(8) # pencereyi kapat.
            self.sinyal.emit(3) # dosya çalıştırılıyor...
            self.sleep(2)
            self.sinyal.emit(7) # pencereyi kapat
        else:
            self.sinyal.emit(11)
            self.sleep(2)
            self.sinyal.emit(7)
        try:
            os.startfile(exeAdı)
        except: pass
            
            
        #self.sinyal2.emit(exeAdı)
                
class SürümleriGetir(QThread):
    def __init__(self):
        super().__init__()
    
    gonder = pyqtSignal(dict)
    def run(self):
        self.firefoxunTumSurumleri = TümSürümleriÇek.firefoxSürümleriÇek()
        self.gonder.emit(self.firefoxunTumSurumleri)

class FireFoxSonSürüm(QThread):
    def __init__(self):
        super().__init__()
    
    komut = pyqtSignal(str)
    def run(self):
        adresKod = urllib.request.urlopen("https://www.mozilla.org/en-US/firefox/all/").read()
        
        duzenli_ifade ='data-latest-firefox="(.*?)"'
        self.firefoxSonSürüm = re.findall(duzenli_ifade, adresKod.decode())[0]
        self.komut.emit(self.firefoxSonSürüm)
"""
class pencereBir(QThread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        super().__init__()
        
        self.pencere1 = QWidget()
        self.pencere1.resize(300, 300)
        self.pencere1.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        self.pencere1.setWindowTitle("Firefox Güncelleniyor")
        etk1 = QLabel("<img src='güncelle.png' />Güncelleme dosyası indiriliyor...", self.pencere1)
        self.pencere1.show()

class pencereİki(QThread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        super().__init__()
        
        self.pencere2 = QWidget()
        self.pencere2.resize(300, 300)      
        self.pencere2.setWindowIcon(QIcon(os.path.join("kaynaklar", "pencere_firefox_güncelle.png")))
        self.pencere2.setWindowTitle("Firefox Güncelleniyor")
        etk2 = QLabel("<img src='güncelle.png' />Güncelleme dosyası başarıyla indirildi !\nGüncelleme dosyası çalıştırılıyor...", self.pencere2)
        self.pencere2.show()            
""" 

class QEtiket(QLabel):
    def __init__(self, *args, **kwargs):
        super(QLabel, self).__init__(*args, **kwargs)
    
    sn = pyqtSignal(int)
    def mousePressEvent(self, QEvent):
        self.sn.emit(10)
        

def denetle(*args, **kwargs):
    pass

qInstallMessageHandler(denetle)             
uygulama = QApplication(sys.argv)
#QApplication.setStyle(QStyleFactory.create("cleanlooks"))
#uygulama.setStyle(QStyleFactory.create("plastique"))
pencere  = FirefoxGuncelleyici()
pencere.show()
uygulama.exec_()