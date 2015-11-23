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
    
        dag = date.today().strftime("%d.%m")
        
        if date.today().weekday() == 5:
            dag += ' , ' + (date.today() + timedelta(days=1)).strftime("%d.%m")
            dag += ' og ' + (date.today() + timedelta(days=2)).strftime("%d.%m")
        
        return dag
        
    def tomorrow(self):
        return (date.today() + timedelta(days=1)).strftime("%d.%m")
    
    def aftertomorrow(self):
        return (date.today() + timedelta(days=2)).strftime("%d.%m")
        
    def has_birthday(self, dato=None):

        daymonth = [date.today().strftime("%d.%m")]
        
        if date.today().weekday == 5:
            daymont.append(tomorrow())
            daymont.append(aftertomorrow())

        if 'dato' in self.request:
            daymonth = [self.request.get('dato')]
                    
        # Read the CSV file
        f = StringIO.StringIO((self.context.bursdag))
        file = f.read()
        csv_reader = csv.reader(file.splitlines(), encoding='latin-1', delimiter=';' )
        bursdager = []
        
        for i in csv_reader: 
            if i[4][0:5] in daymonth:
                bursdager.append(i)
                
        
        
        return bursdager

