# -*- coding: utf-8 -*-
import logging

import time
from xml.dom.minidom import parse

from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import _createObjectByType
from Products.Archetypes.event import ObjectInitializedEvent
from zope import event
import collective.setuphandlertools as sht

from DateTime import DateTime

from g24.elements.sharingbox.form import create, add, edit
from g24.elements.sharingbox.form import FEATURES, IGNORES, G24_BASETYPE

logger = logging.getLogger("g24.importer from xml")

class ImportEvents(object):

    def __init__(self, context):
        self.context = context
        
        importpath = "src/g24.importer/src/g24/importer/scripts/export-events.xml"

        self.content_dom = False        
        try:
            self.content_dom = parse(importpath)
        except Exception as err:
            logger.error("could not open " + importpath + ", maybe you have to run scripts/export-events.py to create it")


    def import_content(self):
        if not self.content_dom:
            logger.error("no xml import found")
            return
        
        for ev in self.content_dom.getElementsByTagName('event'):
            self.create_g24_event(self.context, ev)
            
            """
            try:
                logger.info("import event...")
                self.create_g24_posting(self.context, ev)
                
            except Exception as err:
                logger.error('Failed to import posting ... ')
            """
    
    def create_g24_event(self, container, node):

        data = {}
        
        title = node.getAttribute('pc_title')
        text  = node.getElementsByTagName('text')[0].childNodes[1].data
        
        tags = []
        for t in node.getElementsByTagName('tag'):
            tags.append(t.getAttribute('name'))
        
        # data['username']    = node.getAttribute('username')
        # data['tstamp']      = node.getAttribute('post_time')
        
        from yafowil.base import UNSET
        data = {
            'is_title': str(title).strip() != "",
            'is_event': True,
            'title': title,
            'text': text,
            'subjects': tags,
            'timezone':'Europe/Vienna',
            'whole_day': node.getAttribute('pc_alldayevent') == "1",
            'recurrence':  UNSET,
            'location': node.getAttribute('pc_time'),
        }

        from plone.event.utils import pydt
        createdate      = DateTime(node.getAttribute('pc_time'))
        event_date      = DateTime(node.getAttribute('pc_eventDate') + " " + node.getAttribute('pc_startTime') + " CET")
        # import pdb; pdb.set_trace()
        data['start']   = pydt(event_date)
        
        # todo calc / use end date -- use "duration" if set
        data['end']     = pydt(event_date)
        if node.getAttribute('pc_endDate') != "None":
            end_date      = DateTime(node.getAttribute('pc_endDate') + " " + node.getAttribute('pc_endTime') + " CET")
            data['end']     = pydt(end_date)
         
        
        obj = create(container, G24_BASETYPE)
        obj = add(obj, container)
        
        obj.setCreators(node.getAttribute('pc_informant')) # set the creators by loginname. if more than one, seperate by whitespace
        
        obj.creation_date = createdate

        edit(obj, data, order=FEATURES, ignores=IGNORES)
        logger.info('Created object with id: %s' % obj.id)
        return obj

    def import_finish(self):
        pass


def start_import(context):
    if sht.isNotThisProfile(context, 'g24.importer.xml_events_import.txt'):
        return

    site = context.getSite()
    
    # start import into stream folder
    imp = ImportEvents(site.stream)
    imp.import_content()
    imp.import_finish()
