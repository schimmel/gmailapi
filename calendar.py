try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import atom
import time
import string
import sys

import getpass
import logging

class CalendarManage:
    def __init__(self,user,pwd):
        self.client = gdata.calendar.client.CalendarClient(source='CalendarManage Python Tool')
        self.auth = True
        try:
            self.client.ClientLogin(user, pwd,self.client.source)
        except:
            logging.error("Fehler beim Anmelden!")
            self.auth = False

    def PrintUserCalendars(self):
        logging.info("Funktionsaufruf PrintUserCalendars")
        feed = self.client.GetAllCalendarsFeed()
        print feed.title.text
        for i, a_calendar in enumerate(feed.entry): 
            print '\t%s, %s' % (i, a_calendar.title.text)

    def PrintOwnCalendars(self):
        logging.info("Funktionsaufruf PrintOwnCalendars")
        feed = self.client.GetOwnCalendarsFeed()
        print feed.title.text
        for i, a_calendar in enumerate(feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)

    def DeleteCalendar(self):
        logging.info("Funktionsaufruf DeleteCalendar")
        feed = self.client.GetOwnCalendarsFeed()
        self.PrintOwnCalendars()
        dele = raw_input("Welchen Kalender willstn loeschen (Nr.)?")
        for i, entry in enumerate(feed.entry):
            if str(i) == dele:
                print 'Deleting calendar: %s' % entry.title.text
                try:
                    self.client.Delete(entry.GetEditLink().href)
                except:
                    print "Den Primary Kalender kannst net loeschen!"
                    logging.error("Der Kalender %s konnte nicht geloescht werden!" % (entry.title.text))

    def CopyDefaultCalendar(self,delete):
        logging.info("Funktionsaufruf CopyDefaultCalendar")
        feed = self.client.GetOwnCalendarsFeed()
        new_name = raw_input("Wie soll der Name des Neuen Kalenders sa?  ")
        for i, entry in enumerate(feed.entry):
            if i == 0:
                print 'Primary Calendar: %s' % (entry.title.text)
                primcalendar = self.client.GetCalendarEntry(entry.GetEditLink().href)
        # Create new empty Calendar
        calendar = gdata.calendar.data.CalendarEntry()
        calendar.title = atom.data.Title(text=new_name)
        calendar.summary = atom.data.Summary(text='Copy of Primary Calendar')
        calendar.color = gdata.calendar.data.ColorProperty(value=primcalendar.color.value)
        calendar.timezone = gdata.calendar.data.TimeZoneProperty(value=primcalendar.timezone.value)
        calendar.hidden = gdata.calendar.data.HiddenProperty(value=primcalendar.hidden.value)

        new_calendar = self.client.InsertCalendar(new_calendar=calendar)
        logging.info("CopyDefaultCalendar leerer neuer Kalender erstellt")
        logging.info("Kalender-ID: %s" % (new_calendar.content.src))
        # Events in neuen Kalender kopieren
        feed = self.client.GetCalendarEventFeed()
        for i, an_event in enumerate(feed.entry):
            print '\t%s. %s' % (i, an_event.title.text,)
            event = self.client.GetEventEntry(an_event.GetEditLink().href)
            try:
                self.client.InsertEvent(event,(new_calendar.content.src))
            except:
                #print sys.exc_info()
                logging.error("Fehler beim anlegen von Event %s " % (event.title.text))
            print "Event: %s in neuen Kalender angeleget" % (event.title.text)
            if delete == "yes":
                #OrginalEvent loeschen
                try:
                    self.client.Delete(event)
                except:
                    logging.error("Fehler beim loeschen des Events %s" % (event.title.text))
                print "Event: %s in alten Kalender geloescht" % (event.title.text)

        print "\n!!!Alle Aktionen durchgefuehrt bitte calendar.log checken!!!\n"

class GUI:
    def __init__(self):
        self.select = "unselected"
    
    def show_auth(self):
        print '--------------------Bitte geben Sie ihre Zugangsdaten ein--------------------'
        self.user = raw_input('Benutzername (E-Mail): ')
        self.pwd = getpass.getpass('Passwort: ')

    def show_menue(self):
        print "\n"
        print "Bitte waehlen Sie eine Funktion:"
        print "1  Alle Kalender anzeigen"
        print "2  Eigene Kalender anzeigen"
        print "----------Bearbeitungsfunktionen----------"
        print "3  Eigene Kalender loeschen"
        print "4  Default Kalender in neuen kopieren"
        print "99 Beenden"
        return raw_input("Auswahl:")

    def show_delete(self):
        print "\nSolln a alla Events ausn default Kalender geloescht werden?"
        return raw_input("YES/NO: ").lower()
    
    def nl(self):
        print "\n"

class Logger:
    def __init__(self):
        logging.basicConfig(
            filename="calendar.log",
            level = logging.DEBUG,
            format = "%(asctime)s %(levelname)s: %(message)s", 
            datefmt = "%d.%m.%Y %H:%M:%S")
    

if __name__ =="__main__":
    # Initialize
    Logger()
    logging.info("Calendar.py wurde gestartet")
    auth = False
    cmdgui = GUI() 

    while auth == False:
        cmdgui.show_auth()
        gcal = CalendarManage(cmdgui.user,cmdgui.pwd)
        auth = gcal.auth
    
    while cmdgui.select != "99":
        cmdgui.select = cmdgui.show_menue()
        cmdgui.nl()
        if cmdgui.select == "1":
            gcal.PrintUserCalendars()
        elif cmdgui.select == "2":
            gcal.PrintOwnCalendars()
        elif cmdgui.select == "3":
            gcal.DeleteCalendar()
        elif cmdgui.select == "4":
            delete = cmdgui.show_delete()
            gcal.CopyDefaultCalendar(delete)
        elif cmdgui.select == "99":
            print "Gratualtion jetzt hosts geschaft!!"
        else:
            print "Keine gueltige Auswahl"

    logging.info("Calendar.py wurde beendet")
    logging.shutdown()

