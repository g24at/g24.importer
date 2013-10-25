# -*- coding: utf-8 -*-
import logging
import collective.setuphandlertools as sht
from g24.elements.sharingbox.form import create, add

logger = logging.getLogger("g24.importer - setup content")


def setup_html_transform(context):
    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return
    sht.unsafe_html_transform(logger)


def setup_content(context):

    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return

    site = context.getSite()

    # delete some default folders AND posts folder
    sht.delete_items(site, ('front-page', 'news', 'events', 'Members'), logger)

    site.setLayout('stream')

    _type = 'g24.elements.basetypecontainer'

    posts = create(site, _type)
    posts.id = 'posts'
    posts = add(posts, site)
    posts.setLayout('stream')
    posts.title = u'Posts'

    events = create(site, _type)
    events.id = 'events'
    events = add(events, site)
    events.setLayout('event_listing')
    events.title = u'Events'

    places = create(site, _type)
    places.id = 'places'
    places = add(places, site)
    places.setLayout('stream')
    places.title = u'Places'

#    content_structure = [
#
#        {'type': 'Folder',
#         'id': 'about',
#         'title': u'Info',
#         },
#        {'type': 'Folder',
#         'id': 'about-beta',
#         'title': u'Info Beta Test',
#         },
#
#    ]
#    sht.create_item_runner(site, content_structure, lang='de', logger=logger)
    #site.setLayout('traverse_view')
