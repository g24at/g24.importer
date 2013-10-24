from ConfigParser import ConfigParser
from xml.dom.minidom import Document
import MySQLdb

IN_ENCODING = 'latin-1'
OUT_ENCODING = 'utf-8'

cfg = ConfigParser()
cfg.read('../config.ini')

conn = MySQLdb.connect (host = cfg.get('default', 'mysql.host'),
                           user = cfg.get('default', 'mysql.user'),
                           passwd = cfg.get('default', 'mysql.passwd'),
                           db = cfg.get('default', 'mysql.db'))

"""
mysql> describe nuke_phpbb_topics;
+---------------------+-----------------------+------+-----+---------+----------------+
| Field               | Type                  | Null | Key | Default | Extra          |
+---------------------+-----------------------+------+-----+---------+----------------+
| topic_id            | mediumint(8) unsigned | NO   | PRI | NULL    | auto_increment |
| forum_id            | smallint(8) unsigned  | NO   | MUL | 0       |                |
| topic_title         | char(60)              | NO   |     |         |                |
| topic_poster        | mediumint(8)          | NO   |     | 0       |                |
| topic_time          | int(11)               | NO   |     | 0       |                |
| topic_views         | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_replies       | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_status        | tinyint(3)            | NO   | MUL | 0       |                |
| topic_vote          | tinyint(1)            | NO   |     | 0       |                |
| topic_type          | tinyint(3)            | NO   | MUL | 0       |                |
| topic_first_post_id | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_last_post_id  | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_moved_id      | mediumint(8) unsigned | NO   | MUL | 0       |                |
| topic_attachment    | tinyint(1)            | NO   |     | 0       |                |
| topic_icon          | tinyint(2) unsigned   | NO   |     | 0       |                |
| support_status      | tinyint(3)            | NO   |     | 0       |                |
+---------------------+-----------------------+------+-----+---------+----------------+

mysql> describe nuke_phpbb_forums;
+-------------------------+-----------------------+------+-----+---------+----------------+
| Field                   | Type                  | Null | Key | Default | Extra          |
+-------------------------+-----------------------+------+-----+---------+----------------+
| forum_id                | smallint(5) unsigned  | NO   | PRI | NULL    | auto_increment |
| cat_id                  | mediumint(8) unsigned | NO   | MUL | 0       |                |
| forum_name              | varchar(150)          | YES  |     | NULL    |                |
| forum_desc              | text                  | YES  |     | NULL    |                |
| forum_status            | tinyint(4)            | NO   |     | 0       |                |
| forum_order             | mediumint(8) unsigned | NO   | MUL | 1       |                |
| forum_posts             | mediumint(8) unsigned | NO   |     | 0       |                |
| forum_topics            | mediumint(8) unsigned | NO   |     | 0       |                |
| forum_last_post_id      | mediumint(8) unsigned | NO   | MUL | 0       |                |
| prune_next              | int(11)               | YES  |     | NULL    |                |
| prune_enable            | tinyint(1)            | NO   |     | 0       |                |
| auth_view               | tinyint(2)            | NO   |     | 0       |                |
| auth_read               | tinyint(2)            | NO   |     | 0       |                |
| auth_post               | tinyint(2)            | NO   |     | 0       |                |
| auth_reply              | tinyint(2)            | NO   |     | 0       |                |
| auth_edit               | tinyint(2)            | NO   |     | 0       |                |
| auth_delete             | tinyint(2)            | NO   |     | 0       |                |
| auth_sticky             | tinyint(2)            | NO   |     | 0       |                |
| auth_announce           | tinyint(2)            | NO   |     | 0       |                |
| auth_vote               | tinyint(2)            | NO   |     | 0       |                |
| auth_pollcreate         | tinyint(2)            | NO   |     | 0       |                |
| auth_attachments        | tinyint(2)            | NO   |     | 0       |                |
| auth_download           | tinyint(2)            | NO   |     | 0       |                |
| topic_sort_order        | tinyint(2)            | NO   |     | 0       |                |
| post_sort_order         | tinyint(2)            | NO   |     | 0       |                |
| support_forum           | tinyint(1)            | NO   |     | 0       |                |
| exclude_global_announce | tinyint(1)            | NO   |     | 0       |                |
+-------------------------+-----------------------+------+-----+---------+----------------+

"""

dom = Document()
dom.appendChild(dom.createElement('cats'))

topiccursor = conn.cursor (MySQLdb.cursors.DictCursor)

sql_str = "select forum_id, forum_name, forum_desc, cat_title, cat_desc  from nuke_phpbb_forums f join nuke_phpbb_categories c on f.cat_id = c.cat_id"
topiccursor.execute (sql_str);
topicrows = topiccursor.fetchall()
for catrow in topicrows:
    # create cat element and add attributes
    cm = dom.createElement('cat')
    cm.setAttribute('export', str(1))
    cm.setAttribute('id', str(catrow['forum_id']).decode(IN_ENCODING))
    for attr in ['forum_name', 'cat_title'] :
        cm.setAttribute(attr, str(catrow[attr]).decode(IN_ENCODING))

    # add description
    desc = dom.createElement('desc')
    desc.appendChild(dom.createCDATASection(str(catrow['forum_desc']).decode(IN_ENCODING)))
    cm.appendChild(desc)

    tags = dom.createElement('tags')

    # add cat_title as tag
    tag = dom.createElement('tag')
    tag.setAttribute('name', catrow['cat_title'].decode(IN_ENCODING))
    tags.appendChild(tag)

    # split forum name into parts and add them as tags
    forumname = catrow['forum_name'].decode(IN_ENCODING)
    for val in [t for t in forumname.split(' ') if t not in ["","/","-"]]:
        tag = dom.createElement('tag')
        tag.setAttribute('name', val)
        tags.appendChild(tag)

    cm.appendChild(tags)
    dom.childNodes[0].appendChild(cm)

topiccursor.close()
conn.close ()

with open("category-tag-map.xml", "w") as f:
    f.write(dom.toprettyxml(encoding=OUT_ENCODING))
