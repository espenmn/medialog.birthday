## -*- coding: utf-8 -*-

from zope.interface import implements, Interface
from Products.Five import BrowserView
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields
from datetime import date,  timedelta, datetime
import StringIO
import unicodecsv as csv


from types import StringTypes

from AccessControl import getSecurityManager
from dm.zopepatches.security.proxy import setup_proxy_roles
from dm.zopepatches.security.proxy import cleanup_proxy_roles


class IBirthday(Interface):
    """
    view interface """



class ITeachers(Interface):
    """
    view interface
        """

class Birthday(BrowserView):
    """
    browser view
    """
    
    def date(self, dato=None):
        if 'dato' in self.request:
            return self.request.get('dato')
    
        return date.today().strftime("%d.%m")

    def dayofweek(self):
        return date.today().weekday()
        
        
    def friday(self):
        #warning weekday is different on different setup 
        # here , friday is 4
        return date.today().weekday() == 4 
        
    def weekend(self):
        return (self.tomorrow() + ' & ' + self.aftertomorrow())
        return days
        
    def tomorrow(self):
        return (date.today() + timedelta(days=1)).strftime("%d.%m")
    
    def aftertomorrow(self):
        return (date.today() + timedelta(days=2)).strftime("%d.%m")
        
        
    def between(self, startdate, enddate, mydate):
        st = datetime.strptime(startdate, "%d.%m")
        en = datetime.strptime(enddate, "%d.%m")
        mydate = datetime.strptime(mydate, "%d.%m")

        return ( st < mydate < en )
        
    def birthday_between(self, start=None, end=None):
    
        context = setup_proxy_roles(('Manager'))
        
        try:

            f = StringIO.StringIO((self.context.bursdag))
            file = f.read()
            csv_reader = csv.reader(file.splitlines(), encoding='latin-1', delimiter=';' )
            bursdager = []
            start= '01.01'
            end = '12.12'
        
            if 'start' in self.request:
                start = self.request.get('start')
            
            if 'end' in self.request:
                end = self.request.get('end')
            
            st = datetime.strptime(start, "%d.%m")
            en = datetime.strptime(end, "%d.%m")
                    
            for i in csv_reader: 
                bdate = (i[4][0:5])
                mydate = datetime.strptime(bdate, "%d.%m")

                if st <= mydate  <= en:
                    bursdager.append(i)
        
            return bursdager
        
        finally:
            cleanup_proxy_roles(context)

                

    def has_birthday(self, dato=None):

        daymonth = self.date()
        
        context = setup_proxy_roles(('Manager'))
        
        try:
            # Read the CSV file
            f = StringIO.StringIO((self.context.bursdag))
            file = f.read()
            csv_reader = csv.reader(file.splitlines(), encoding='latin-1', delimiter=';' )
            bursdager = []
            saturday = []
            sunday = []
        
            if 'dato' in self.request:
                daymonth = self.request.get('dato')
            
                for i in csv_reader: 
                    if i[4][0:5] == daymonth:
                        bursdager.append(i)
        
                return bursdager, saturday, sunday
                
        
            for i in csv_reader: 
                if i[4][0:5] == daymonth:
                    bursdager.append(i)
        
                if self.friday():
                    if i[4][0:5] == self.tomorrow():
                        saturday.append(i)
                    if i[4][0:5] == self.aftertomorrow():
                        sunday.append(i)

        
            return bursdager, saturday, sunday
        
        finally:
            cleanup_proxy_roles(context)
            
            
class Teachers(BrowserView):
    """
    browser view
    """
    
    def teachers(self):
        context = setup_proxy_roles(('Manager'))
        
        ansattelist = []
        
        try:

            f = StringIO.StringIO((self.context.ansatte))
            file = f.read()
            csv_reader = csv.reader(file.splitlines(), delimiter=';' )
            
            for i in csv_reader: 
                if not "ornavn" in i[1]:
                    ansattelist.append(i)
        
            return ansattelist
        
        finally:
            cleanup_proxy_roles(context)


