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

<MeasureFeedingTime>
	start: btn
    comment: Kom.text	

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
				text: root.startTimeLabel
				id: anf
			Label:
				text: "Ende: "
			Label:
				text: root.endTimeLabel
		Label:
			text: root.durationLabel
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
				    root.manager.current = "times"
				    root.manager.transition.direction = "right"
		    Button:
			    text: "Protokoll anzeigen"
			    size_hint: (1.,0.3)
			    on_press:
				    root.manager.current = "show"
				    root.manager.transition.direction = "left"
				    root.readProtocol()
<Protocol>
    on_enter:
        root.start()
	GridLayout:
		cols: 1
        Button:
            text: "ältere Einträge"
            on_press:
                root.getOlderEntries()
        Label:
            text: root.label1
        Label:
            text: root.label2
        Label:
            text: root.label3
        Label:
            text: root.label4
        Label:
            text: root.label5
        Label:
            text: root.label6
        Label:
            text: root.label7
        Label:
            text: root.label8
        Label:
            text: root.label9
        Label:
            text: root.label10
        Button:
            text: "neuere Einträge"
            on_press:
                root.getNewerEntries()
	    Button:
	        text: "Zurück"
	        on_press:
    	    	root.manager.current = "measure"
    	    	root.manager.transition.direction = "right"
<FeedingTimes>
    on_enter: root.read()
    GridLayout:
        cols: 1
        Label:
            text: root.labelTimeSince
        Label:
            text: root.labelTime
        Button:
            text: "Zurück"
            size_hint: (1.,0.2)
            on_press:
                root.manager.current = "measure"
                root.manager.transition.direction = "left"
""")

class MeasureFeedingTime(Screen):
    start = ObjectProperty()
    startTimeLabel = StringProperty()
    endTimeLabel = StringProperty()
    durationLabel = StringProperty()
    comment = StringProperty()

    measure = False
    time1 = time.time()
    time2 = time.time()
    timeStamp = DateTime.now()

    def zeiterfassen(self):
        self.timeStamp = DateTime.now()

        if self.measure == False:
            self.time1 = time.time()
            self.measure = True
            self.beginMeasurement()
        elif self.measure == True:
            self.time2 = time.time()
            self.measure = False
            duratin = self.time2 - self.time1
            durationInMinutes = int(duratin / 60)
            self.durationLabel = "Stillzeit: "+str(durationInMinutes)+" Minuten"
            self.endMeasurement()

    def saveLastFeedingTime(self):
        with open('lastFeeding.txt', 'w') as f:
            f.write(str(self.time2)+"\n"+str(self.timeStamp.strftime("%H:%M")))

    def beginMeasurement(self):
        self.startTimeLabel= self.timeStamp.strftime("%H:%M")
        self.endTimeLabel = ""
        with open ('Protokoll.txt', 'a') as protocol:
            protocol.write("\n"+str(self.timeStamp.strftime("%D: %H:%M")))
        self.saveLastFeedingTime()

    def endMeasurement(self):
        self.endTimeLabel = self.timeStamp.strftime("%H:%M")
        duration = self.time2 - self.time1
        durationInMinutes = int(duration / 60)
        with open('Protokoll.txt', 'a') as protocol:
            protocol.write(str(self.timeStamp.strftime(" bis %H:%M")) + "\n")
            protocol.write(str(durationInMinutes) + " Minuten\n")
            if self.comment != "":
                protocol.write(self.comment + "\n")
                self.comment= ""
        self.saveLastFeedingTime()

    def readProtocol(self):
        return Protocol().readProtocol()

class Protocol(Screen, GridLayout): 
        
    label1 = StringProperty()
    label2 = StringProperty()
    label3 = StringProperty()
    label4 = StringProperty()
    label5 = StringProperty()
    label6 = StringProperty()
    label7 = StringProperty()
    label8 = StringProperty()
    label9 = StringProperty()
    label10 = StringProperty()
    
    limit = 0
    etries = []
    offset = 0

    def start(self):
        self.limit = self.readProtocol()
        self.offset = self.limit
        self.updateLabel()

    def readProtocol(self):
        lines = 0
        self.entries = []

        try:
            with open('Protokoll.txt', 'r', encoding="utf-8") as protocol:
                for entry in protocol:
                    lines = lines + 1
                    self.entries.append(entry)
        except FileNotFoundError:
            entry = "Es ist noch kein Protokoll vorhanden"
            self.entries.append(entry)

        i = 11 - lines
        while i > 0:
            self.entries.append("")
            i = i-1

        if lines < 10:
            lines = 10

        return lines

    def getOlderEntries(self):
        self.offset = self.offset - 9
        if self.offset < 10:
            self.offset = 10
        self.updateLabel()

    def getNewerEntries(self):
        if self.offset + 9 < self.limit:
            self.offset = self.offset + 9
        else:
            self.offset = self.limit
        self.updateLabel()

    def updateLabel(self):
        self.label1 = self.entries[self.offset - 10]
        self.label2 = self.entries[self.offset - 9]
        self.label3 = self.entries[self.offset - 8]
        self.label4 = self.entries[self.offset - 7]
        self.label5 = self.entries[self.offset - 6]
        self.label6 = self.entries[self.offset - 5]
        self.label7 = self.entries[self.offset - 4]
        self.label8 = self.entries[self.offset - 3]
        self.label9 = self.entries[self.offset - 2]
        self.label10 = self.entries[self.offset - 1]

class FeedingTimes(Screen):
    labelTimeSince = StringProperty()
    labelTime = StringProperty()

    def read(self):
        try:
            with open('lastFeeding.txt', 'r') as f:
                times = f.readlines()
        except FileNotFoundError:
            times = ["0", "0"]
        showTime = times[1]
        timeOfFeeding = float(times[0])
        currentTime = time.time()
        secondsSince = currentTime - timeOfFeeding
        hoursSince = int(secondsSince / 3600)
        minutesSince = int(secondsSince / 60)
        minutesSince = minutesSince - hoursSince * 60
        self.labelTimeSince = "Zuletzt gestillt vor " + str(hoursSince) + ":" + "{:02}".format(minutesSince) + " Stunden"
        self.labelTime = "Um " + showTime + " Uhr"

SM = ScreenManager()
SM.add_widget(MeasureFeedingTime(name='measure'))
SM.add_widget(Protocol(name='show'))
SM.add_widget(FeedingTimes(name='times'))

class Stillzeit(App):
    def build(self):
        return SM

if __name__ == '__main__':
    Stillzeit().run()
