#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import time
from datetime import datetime as DateTime

# Gui
Builder.load_string("""
<Startseite>
    GridLayout:
        cols: 1
        Button:
            text: "Neue Stillzeit erfassen"
	        on_press: 
                root.manager.current = "messen"
                root.manager.transition.direction = "right"

        GridLayout:
            cols:2
            Button:
                text: "Letztes Stillen"
            Button:
                text: "Protokoll anzeigen"

<Zeitmessen>
	start: btn
    kommentar: Kom.text	

	GridLayout:
		cols: 1
		size: root.width, root.height
		
		Button:
			text: "Zeitstempel erfassen"
			id: btn
			size_hint: (1.,0.3)
			on_press:
				root.zeiterfassen()
		GridLayout:
			cols: 4
			Label:
				text: "Beginn: "
			Label:
				text: root.anfang
				id: anf
			Label:
				text: "Ende: "
			Label:
				text: root.ende
		Label:
			text: root.stilldauer
			size_hint: (1.,0.3)
		GridLayout:
			cols: 2 
			Label:
				text: "Kommentar"            
			TextInput:
			    id: Kom
                text: ""
		    Button:
			    text: "letztes Stillen"
			    size_hint: (1.,0.3)
			    on_press:
				    root.manager.current = "zeiten"
				    root.manager.transition.direction = "right"
		    Button:
			    text: "Protokoll anzeigen"
			    size_hint: (1.,0.3)
			    on_press:
				    root.manager.current = "zeigen"
				    root.manager.transition.direction = "left"
				    root.lesen()
<Protokoll>
    on_enter:
        root.start()
	GridLayout:
		cols: 1
        Button:
            text: "ältere Einträge"
            on_press:
                root.Aelter()
        Label:
            text: root.anzeige1
        Label:
            text: root.anzeige2
        Label:
            text: root.anzeige3
        Label:
            text: root.anzeige4
        Label:
            text: root.anzeige5
        Label:
            text: root.anzeige6
        Label:
            text: root.anzeige7
        Label:
            text: root.anzeige8
        Label:
            text: root.anzeige9
        Label:
            text: root.anzeige10
        Button:
            text: "neuere Einträge"
            on_press:
                root.Neuer()
	    Button:
	        text: "Zurück"
	        on_press:
    	    	root.manager.current = "messen"
    	    	root.manager.transition.direction = "right"
<Zeiten>
    on_enter: root.lesen()
    GridLayout:
        cols: 1
        Label:
            text: root.anzeigediff
        Label:
            text: root.anzeigezeit
        Button:
            text: "Zurück"
            size_hint: (1.,0.2)
            on_press:
                root.manager.current = "messen"
                root.manager.transition.direction = "left"
""")

class Zeitmessen(Screen):
    start = ObjectProperty()
    anfang = StringProperty()
    ende = StringProperty()
    stilldauer = StringProperty()
    kommentar = StringProperty()

    messen = False
    zeit1 = time.time()
    zeit2 = time.time()
    zeitstempel = DateTime.now()

    def zeiterfassen(self):
        self.zeitstempel = DateTime.now()

        if self.messen == False:
            self.zeit1 = time.time()
            self.messen = True
            self.beginn()
        elif self.messen == True:
            self.zeit2 = time.time()
            self.messen = False
            dauer = self.zeit2 - self.zeit1
            dauermin = dauer  / 60
            dauermin = int(dauermin)
            dauersek = dauer - dauermin
            self.stilldauer = "Stillzeit: "+str(dauermin)+" Minuten"
            self.beendet()

    def ZuletztGestillt(self):
        with open('LetztesStillen.txt', 'w') as letztes_stillen:
            letztes_stillen.write(str(self.zeit2)+"\n"+str(self.zeitstempel.strftime("%H:%M")))

    def beginn(self):
        self.anfang = self.zeitstempel.strftime("%H:%M")
        self.ende = ""
        with open ('Protokoll.txt', 'a') as protokoll:
            protokoll.write("\n"+str(self.zeitstempel.strftime("%D: %H:%M")))
        self.ZuletztGestillt()

    def beendet(self):
        self.ende = self.zeitstempel.strftime("%H:%M")
        dauer = self.zeit2 - self.zeit1
        dauermin = dauer  / 60
        dauermin = int(dauermin)
        with open('Protokoll.txt', 'a') as protokoll:
            protokoll.write(str(self.zeitstempel.strftime(" bis %H:%M"))+"\n")
            protokoll.write(str(dauermin)+" Minuten\n")
        if self.kommentar != "":
            with open('Protokoll.txt', 'a') as protokoll:
                protokoll.write(self.kommentar+"\n")
            self.kommentar = ""
        self.ZuletztGestillt()

    def lesen(self):
        return Protokoll().lesen()

