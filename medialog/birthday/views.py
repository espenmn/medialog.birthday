## -*- coding: utf-8 -*-


from zope.interface import implements, Interface
from Products.Five import BrowserView
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields

from datetime import date

import StringIO
import csv 


class IBirthday(Interface):
    """
    view interface
    """


class Birthday(BrowserView):
    """
    browser view
    """
    
    @property
    def date(self):
        return date.today().strftime("%d.%m.%Y")
    
    
    @property
    def has_birthday(self):

        daymonth = date.today().strftime("%d.%m")
        
        # Read the CSV file
        f = StringIO.StringIO((self.context.bursdag))
        file = f.read()
        csv_reader = csv.reader(file.splitlines(), delimiter=';' )
        
        bursdager = []
        
        for i in csv_reader: 
            if i[4].startswith(daymonth):
                #[x.encode('utf-8') for x in i]
                bursdager.append(i)
        
        return bursdager

