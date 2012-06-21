# -*- coding: utf-8 -*-
import logging
import transaction
from DateTime import DateTime
from xml.dom.minidom import parse
from g24.elements.sharingbox.form import FEATURES, IGNORES, G24_BASETYPE
from g24.elements.sharingbox.form import create, add, edit

logger = logging.getLogger("g24.importer - from xml")

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

        for idx, th in\
                enumerate(self.content_dom.getElementsByTagName('thread')):
            #if idx>50: break
            try:
                logger.info("import thread")

                postings = th.getElementsByTagName('post')

                if (len(postings)<1):
                    logger.warning("thread without postings")
                    continue

                mainpost = self.create_g24_posting(self.context, self.map_xml_to_post(postings[0]))

                for p in postings[1:len(postings)]:
                    obj = self.create_g24_posting(mainpost,
                                                  self.map_xml_to_post(p))
                    logger.info('Created object #%s with id: %s'\
                                % (obj.id, idx))
            except Exception as err:
                logger.error('Failed to import thread ... %s ' % err)
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
            'is_thread': postingdata['title'].strip() != "", # TODO: is_thread only for threads
            'title': postingdata['title'],
            'text': postingdata['text'],
            'subjects': postingdata['tags'],
        }

        obj = create(container, G24_BASETYPE)
        obj.setCreators(postingdata['username']) # set the creators by loginname. if more than one, seperate by whitespace
        obj.creation_date = DateTime(postingdata['post_time'])
        edit(obj, data, order=FEATURES, ignores=IGNORES)
        obj = add(obj, container)

        transaction.commit()

        return obj

    def import_finish(self):
        pass


def start_import(context):
    if context.readDataFile('g24.importer.xml_import.txt') is None: return

    site = context.getSite()

    postsfolder = site['posts']

    # start import into posts folder
    imp = ImportPhpBBPostings(postsfolder)
    imp.import_content()
    imp.import_finish()
