# -*- coding: utf-8 -*-
import logging
import MySQLdb

from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import _createObjectByType
from Products.Archetypes.event import ObjectInitializedEvent
from zope import event
import collective.setuphandlertools as sht

logger = logging.getLogger("g24.importer from postnuke")

class ImportPhpBB(object):

    def __init__(self, context):

        self.conn = None
        self.context = context
        self.pt = getToolByName(context, 'portal_transforms')

        #wft = getToolByName(site, 'portal_workflow')
        #wft.doActionFor(site['forum'], 'publish')

    def import_mysql_connect(self):
        try:
            self.conn = MySQLdb.connect (
                    host = "localhost",
                    user = "g24_726",
                    passwd = "g24_726",
                    db = "g24_726",
                    use_unicode = True,
                    charset = 'latin1') # <-- SET the character set!
            self.conn.set_character_set('latin1')

        except MySQLdb.Error, e:
            raise RuntimeError, "Error %d: %s" % (e.args[0], e.args[1])

    def import_nuke_phpbb_users(self):
        cursor = self.conn.cursor()

        cursor.execute("""SELECT username, user_email, user_avatar,
        user_website, user_from, user_sig, user_regdate FROM nuke_phpbb_users n
        ORDER BY user_id LIMIT 0,550;""")

        pm = getToolByName(self.context, 'portal_membership')
        context = self.context
        cnt = 0
        while True:
            row = cursor.fetchone()
            if row == None: break
            if row[0].lower() == 'anonymous': continue
            try:
               sht.add_user(
                   context=context,
                   username=row[0],
                   password=row[0],
                   groups=[],
                   email=row[1],
                   fullname="",
                   data={'portrait': sht.load_file(globals(),
                         'setupdata/avatar/%s' % row[2]),
                         'home_page': row[3],
                         'location': row[4],
                         'description': row[5],
                         },
                   logger=logger)
            except ValueError:
                logger.error("Invalid Username: %s, %s" % (row[0], row[1]))

            except:
                logger.error("Invalid Format: %s, %s" % (row[0], row[1]))

            cnt = cnt + 1; print cnt

        cursor.close()

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


    def import_finish(self):
        self.conn.close()


def start_import(context):
    if sht.isNotThisProfile(context, 'g24.importer.postnuke_import.txt'):
        return

    site = context.getSite()
    imp = ImportPhpBB(site)
    imp.import_mysql_connect()
    imp.import_nuke_phpbb_users()

    #imp.import_nuke_phpbb_categories()
    #imp.import_nuke_phpbb_forums()
    #imp.import_nuke_phpbb_topics()
    #imp.import_nuke_phpbb_posts()

    imp.import_finish()
