# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from pnexport import cleanTextFromControlChars
from xml.dom.minidom import Document
import HTMLParser
import MySQLdb
import collections
import phpserialize
import re
import sys


IN_ENCODING = 'latin-1'
OUT_ENCODING = 'utf-8'

cfg = ConfigParser()
cfg.read('../config.ini')

conn = MySQLdb.connect(host=cfg.get('default', 'mysql.host'),
                       user=cfg.get('default', 'mysql.user'),
                       passwd=cfg.get('default', 'mysql.passwd'),
                       db=cfg.get('default', 'mysql.db'))

"""

mysql> describe nuke_postcalendar_events;
+----------------+-----------------------+------+-----+------------+----------------+
| Field          | Type                  | Null | Key | Default    | Extra          |
+----------------+-----------------------+------+-----+------------+----------------+
| pc_eid         | int(11) unsigned      | NO   | PRI | NULL       | auto_increment |
| pc_aid         | varchar(30)           | NO   |     |            |                |
| pc_title       | varchar(150)          | YES  |     | NULL       |                |
| pc_time        | datetime              | YES  |     | NULL       |                |
| pc_hometext    | text                  | YES  |     | NULL       |                |
| pc_comments    | int(11)               | YES  |     | 0          |                |
| pc_counter     | mediumint(8) unsigned | YES  |     | NULL       |                |
| pc_topic       | int(3)                | NO   |     | 1          |                |
| pc_informant   | varchar(20)           | NO   |     |            |                |
| pc_eventDate   | date                  | NO   |     | 0000-00-00 |                |
| pc_endDate     | date                  | NO   |     | 0000-00-00 |                |
| pc_recurrtype  | int(1)                | NO   |     | 0          |                |
| pc_recurrspec  | text                  | YES  |     | NULL       |                |
| pc_recurrfreq  | int(3)                | NO   |     | 0          |                |
| pc_startTime   | time                  | YES  |     | NULL       |                |
| pc_endTime     | time                  | YES  |     | NULL       |                |
| pc_alldayevent | int(1)                | NO   |     | 0          |                |
| pc_location    | text                  | YES  |     | NULL       |                |
| pc_conttel     | varchar(50)           | YES  |     | NULL       |                |
| pc_contname    | varchar(150)          | YES  |     | NULL       |                |
| pc_contemail   | varchar(255)          | YES  |     | NULL       |                |
| pc_website     | varchar(255)          | YES  |     | NULL       |                |
| pc_fee         | varchar(50)           | YES  |     | NULL       |                |
| pc_eventstatus | int(11)               | NO   |     | 0          |                |
| pc_catid       | int(11)               | NO   | MUL | 0          |                |
| pc_duration    | bigint(20)            | NO   |     | 0          |                |
| pc_sharing     | int(11)               | NO   |     | 0          |                |
| pc_language    | varchar(30)           | YES  |     |            |                |
+----------------+-----------------------+------+-----+------------+----------------+

"""


