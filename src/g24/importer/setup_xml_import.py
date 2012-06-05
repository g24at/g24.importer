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

class ImportPhpBBPostings(object):

    def __init__(self, context):
        self.context = context
        
        importpath = "src/g24.importer/src/g24/importer/scripts/export-posts.xml"

        self.content_dom = False        
        try:
            self.content_dom = parse(importpath)
        except Exception as err:
            logger.error("could not open " + importpath + ", maybe you have to run scripts/export-posts.py to create it")

        """
        self.conn = None
        self.pt = getToolByName(context, 'portal_transforms')
        """
        
        #wft = getToolByName(site, 'portal_workflow')
        #wft.doActionFor(site['forum'], 'publish')


    def import_content(self):
        if not self.content_dom:
            logger.error("no xml import found")
            return
        
        for th in self.content_dom.getElementsByTagName('thread'):
            try:
                logger.info("import thread")
                
                postings = th.getElementsByTagName('post')
    
                if (len(postings)<1):
                    logger.warning("thread without postings")
                    continue
                
                mainpost = self.create_g24_posting(self.context, self.map_xml_to_post(postings[0]))
                
                for p in postings[1:len(postings)]:
                    self.create_g24_posting(mainpost, self.map_xml_to_post(p))
            except Exception as err:
                logger.error('Failed to import thread ... ')
                #logger.error(err.)
    
    def map_xml_to_post(self, node):
        data = {}
        
        data['title']   = node.getAttribute('post_subject')
        data['text']    = node.getElementsByTagName('text')[0].childNodes[1].data
        
        data['tags']    = []
        for t in node.getElementsByTagName('tag'):
            data['tags'].append(t.getAttribute('name'))
        
        data['username']    = node.getAttribute('username')
        #data['tstamp']      = node.getAttribute('post_time')
        data['post_time']      = node.getAttribute('post_time')
        
        return data
        
    def create_g24_posting(self, container, postingdata):
        data = {
            'is_title': True,
            'title': postingdata['title'],
            'text': postingdata['text'],
            'subjects': postingdata['tags'],
        }

        obj = create(container, G24_BASETYPE)
        obj = add(obj, container)
        obj.setCreators(postingdata['username']) # set the creators by loginname. if more than one, seperate by whitespace
        
        obj.creation_date = DateTime(postingdata['post_time'])

        edit(obj, data, order=FEATURES, ignores=IGNORES)
        logger.info('Created object with id: %s' % obj.id)
        return obj

    def import_finish(self):
        pass


def start_import(context):
    if sht.isNotThisProfile(context, 'g24.importer.xml_import.txt'):
        return

    site = context.getSite()

    # delete stream folder
    sht.delete_items(site, ('stream'), logger)
    data = dict(is_title=True, title=u'Stream')
    streamfolder = create(site, G24_BASETYPE)
    streamfolder.id = 'stream'
    streamfolder = add(streamfolder, site)
    edit(streamfolder, data, order=FEATURES, ignores=IGNORES)
    
    # start import into stream folder
    imp = ImportPhpBBPostings(site.stream)
    imp.import_content()
    imp.import_finish()
