# -*- coding: utf-8 -*-
import collective.setuphandlertools as sht
import logging
from Products.CMFCore.utils import getToolByName
from random import randint
from DateTime import DateTime
from plone.app.textfield.value import RichTextValue

def create_g24_posting(texts, cats,  maxchilds):
    content = []
    for i in range(2,randint(3, 12)):
        content.append(texts[randint(0, len(texts)-1)])

    d = {'type': 'g24.elements.basetype',
                 'title': texts[randint(0, len(texts)-1)],
                 'data': {'description': "",
                          'text': RichTextValue(raw = '\n'.join(content)),
                          'Subject': (cats[randint(0, len(cats)-1)], cats[randint(0, len(cats)-1)]),
                          #'Creator': myuser,
                }}

    myChilds = randint(0,maxchilds)
    d['childs'] = []
    for i in range(0,myChilds):
        d['childs'].append(create_g24_posting(texts, cats, maxchilds - myChilds))

    return d

logger = logging.getLogger("g24.importer")

cat = (
    'event',
    'film',
    'theater',
    'artikel',
    'neue medien',
    'info',
    'blabla'
)

def setup_html_transform(context):
    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return
    sht.unsafe_html_transform(logger)

def setup_content(context):

    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return

    site = context.getSite()

    # delete some default folders AND the stream folder
    sht.delete_items(site, ('news', 'events', 'stream'), logger)

    # setup admin + some test users
    sht.add_group(site, 'Members', roles=['Members'], logger=logger)
    
    sht.add_user(site, 'thet', 'thet',
                 email='johannes@raggam.co.at', fullname="Johannes Raggam",
                 groups=['Administrators'], logger=logger)

    sht.add_user(site, 'testuser', 'testuser',
                 email='test@localhost', fullname="Testuser",
                 groups=['Members'], logger=logger)

    sht.add_user(site, 'testuser2', 'testuser2',
                 email='test2@localhost', fullname="Testuser2",
                 groups=['Members'], logger=logger)

    sht.add_user(site, 'testuser3', 'testuser3',
                 email='test3@localhost', fullname="Testuser3",
                 groups=['Members'], logger=logger)

    # setup the folder for "postings"/bastypes
    streamfolder =  {'type': 'Folder',
         'id': 'stream',
         'title': u'Stream',
         'opts': {
                  'setDefault': True,
                  'setImmediatelyAddableTypes': ['g24.elements.basetype'],
                  },
        }

    # textparts to generate postings
    textparts  = [u'g24 10 Jahresfeier im Forum Stadtpark.',
                    u'Musik Videos aus den 80er-Jahren',
                    u'BürgerInneninitiative für eine Abschaffung der EU-Richtlinie zur Vorratsdatenspeicherung 2006/24/EG',
                u'Den – wortwörtlich – schwerpunkt bilden jetzt bassig-wummernde drones',
                u'Zumindest immer wieder, schöne, aber eisige harmonien. ',
                u'Seit kurzem ist die Festival-Website online und freudig kündigen wir die ersten Filme an',
                u'FM4, Biorama, The Gap, Junge Welt, oekonews.at, ZiGe.TV, Radio Helsinki, g24.at',
                u'Yeni Hayat, Analyse&Kritik, Lebensart, Luxemburg, iz3w ',
                u'Green Economy (Was wird im Rahmen der UNO diskutiert? Welche Chancen und Gefahren sind damit verbunden?',
                u'Mit einem spannenden, aktuellen Filmprogramm sowie zahlreichen Vorträgen, Workshops und Podiumsdiskussionen',
                u'Über direkte Demokratie im Nationalrat, Parteiprogramme, Liquid Democrazy, ... ',
                u'This module implements pseudo-random number generators for various distributions.',
                ]

    # add "postings"
    streamfolder['childs'] = []

    #pm = getToolByName(context, 'portal_membership')
    #myuser = pm.getMemberById('testuser3')

    # create 25 randomized posting-threads
    for i in range(0,25) :
        streamfolder['childs'].append(create_g24_posting(textparts, cat, 4))

    content_structure = [streamfolder]
    sht.create_item_runner(site, content_structure, lang='de', logger=logger)