# from Products.CMFPlone.utils
def safe_unicode(value, encoding='utf-8'):
    """Converts a value to unicode, even it is already a unicode string.
    """
    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        try:
            value = unicode(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode('utf-8', 'replace')
    return value


def _cleanup_textonly(s):
    # http://stackoverflow.com/questions/730299/replace-html-entities-with-the-corresponding-utf-8-characters-in-python-2-6
    s = s.strip()
    pars = HTMLParser.HTMLParser()
    result = pars.unescape(s)
    #d = {
    #    '&quot;': '"',
    #    '&amp;': '&',
    #    '&lt;': '<',
    #    '&gt;': '>',
    #}
    ## http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements/2401481#2401481
    ## no whole words
    #pattern = re.compile('|'.join(d.keys()))
    ## whole words
    ##pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
    #result = pattern.sub(lambda x: d[x.group()], s)
    return safe_unicode(result)


dom = Document()
dom.appendChild(dom.createElement('export'))

# load categories lookup
sql_str = "select * from nuke_postcalendar_categories"
cursor = conn.cursor (MySQLdb.cursors.DictCursor)
cursor.execute (sql_str);
rows = cursor.fetchall()
categories = {}
for cat in rows:
    categories[str(cat['pc_catid'])] = cleanTextFromControlChars(str(cat['pc_catname']))

test_set = True
custom_limit = ""
if len (sys.argv) > 1:
    if sys.argv[1] == "all" : test_set = False
    else : test_set = False ; custom_limit = sys.argv[1]

# select topics for export
sql_str = "select * from nuke_postcalendar_events where pc_eventstatus = 1"
if      test_set            : sql_str = sql_str + " order by RAND() limit 0,200"
elif    custom_limit != ""  : sql_str = sql_str + " " + custom_limit

#sql_str = sql_str + " and pc_eid < 3000 and pc_eid > 2800"
#sql_str = sql_str + " and pc_eid = 47 "
#sql_str = sql_str + " and pc_eid in (" + ','.join([str(2544),str(2541)]) + ") "
#sql_str = sql_str + " order by RAND() limit 0,20"

eventcursor = conn.cursor (MySQLdb.cursors.DictCursor)
eventcursor.execute (sql_str);
eventrows = eventcursor.fetchall()

items_ok = 0
items_fail = 0

locations = {}


# search for this string : reference
loc_map = collections.OrderedDict([
    (u'92,6', 'radio_helsinki'),
    (u'92.6', 'radio_helsinki'),
    (u'97,9', 'radio_soundportal'),
    (u'97.9', 'radio_soundportal'),
    (u'afro', 'afro_asiatisches_institut'),
    (u'after dark', 'after_dark'),
    (u'ajz', 'ajz_insel'),
    (u'alte tech', 'alte_technik'),
    (u'arbeiterkammer', 'arbeiterkammer'),
    (u'arcadium', 'arcadium'),
    (u'audimax - fh', 'fh_joanneum'),
    (u'audimax fh', 'fh_joanneum'),
    (u'augartenkino', 'kiz'),
    (u'augarten ', 'augarten'),
    (u'augartenpark', 'augarten'),
    (u'augratenpark', 'augarten'),
    (u'aula der alten', 'kf_uni'),
    (u'aula der karl', 'kf_uni'),
    (u'aula der univ', 'kf_uni'),
    (u'aula, haupt', 'kf_uni'),
    (u'aznull', 'aznull'),
    (u'babenberger', 'babenbergerhof'),
    (u'backstage', 'backstage'),
    (u'badeschiff', 'badeschiff'),
    (u'bahnhof non-stop', 'non_stop'),
    (u'baodo', 'baodo_im_nil'),
    (u'bar projekt', 'barprojekt'),
    (u'barprojekt', 'barprojekt'),
    (u'bildungsverein', 'bildungsverein_kpoe'),
    (u'bildungszentrum', 'bildungsverein_kpoe'),
    (u'blue moon', 'blue_moon'),
    (u'bluemoon', 'blue_moon'),
    (u'borra ville', 'borraville'),
    (u'borraville', 'borraville'),
    (u'botanischer', 'botanischer_garten'),
    (u'brot & spiele', 'brot_spiele'),
    (u'bruecke', 'die_bruecke'),
    (u'brücke', 'die_bruecke'),
    (u'camera', 'camera_austria'),
    (u'celery', 'celerys'),
    (u'cider', 'cider_farm'),
    (u'clubq', 'club_q'),
    (u'cselley', 'cselley_muehle'),
    (u'cube', 'cube'),
    (u'cuntra', 'cuntra'),
    (u'das ton', 'das_ton'),
    (u'de-zentrale', 'dezentrale'),
    (u'dezentrale', 'dezentrale'),
    (u'different', 'diverse'),
    (u'div locations', 'diverse'),
    (u'diverse', 'diverse'),
    (u'doku graz', 'doku_graz'),
    (u'doku, graz', 'doku_graz'),
    (u'dom im berg', 'dom_im_berg'),
    (u'dom im schlossberg', 'dom_im_berg'),
    (u'domimberg', 'dom_im_berg'),
    (u'dreihackengasse 42', 'postgarage'),
    (u'drews', 'karl_drews_klub'),
    (u'ecs - labor', 'esc'),
    (u'esc ', 'esc'),
    (u'esc-', 'esc'),
    (u'esc/', 'esc'),
    (u'eschenlaube', 'eschenlaube'),
    (u'everywhere', 'diverse'),
    (u'exil', 'exil'),
    (u'exlosib', 'explosiv'),
    (u'exlosiv', 'explosiv'),
    (u'explosiv', 'explosiv'),
    (u'fast alle clubs in graz', 'diverse'),
    (u'festsaal', 'arbeiterkammer'),
    (u'fh joanneum', 'fh_joanneum'),
    (u'flex', 'flex'),
    (u'fluc', 'fluc'),
    (u'fm4', 'fm4'),
    (u'forum keler', 'forum_stadtpark'),
    (u'forum keller', 'forum_stadtpark'),
    (u'forum stadpark', 'forum_stadtpark'),
    (u'forum stadtpark', 'forum_stadtpark'),
    (u'forumstadtpark', 'forum_stadtpark'),
    (u'forumwiese', 'forum_stadtpark'),
    (u'franziskaner', 'franziskaner_platz'),
    (u'freibad mettersdorf', 'freibad_mettersdorf'),
    (u'freie galerie', 'freie_galerie'),
    (u'ganz graz', 'diverse'),
    (u'gmd', 'generalmusikdirektion'),
    (u'graz all over', 'diverse'),
    (u'graz und gleisdorf', 'diverse'),
    (u'graz und steiermark', 'diverse'),
    (u'graz und umgebung', 'diverse'),
    (u'grazer kinos', 'diverse'),
    (u'gulaschhütte', 'gulaschhuette'),
    (u'haider cider', 'cider_farm'),
    (u'haider farm', 'cider_farm'),
    (u'haiderfarm', 'cider_farm'),
    (u'harrach', 'harrach'),
    (u'hauptbahnhof', 'hauptbahnhof_graz'),
    (u'hauptplatz', 'graz_hauptplatz'),
    (u'haus der architektur', 'hda'),
    (u'hda ', 'hda'),
    (u'hda/', 'hda'),
    (u'literaturhaus', 'literaturhaus_graz'),
    (u'list halle', 'helmut_list_halle'),
    (u'helmut list', 'helmut_list_halle'),
    (u'helmut-list', 'helmut_list_halle'),
    (u'helsinki', 'radio_helsinki'),
    (u'herbstbar', 'herbstbar'),
    (u'hot spot', 'hot_spot'),
    (u'iku ', 'iku'),
    (u'iku,', 'iku'),
    (u'imcubus', 'imcubus'),
    (u'infolade', 'infoladen'),
    (u'isop', 'isop'),
    (u'jugen- & kulturzentrum house', 'juz_house'),
    (u'jugend&kulturzentrum house', 'juz_house'),
    (u'jugend- & kulturzentrum house', 'juz_house'),
    (u'jugend- & kulturzentrum house', 'juz_house'),
    (u'jugend- und kulturzentrum house', 'juz_house'),
    (u'juz house', 'juz_house'),
    (u'juz mureck', 'juz_house'),
    (u'juz*house', 'juz_house'),
    (u'juz.house', 'juz_house'),
    (u'juzhouse', 'juz_house'),
    (u'k1 - beisl', 'k1_beisl'),
    (u'k1 beisl', 'k1_beisl'),
    (u'k1-beisl', 'k1_beisl'),
    (u'kammersaal', 'arbeiterkammer'),
    (u'kaiser franz josef kai', 'sub'),
    (u'kasematten', 'kasemattenbuehne'),
    (u'kf uni', 'kf_uni'),
    (u'kf-uni', 'kf_uni'),
    (u'kfu ', 'kf_uni'),
    (u'kfuni', 'kf_uni'),
    (u'kig ', 'kig'),
    (u'kig!', 'kig'),
    (u'kig_', 'kig'),
    (u'kim ', 'forum_stadtpark'),
    (u'kim/', 'forum_stadtpark'),
    (u'kunsthaus', 'kunsthaus'),
    (u'kunstlabor', 'medien_kunstlabor'),
    (u'landesmuseum', 'museum_joanneum'),
    (u'lendluft', 'spektral_lendluft'),
    (u'libertad', 'cafe_libertad'),
    (u'lila eule', 'lila_eule'),
    (u'loam', 'da_loam'),
    (u'da laom', 'da_loam'),
    (u'loft', 'loft'),
    (u'm59', 'jazz_m59'),
    (u'massiv', 'club_massiv'),
    (u'mediathek', 'diemediathek'),
    (u'medienfabrik', 'ehemalige_medienfabrik'),
    (u'medienturm', 'medienturm'),
    (u'meerschein', 'meerscheinschloessl'),
    (u'mehrere locations', 'diverse'),
    (u'minoriten', 'minoriten_graz'),
    (u'mohoga', 'mohoga'),
    (u'moxx', 'wist'),
    (u'mumuth', 'mumuth'),
    (u'murpromenade', 'murpromenade'),
    (u'musikdirektion', 'generalmusikdirektion'),
    (u'niese', 'niesenberger'),
    (u'iesenberger', 'niesenberger'),
    (u'non stop', 'non_stop'),
    (u'non-stop', 'non_stop'),
    (u'non- ', 'non_stop'),
    (u'nonstop', 'non_stop'),
    (u'nova park', 'hotel_novapark'),
    (u'novapark', 'hotel_novapark'),
    (u'oper', 'oper_graz'),
    (u'orpheum', 'orpheum_graz'),
    (u'p.p.c', 'ppc'),
    (u'papierfabrik', 'papierfabrik'),
    (u'parkhouse', 'parkhouse'),
    (u'passamtwiese', 'passamtwiese'),
    (u'postgarage', 'postgarage'),
    (u'pro&st', 'cafe_prost'),
    (u'prost', 'cafe_prost'),
    (u'rabenstein', 'burg_rabenstein'),
    (u'raggam', 'raggam'),
    (u'raumwerk', 'raumwerk'),
    (u'rechbauer', 'rechbauer_kino'),
    (u'red box', 'arcadium'),
    (u'reigen', 'reigen'),
    (u'resowi', 'resowi'),
    (u'rhizom', 'rhizom'),
    (u'rondo', 'rondo'),
    (u'rosa pink', 'galerie_rosa_pink'),
    (u'rosa-pink', 'galerie_rosa_pink'),
    (u'rotor', 'rotor'),
    (u'schaumbad', 'schaumbad'),
    (u'schauspielhaus', 'schauspielhaus'),
    (u'scherbe', 'die_scherbe'),
    (u'schillingdorf', 'borraville'),
    (u'schubert-kino', 'schubertkino'),
    (u'schubertkino', 'schubertkino'),
    (u'seifenfabrik', 'seifenfabrik'),
    (u'siebing', 'raggam'),
    (u'space04', 'kunsthaus'),
    (u'spektral', 'spektral'),
    (u'stockwerk', 'stockwerkjazz'),
    (u'sublime', 'sublime'),
    (u'teatro', 'teatro'),
    (u'theatro', 'teatro'),
    (u'thienfeld', 'vipers'),
    (u'uni-t', 'unit'),
    (u'unit', 'unit'),
    (u'villa borra', 'borraville'),
    (u'veilchen', 'veilchen'),
    (u'viperes', 'vipers'),
    (u'vipers', 'vipers'),
    (u'volkshaus', 'kpoe_volkshaus'),
    (u'volxhaus', 'kpoe_volkshaus'),
    (u'vorklinik', 'vorklinik'),
    (u'wakuum', 'wakuum'),
    (u'welthaus', 'welthaus'),
    (u'wendepunkt', 'wendepunkt'),
    (u'wiesen', 'wiesen'),
    (u'wildon', 'wildon'),
    (u'wist', 'wist'),
    (u'ziegelwerk', 'ziegelwerk'),
    (u'palaver', 'palaver'),
    (u'pallaver', 'palaver'),
    (u'kaiserfeld', 'cafe_kaiserfeld'),
    (u'das lokal', 'das_lokal'),
    (u'daslokal', 'das_lokal'),
    (u'wahllokal', 'diverse'),
    (u'forum kloster', 'forum_kloster'),
    (u'forumkloster', 'forum_kloster'),
    (u'generalihof', 'generalihof'),
    (u'gironcoli', 'gironcoli_museum'),
    (u'klagenfurt', 'klagenfurt'),
    (u'gleisdorf', 'gleisdorf'),
    (u'feldbach', 'feldbach'),
    (u'weiz', 'weiz'),
    (u'stenfeld', 'fuerstenfeld'),
    (u'kottulinsky', 'kottulinsky'),
    (u'kulturkompetenzzentrum', 'niesenberger'),
    (u'leibnitz', 'leibnitz'),
    (u'reinerhof', 'reinerhof'),
    (u'kongress', 'grazer_congress'),
    (u'congress', 'grazer_congress'),
    (u'stadthalle', 'grazer_stadthalle'),
    (u'volkstheater', 'grazer_volkstheater'),
    (u'elektronische musik', 'iem'),
    (u'karl-franzens', 'kf_uni'),
    (u'jazzkeller', 'leibnitz'),
    (u'landesmueum', 'museum_joanneum'),
    (u'laafeld', 'radkersburg'),
    (u'gorna', 'radkersburg'),
    (u'nstlerhaus', 'kuenstlerhaus_graz'),
    (u'music_house', 'music_house'),
    (u'muwa', 'museum_der_wahrnehmung'),
    (u'wahrnehmung', 'museum_der_wahrnehmung'),
    (u'kristallwerk', 'kristallwerk'),
    (u'volksgarten', 'volksgarten'),
    (u'verschiedene', 'diverse'),
    (u'weltcaf', 'weltcafe'),
    # begin non-cannonical comparison
    (u'geidorf', 'geidorf_kino'),
    (u'ljubljana', 'ljubljana'),
    (u'pekarna', 'maribor'),
    (u'union halle', 'unionhalle'),
    (u'union platz', 'leibnitz'),
    (u'subsub', 'ljubljana'),
    (u'linz', 'linz'),
    (u'wien', 'wien'),
    (u'zagreb', 'zagreb'),
    (u'maribor', 'maribor'),
    (u'mariahilfer', 'diverse'),
    (u'innenstadt', 'diverse'),
    (u'jakominiplatz', 'diverse'),
    (u'kaiser-josef-platz', 'diverse'),
    (u'mureck', 'mureck'),
    (u'dtiroler', 'diverse'),
    (u'karmeliterplatz', 'diverse'),
    (u'herrengasse', 'diverse'),
    (u'griesplatz', 'diverse'),
    (u'kiz', 'kiz'),
    (u'sub', 'sub'),
    (u'ekh', 'ekh'),
    (u'ppc', 'ppc'),
    (u'ska', 'ska'),
    (u'tao', 'tao'),
    (u'wall', 'wall'),
    (u'ttz', 'kristallwerk'),
    (u'kug', 'kug'),
    (u'nil', 'baodo_im_nil'),
    (u'wuk', 'wuk'),
    (u'iem', 'iem'),
    (u'institut ', 'kf_uni'),
    (u'uni ', 'kf_uni'),
    (u'hs ', 'kf_uni'),
    (u'lend', 'diverse'),
    (u'graz', 'diverse'),
    (u'museumsakademie', 'museum_joanneum'),
    (u'gemeindeamt', 'diverse'),
    (u'gemeinderat', 'diverse'),
    (u'camp', 'camp_herbstbar'),
])
loc_map_keys = loc_map.keys()

known_locations = {
    'borraville': {'title': 'Borraville'},
    'veilchen': {'title': 'Veilchen'},

    }

# loop over events
for event in eventrows:
    #try:
        #except Exception as err:
    #    #print "error in row" , str(rowcount)
    #    print "FAIL export of event ", str(event['pc_eid']), err
    #    #print rawtext
    #    items_fail += 1

    def _get_key(title):
        for item in loc_map_keys:
            if item in title:
                return loc_map[item]
        return title

    eventnode = dom.createElement('event')

    # process location information
    locstring = str(event['pc_location']).decode(IN_ENCODING)
    if "{" in locstring:
        _locstruct = phpserialize.unserialize(locstring)
        # cleanup locations details
        locstruct = {}
        for key, val in _locstruct.items():
            key = _cleanup_textonly(key)
            val = _cleanup_textonly(val)
            locstruct[key] = val
        loc = _get_key(locstruct["event_location"].lower())
        if loc:
            locations[loc] = locstruct
    else:
        locstring = _cleanup_textonly(locstring)
        loc = _get_key(locstring.lower())
        if loc and not loc in loc_map:
            # if it's already there, it might be better defined...
            locations[loc] = {'event_location': locstring}

    if loc:
        eventnode.setAttribute('location_name', loc)

    # export fields
    fields = [
                'pc_contname',
                'pc_eid',
                'pc_fee',
                'pc_contemail',
                'pc_duration',
                'pc_website',
               # 'pc_aid',
               # 'pc_recurrfreq',
                'pc_eventstatus',
                'pc_time',
                'pc_informant',

                'pc_conttel',
                'pc_alldayevent',
              # 'pc_recurrspec',
                'pc_eventDate',
              #  'pc_recurrtype',
                'pc_startTime',
                'pc_topic'
                ]
    for attr in fields:
        eventnode.setAttribute(attr, str(event[attr]).decode(IN_ENCODING))

    # only set end date if value is set
    for attr in ['pc_endDate', 'pc_endTime']:
        if event[attr]:
            eventnode.setAttribute(attr , str(event[attr]).decode(IN_ENCODING))

    title = cleanTextFromControlChars(str(event["pc_title"]).decode(IN_ENCODING))
    eventnode.setAttribute("pc_title" , title)

    # clean + add event text
    posting_text = str(event['pc_hometext']).decode(IN_ENCODING)
    posting_text = cleanTextFromControlChars(posting_text)
    lines = posting_text.split("\n")
    if ':text:' in lines[0]:
        lines[0] = re.sub(':text:','', lines[0])
        posting_text= "<br/>".join(lines)
    elif ':html:' in lines[0]:
        lines[0] = re.sub(':html:','', lines[0])
        posting_text= "".join(lines)

    txt = dom.createElement('text')
    txt.appendChild(dom.createCDATASection(posting_text))
    eventnode.appendChild(txt)

    # tag(s)
    tagnode = dom.createElement('tag')
    tagnode.setAttribute('name', categories[str(event['pc_catid'])])
    eventnode.appendChild(tagnode)

    #tagnode = dom.createElement('tag')
    #tagnode.setAttribute('name', '__event_import')
    #eventnode.appendChild(tagnode)

    dom.childNodes[0].appendChild(eventnode)
    items_ok += 1


eventcursor.close()
conn.close()

with open("export-events.xml", "w") as f:
    f.write(dom.toprettyxml(encoding=OUT_ENCODING))

print "events export done! ok:", items_ok, ", failed:", items_fail


### LOCATIONS

# case insensitive sorting
locations = collections.OrderedDict(sorted(locations.items()))  #, key=str.lower))


dom = Document()
dom.appendChild(dom.createElement('export'))
for k in sorted(locations.keys()):
    loc = locations[k]
    lnode = dom.createElement('location')
    if type(loc) == dict:
        for attr, val in loc.items():
            lnode.setAttribute(attr, val)
    dom.childNodes[0].appendChild(lnode)
    lnode.setAttribute('name', k)

with open("export-places.xml", "w") as f:
    f.write(dom.toprettyxml(encoding=OUT_ENCODING))


import json
with open("export-places.json", "w") as f:
    f.write(json.dumps(
        locations,
        encoding='utf-8',
        #ensure_ascii=False,
        sort_keys=False,  # locations already case-insensitive sorted
        indent=4,
        separators=(',', ': ')
    ))

print "places export done! number places: %s" % len(locations)
