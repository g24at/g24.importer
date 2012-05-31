# -*- coding: utf-8 -*-
import collective.setuphandlertools as sht
import logging
from Products.CMFCore.utils import getToolByName
from random import randint
from DateTime import DateTime

from g24.elements.sharingbox.form import create, add, edit
from g24.elements.sharingbox.form import FEATURES, IGNORES, G24_BASETYPE

logger = logging.getLogger("g24.importer")

cat = (
    u'event',
    u'film',
    u'theater',
    u'artikel',
    u'neue medien',
    u'info',
    u'blabla'
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
    sht.delete_items(site, ('front-page', 'news', 'stream'), logger)

    # setup admin + some test users
    sht.add_group(site, 'Members', roles=['Members'], logger=logger)

    # groups=['Administrators']

    sht.add_user(site, 'thet', 'thet',
            email='tdot@g24.at', fullname="Johannes Raggam",
            groups=['Members'], logger=logger)


    sht.add_user(site, 'test1', 'test1',
            email='test1@localhost', fullname="Testuser1",
            groups=['Members'], logger=logger)

    sht.add_user(site, 'test2', 'test2',
            email='test2@localhost', fullname="Testuser2",
            groups=['Members'], logger=logger)

    sht.add_user(site, 'test3', 'test3',
            email='test3@localhost', fullname="Testuser3",
            groups=['Members'], logger=logger)


    # textparts to generate postings
    textparts  = [
            u'g24 10 Jahresfeier im Forum Stadtpark.',
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

    #pm = getToolByName(context, 'portal_membership')
    #myuser = pm.getMemberById('testuser3')


    def create_g24_posting(container, texts, cats, maxchilds):
        content = []
        for i in range(2, randint(3, 12)):
            content.append(texts[randint(0, len(texts)-1)])

        data = {
            'is_title': True,
            'title': texts[randint(0, len(texts)-1)],
            'text': u'\n'.join(content),
            'subjects': (cats[randint(0, len(cats)-1)], cats[randint(0, len(cats)-1)]),
            #'Creator': myuser,
        }

        obj = create(container, G24_BASETYPE)
        obj = add(obj, container)
        edit(obj, data, order=FEATURES, ignores=IGNORES)
        logger.info('Created object with id: %s' % obj.id)

        myChilds = randint(0, maxchilds)
        for i in range(0, myChilds):
            create_g24_posting(obj, texts, cats, maxchilds - myChilds)

        return obj


    # setup the folder for "postings"/bastypes
    data = dict(is_title=True, title=u'Stream')
    streamfolder = create(site, G24_BASETYPE)
    streamfolder.id = 'stream'
    streamfolder = add(streamfolder, site)
    edit(streamfolder, data, order=FEATURES, ignores=IGNORES)

    # create 25 randomized posting-threads
    for i in range(0, 25) :
        create_g24_posting(streamfolder, textparts, cat, 4)
