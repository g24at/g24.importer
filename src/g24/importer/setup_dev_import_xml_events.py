# -*- coding: utf-8 -*-
from DateTime import DateTime
from g24.elements.sharingbox.crud import create, add, edit
from g24.elements.sharingbox.form import FEATURES, G24_BASETYPE
from plone.event.utils import pydt
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.uuid.interfaces import IUUID
from xml.dom.minidom import parse
import json
import logging
import requests
import transaction


logger = logging.getLogger("g24.importer events from xml")

LOC_TO_UUID = {}


def get_geocode(*address):
    # http://stackoverflow.com/questions/3652951/google-maps-api-get-coordinat
    # es-of-address
    # http://maps.google.com/maps/api/geocode/json?address=1600+Amphitheatre+
    # Parkway,+Mountain+View,+CA&sensor=false

    # TODO: change country name with real one
    #

    address = [it for it in address if it]
    address_str = ','.join(address).replace(' ', '+')
    url = 'http://maps.google.com/maps/api/geocode/json'\
          '?address=Austria,%s&sensor=false' % address_str
    req = requests.get(url)
    lat = 0
    lng = 0
    if (req.ok):
        res = json.loads(req.text or req.content)
        try:
            lat = res['results'][0]['geometry']['location']['lat']
            lng = res['results'][0]['geometry']['location']['lng']
        except:  # KeyError, IndexError
            logger.warn('no geolocation for: %s' % address)
    return lat, lng


def import_places(container):

    importpath = "src/g24.importer/src/g24/importer/scripts/export-places.json"
    locations = json.loads(open(importpath).read())

    batch = 0
    for key, loc in locations.items():
        batch += 1
        # create data
        data = {'is_place': True}

        title = 'event_location' in loc and loc['event_location'] or None
        str1 = 'event_street1' in loc and loc['event_street1'] or None
        str2 = 'event_street2' in loc and loc['event_street2'] or None
        street = '%s%s%s' % (str1 and str1 or '',
                             str1 and str2 and ' ' or '',
                             str2 and str2 or '')
        zipc = 'event_postal' in loc and loc['event_postal'] or None
        city = 'event_city' in loc and loc['event_city'] or None

        lat, lng = get_geocode(zipc, city, title, str1, str2)
        if title:
            data['title'] = title
        if street:
            data['street'] = street
        if zipc:
            data['zip_code'] = zipc
        if city:
            data['city'] = city
        data['country'] = '040'
        if lat and lng:
            data['geolocation'] = Geolocation(lat, lng)

        obj = create(container, G24_BASETYPE)
        edit(obj, data, order=FEATURES)
        obj = add(obj, container)
        uuid = IUUID(obj)
        LOC_TO_UUID[key] = uuid
        logger.info('created place %s, uuid: %s, lat: %s, lng: %s' % (
            title, uuid, lat, lng
        ))

        if batch % 10 == 0:
            transaction.get().commit()


class ImportEvents(object):

    def __init__(self, context):
        self.context = context
        importpath =\
            "src/g24.importer/src/g24/importer/scripts/export-events.xml"
        self.content_dom = False
        self.content_dom = parse(importpath)

    def import_content(self):
        if not self.content_dom:
            logger.error("no xml import found")
            return

        ok = 0
        fail = 0
        for idx, ev in\
                enumerate(self.content_dom.getElementsByTagName('event')):
            #if idx>50: break
            try:
                obj = self.create_g24_event(self.context, ev)
                ok += 1
                logger.info('created event #%s with id: %s' % (obj.id, idx))
            except Exception as err:
                logger.error(
                    'Failed to import event ( id '
                    + ev.getAttribute('pc_eid') + ')... ' + repr(err)
                )
                fail += 1

            if idx % 10 == 0:
                transaction.get().commit()

        logger.info('Import done, ok: ' + str(ok) + ', failed : ' + str(fail))

    def create_g24_event(self, container, node):
        title = node.getAttribute('pc_title')
        text = node.getElementsByTagName('text')[0].childNodes[1].data
        tags = []
        for t in node.getElementsByTagName('tag'):
            tags.append(t.getAttribute('name'))

        loc = node.getAttribute('location_name')
        data = {
            'is_event': True,
            'title': title,
            'text': text,
            'subjects': tags,
            'timezone': 'Europe/Vienna',
            'whole_day': node.getAttribute('pc_alldayevent') == "1",
            'open_end': False,
            'recurrence': None,
            'location': LOC_TO_UUID.get(loc),
        }

        createdate = DateTime(node.getAttribute('pc_time'))
        event_date = DateTime(
            node.getAttribute('pc_eventDate') + " " +
            node.getAttribute('pc_startTime') + " Europe/Vienna"
        )
        data['start'] = pydt(event_date)

        # calc / use end date , fallback is same as start
        data['end'] = pydt(event_date)
        if node.hasAttribute('pc_endDate'):
            end_date = DateTime(
                node.getAttribute('pc_endDate') + " " +
                node.getAttribute('pc_endTime') + " Europe/Vienna"
            )
            data['end'] = pydt(end_date)
        elif node.getAttribute('pc_duration'):
            end_date = DateTime(
                int(event_date) +
                int(node.getAttribute('pc_duration'))
            )
            data['end'] = pydt(end_date)

        obj = create(container, G24_BASETYPE)
        # set the creators by loginname. if more than one,
        # seperate by whitespace
        obj.setCreators(node.getAttribute('pc_informant'))
        obj.creation_date = createdate
        edit(obj, data, order=FEATURES)
        obj = add(obj, container)

        return obj

    def import_finish(self):
        pass


def start_import(context):
    if context.readDataFile('g24.importer.xml_events_import.txt') is None:
        return

    site = context.getSite()

    # import locations first
    import_places(site.places)

    # start import into posts folder
    imp = ImportEvents(site.posts)
    imp.import_content()
    #imp.import_finish()
