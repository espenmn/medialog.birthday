## -*- coding: utf-8 -*-

from zope.interface import implements, Interface
from Products.Five import BrowserView
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields
from datetime import date,  timedelta
import StringIO
import unicodecsv as csv

class IBirthday(Interface):
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
        
    def friday(self):
        #warning weekday is different on different setup 
        # here , friday is 5
        return date.today().weekday() == 2 
        
    def weekend(self):
        return (self.tomorrow() + ' & ' + self.aftertomorrow())
        return days
        
    def tomorrow(self):
        return (date.today() + timedelta(days=1)).strftime("%d.%m")
    
    def aftertomorrow(self):
        return (date.today() + timedelta(days=2)).strftime("%d.%m")
        
        
    def has_birthday(self, dato=None):

        daymonth = self.date()
        
                    
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