class Startseite(Screen, GridLayout):
    pass

class Protokoll(Screen, GridLayout): 
        
    anzeige1 = StringProperty()
    anzeige2 = StringProperty()
    anzeige3 = StringProperty()
    anzeige4 = StringProperty()
    anzeige5 = StringProperty()
    anzeige6 = StringProperty()
    anzeige7 = StringProperty()
    anzeige8 = StringProperty()
    anzeige9 = StringProperty()
    anzeige10 = StringProperty()
    limit = 0
    eintraege = []
    zeige = 0

    def start(self):

        self.zeige = self.lesen()
        self.Label()

    def lesen(self):
        i = 0
        a = 11
        self.eintraege = []

        try:
            with open('Protokoll.txt', 'r') as protokoll:
                for eintrag in protokoll:
                    i = i + 1
                    self.eintraege.append(eintrag)
        except FileNotFoundError:
            eintrag = "Es ist noch kein Protokoll vorhanden"
            self.eintraege.append(eintrag)

        self.limit = i

        a = a - i

        while a > 0:
            self.eintraege.append("")
            a = a-1

        if i < 10:
            i = 10

        return i

    def Aelter(self):
        self.lesen()
        self.zeige = self.zeige - 9
        if self.zeige < 10:
            self.zeige = 10
        self.Label()

    def Neuer(self):
        self.lesen()
        if self.zeige + 9 < self.limit:
            self.zeige = self.zeige + 9
        else:
            self.zeige = self.limit

        self.Label()

    def Label(self):
        self.anzeige1 = self.eintraege[self.zeige-10]
        self.anzeige2 = self.eintraege[self.zeige-9]
        self.anzeige3 = self.eintraege[self.zeige-8]
        self.anzeige4 = self.eintraege[self.zeige-7]
        self.anzeige5 = self.eintraege[self.zeige-6]
        self.anzeige6 = self.eintraege[self.zeige-5]
        self.anzeige7 = self.eintraege[self.zeige-4]
        self.anzeige8 = self.eintraege[self.zeige-3]
        self.anzeige9 = self.eintraege[self.zeige-2]
        self.anzeige10 = self.eintraege[self.zeige-1]

class Zeiten(Screen):

    anzeigediff = StringProperty()
    anzeigezeit = StringProperty()

    def lesen(self):
        try:
            with open('LetztesStillen.txt', 'r') as letztes_stillen:
                zeiten = letztes_stillen.readlines()
        except FileNotFoundError:
            zeiten = ["0", "Fehler, Datei nicht gefunden"]
        zeitanzeige = zeiten[1]
        zeit1 = float(zeiten[0])
        zeit2 = time.time()
        zeitseitStillen = zeit2 - zeit1
        zeitseitStillenh = int(zeitseitStillen / 3600)
        zeitseitStillenmin = int(zeitseitStillen / 60)
        zeitseitStillenmin = zeitseitStillenmin - zeitseitStillenh * 60
        self.anzeigediff = "Zuletzt gestillt vor "+str(zeitseitStillenh)+":"+"{:02}".format(zeitseitStillenmin)+" Stunden"
        self.anzeigezeit = "Um "+zeitanzeige+" Uhr"

SM = ScreenManager()
SM.add_widget(Zeitmessen(name='messen'))
SM.add_widget(Protokoll(name='zeigen'))
SM.add_widget(Zeiten(name='zeiten'))

class Stillzeit(App):
    def build(self):
        return SM

if __name__ == '__main__':
    Stillzeit().run()
