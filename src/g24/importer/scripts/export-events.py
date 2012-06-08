import MySQLdb
import time
#from pnexport import transformPostingText 
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import phpserialize

from ConfigParser import ConfigParser



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
    categories[str(cat['pc_catid'])] = str(cat['pc_catname'])

# select topics for export
sql_str = "select * from nuke_postcalendar_events where pc_eventstatus = 1"
sql_str = sql_str + " order by RAND() limit 0,15"

eventcursor = conn.cursor (MySQLdb.cursors.DictCursor)
eventcursor.execute (sql_str);
eventrows = eventcursor.fetchall() 

items_ok = 0
items_fail = 0
# loop over topics
for event in eventrows:
    try:
        eventnode = dom.createElement('event')
        
        locstring = str(event['pc_location']).decode('latin-1')
        if "{" in locstring:
            locstruct = phpserialize.unserialize(locstring)
            
            loc = locstruct["event_location"]
        else:
            loc = locstring
        
        eventnode.setAttribute('location_name', loc)
        
        fields = [  
                    'pc_contname', 
                    'pc_eid', 
                    'pc_fee', 
                    'pc_contemail', 
                    'pc_duration', 
                    'pc_website', 
                    'pc_aid', 
                    'pc_recurrfreq', 
                    'pc_eventstatus', 
                    'pc_time', 
                    'pc_informant', 
                    'pc_endTime', 
                    'pc_title', 
                    'pc_conttel', 
                    'pc_alldayevent', 
                    'pc_recurrspec', 
                    'pc_eventDate', 
                    'pc_endDate', 
                    'pc_recurrtype', 
                    'pc_startTime', 
                    'pc_topic'
                    ]
        for attr in fields:
            eventnode.setAttribute(attr , str(event[attr]).decode('latin-1'))    

        posting_text = str(event['pc_hometext']).decode('latin-1')
        cleaned = []
        for line in posting_text.split("\n"):
            cleaned.append(''.join(c for c in line if ord(c) >= 32))
            
        # add posting text 
        txt         = dom.createElement('text')
        posting_text= "\n".join(cleaned)
        txt.appendChild(dom.createCDATASection(posting_text))
        eventnode.appendChild(txt)
        
        # tag(s)
        tagnode = dom.createElement('tag')
        tagnode.setAttribute('name', categories[str(event['pc_catid'])])
        eventnode.appendChild(tagnode)
        
        tagnode = dom.createElement('tag')
        tagnode.setAttribute('name', '__event')
        eventnode.appendChild(tagnode)
        
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
