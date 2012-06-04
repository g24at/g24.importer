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
        data['tstamp']      = node.getAttribute('post_time')
        
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
        
        # obj.creation_date = postingdata['tstamp']
        obj.creation_date = DateTime('2010/10/10 10:00 UTC')

        edit(obj, data, order=FEATURES, ignores=IGNORES)
        logger.info('Created object with id: %s' % obj.id)
        return obj
    
        
    """
    def import_nuke_phpbb_categories(self):
        cursor = self.conn.cursor()
        cursor.execute ("SELECT * FROM `nuke_phpbb_categories` ORDER BY cat_id")

        cat = []
        while(1):
            row = cursor.fetchone()
            if row == None:
                break
            ctxt = self.clean_text(row[1])
            # print("%s, %s" % (row[0], ctxt))
            cat.append(ctxt)
        self.pb.setCategories(cat)
        self.logger.info('ploneboard categories set: ' + str(cat))
        cursor.close()

    def import_nuke_phpbb_forums(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT c.cat_title, f.forum_name, f.forum_desc, f.forum_id \
                         FROM `nuke_phpbb_forums` AS f,\
                              `nuke_phpbb_categories` AS c\
                         WHERE f.cat_id = c.cat_id\
                         ORDER BY f.cat_id, f.forum_order")


        while(1):
            row = cursor.fetchone()
            if row == None:
                break
            if not str(row[3]) in self.pb.contentIds():
                cat= self.clean_text(row[0])
                title = self.clean_text(row[1])
                desc = self.clean_text(row[2])
                forum = self.pb.invokeFactory('PloneboardForum', row[3], title=title, description=desc, category=cat)

                self.logger.info(
                    'ploneboard forum created: title: %s, id:%s' %
                    (title, row[3]))
            else:
                self.logger.info(
                    'ploneboard forum EXISTS: id:%s' % row[3])

        cursor.close()


    def import_nuke_phpbb_topics(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT forum_id, topic_id, topic_title\
                         FROM `nuke_phpbb_topics`\
                         WHERE topic_id < 100\
                         ORDER BY forum_id, topic_id;")

        while(1):
            row = cursor.fetchone()
            if row == None:
                break
            forum = self.pb[str(row[0])]
            if not str(row[1]) in forum.contentIds():
                title = self.clean_text(row[2])
                topic = forum.invokeFactory('PloneboardConversation', row[1], title=title)

                self.logger.info(
                    'ploneboard conversation created: title: %s, id:%s' %
                    (title, row[1]))
            else:
                self.logger.info(
                    'ploneboard conversation EXISTS: id:%s' % row[1])

        cursor.close()


    def import_nuke_phpbb_posts(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT p.forum_id, p.topic_id, p.post_id, t.post_subject, t.post_text\
                         FROM nuke_phpbb_posts AS p,\
                         nuke_phpbb_posts_text AS t\
                         WHERE p.post_id = t.post_id\
                         AND p.topic_id < 100\
                         ORDER BY p.forum_id, p.topic_id, p.post_id;")

        while(1):
            try:
                row = cursor.fetchone()
                if row == None:
                    break

                forum = self.pb[str(row[0])]
                topic = forum[str(row[1])]
                if not str(row[2]) in topic.contentIds():
                    id = row[2]
                    title = self.clean_text(row[3])
                    text = self.clean_web(row[4])

                    #post = self.pb[str(row[0])][str(row[1])].addComment(title, text)
                    #post = self.pb[str(row[0])][str(row[1])].invokeFactory('PloneboardComment', row[2], title=title, text=text)

                    if not title:
                        title = topic.Title()

                    m = _createObjectByType('PloneboardComment', topic, id)
                    event.notify(ObjectInitializedEvent(m))

                    # XXX: There is some permission problem with AT write_permission
                    # and using **kwargs in the _createObjectByType statement.
                    m.setTitle(title)
                    m.setText(text)

                    ## TODO: set the creator of comment
                    #if creator is not None:
                    #    m.setCreators([creator])

                    # Create files in message: NOT SUPPORTET NOW

                    # If this comment is being added by anonymous, make sure that the true
                    # owner in zope is the owner of the forum, not the parent comment or
                    # conversation. Otherwise, that owner may be able to view or delete
                    # the comment.
                    membership = getToolByName(topic, 'portal_membership')
                    if membership.isAnonymousUser():
                        utils.changeOwnershipOf(m, forum.owner_info()['id'], False)

                    m.indexObject()
                    # TODO: bottleneck?
                    topic.reindexObject() # Sets modified

                    self.logger.info(
                        'ploneboard comment created: title: %s, id:%s, topic:%s, forum:%s,' %
                        (title, id, topic, forum))
                else:
                    self.logger.info(
                        'ploneboard comment EXISTS: id:%s' % id)
            except:
                import pdb; pdb.set_trace

        cursor.close()
    """

    """
    def clean_encoding(self, txt):
        return txt.encode('utf-8')

    def clean_text(self, txt):
        txt = self.clean_encoding(txt)
        txt = self.pt.convert('html_to_text', txt).getData()
        txt = txt.replace('&#38;', '&')
        txt = txt.replace('&amp;', '&')
        return txt

    def clean_web(self, txt):
        txt = self.clean_encoding(txt)
        txt = self.pt.convert('html_to_web_intelligent_plain_text', txt).getData()
        return txt
    """


    def import_finish(self):
        pass


def start_import(context):
    if sht.isNotThisProfile(context, 'g24.importer.xml_import.txt'):
        return

    site = context.getSite()
    
    # we expect site.stream to be already created
    imp = ImportPhpBBPostings(site.stream)
    imp.import_content()
    imp.import_finish()
