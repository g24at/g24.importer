import MySQLdb
import time
from pnexport import cleanTextFromControlChars
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import phpserialize
import re

from ConfigParser import ConfigParser
import sys


cfg = ConfigParser()
cfg.read('../config.ini')

conn = MySQLdb.connect (host = cfg.get('default', 'mysql.host'),
                           user = cfg.get('default', 'mysql.user'),
                           passwd = cfg.get('default', 'mysql.passwd'),
                           db = cfg.get('default', 'mysql.db'))

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

# loop over events
for event in eventrows:
    try:
        eventnode = dom.createElement('event')

        # process location information
        locstring = str(event['pc_location']).decode('latin-1')
        if "{" in locstring:
            locstruct = phpserialize.unserialize(locstring)
            loc = locstruct["event_location"]
            locations[loc] = locstruct
        else:
            loc = locstring
            locations[loc] = loc

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
            eventnode.setAttribute(attr, str(event[attr]).decode('latin-1'))

        # only set end date if value is set
        for attr in ['pc_endDate', 'pc_endTime']:
            if event[attr]:
                eventnode.setAttribute(attr , str(event[attr]).decode('latin-1'))

        title = cleanTextFromControlChars(str(event["pc_title"]).decode('latin-1'))
        eventnode.setAttribute("pc_title" , title)

        # clean + add event text
        posting_text = str(event['pc_hometext']).decode('latin-1')
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

    except Exception as err:
        #print "error in row" , str(rowcount)
        print "FAIL export of event ", str(event['pc_eid']), err
        #print rawtext
        items_fail += 1

eventcursor.close()
conn.close ()

with open("export-events.xml", "w") as f:
    f.write(dom.toprettyxml(encoding="UTF-8"))

print "done! ok:", items_ok, ", failed:", items_fail

dom = Document()
dom.appendChild(dom.createElement('export'))
for k in sorted(locations.keys()):
    loc = locations[k]
    lnode = dom.createElement('location')
    lnode.setAttribute('name', k)
    if type(loc) == dict:
        for attr, val in loc.items():
            lnode.setAttribute(attr,val)
    dom.childNodes[0].appendChild(lnode)

with open("export-places.xml", "w") as f:
    f.write(dom.toprettyxml(encoding="UTF-8"))

