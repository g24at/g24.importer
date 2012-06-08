import MySQLdb
import time
from pnexport import transformPostingText, cleanTextFromControlChars
from xml.dom.minidom import Document
from xml.dom.minidom import parse

from ConfigParser import ConfigParser
import sys

cfg = ConfigParser()
cfg.read('../config.ini')

conn = MySQLdb.connect (host = cfg.get('default', 'mysql.host'),
                           user = cfg.get('default', 'mysql.user'),
                           passwd = cfg.get('default', 'mysql.passwd'),
                           db = cfg.get('default', 'mysql.db'))

"""

mysql> describe nuke_phpbb_posts;
+-----------------+-----------------------+------+-----+---------+----------------+
| Field           | Type                  | Null | Key | Default | Extra          |
+-----------------+-----------------------+------+-----+---------+----------------+
| post_id         | mediumint(8) unsigned | NO   | PRI | NULL    | auto_increment |
| topic_id        | mediumint(8) unsigned | NO   | MUL | 0       |                |
| forum_id        | smallint(5) unsigned  | NO   | MUL | 0       |                |
| poster_id       | mediumint(8)          | NO   | MUL | 0       |                |
| post_time       | int(11)               | NO   | MUL | 0       |                |
| poster_ip       | varchar(8)            | NO   |     |         |                |
| post_username   | varchar(25)           | YES  |     | NULL    |                |
| enable_bbcode   | tinyint(1)            | NO   |     | 1       |                |
| enable_html     | tinyint(1)            | NO   |     | 0       |                |
| enable_smilies  | tinyint(1)            | NO   |     | 1       |                |
| enable_sig      | tinyint(1)            | NO   |     | 1       |                |
| post_edit_time  | int(11)               | YES  |     | NULL    |                |
| post_edit_count | smallint(5) unsigned  | NO   |     | 0       |                |
| post_attachment | tinyint(1)            | NO   |     | 0       |                |
| post_icon       | tinyint(2) unsigned   | NO   |     | 0       |                |
+-----------------+-----------------------+------+-----+---------+----------------+

mysql> describe nuke_phpbb_posts_text;
+--------------+-----------------------+------+-----+---------+-------+
| Field        | Type                  | Null | Key | Default | Extra |
+--------------+-----------------------+------+-----+---------+-------+
| post_id      | mediumint(8) unsigned | NO   | PRI | 0       |       |
| bbcode_uid   | varchar(10)           | NO   |     |         |       |
| post_subject | varchar(60)           | YES  |     | NULL    |       |
| post_text    | text                  | YES  |     | NULL    |       |
+--------------+-----------------------+------+-----+---------+-------+

['post_username', 'post_attachment', 'post_time', 'poster_ip', 'post_subject', 'post_edit_time', 'bbcode_uid', 'enable_html', 'forum_id', 'enable_sig', 'poster_id', 'post_id', 'enable_smilies', 'post_icon', 'post_edit_count', 'topic_id', 'post_text', 'pt.post_id', 'enable_bbcode']

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
dom.appendChild(dom.createElement('export'))

# load cat / tag information
tagdom = parse('category-tag-map.xml')
export_topics = []
cats_info = {}
for cat in tagdom.getElementsByTagName('cat'):
    if cat.getAttribute("export") == "1":
        export_topics.append(cat.getAttribute("id"))

    tags = []
    for tag in cat.getElementsByTagName('tag'):
        tags.append(tag.getAttribute('name'))

    cats_info[cat.getAttribute("id")] = tags


test_set = True
custom_limit = ""
if len (sys.argv) > 1:
    if sys.argv[1] == "all" : test_set = False
    else : test_set = False ; custom_limit = sys.argv[1]


# select topics for export
sql_str = "select * from nuke_phpbb_topics "
sql_str = sql_str + " where forum_id in (" + ','.join(export_topics) + ")"
if      test_set            : sql_str = sql_str + " order by RAND() limit 0,200"
elif    custom_limit != ""  : sql_str = sql_str + " " + custom_limit

print "Selecting Topics : ", sql_str
topiccursor = conn.cursor (MySQLdb.cursors.DictCursor)
topiccursor.execute (sql_str);
topicrows = topiccursor.fetchall()

topics_ok = 0
topics_fail = 0
# loop over topics
for topic in topicrows:
    try:
        threadnode = dom.createElement('thread')

        tags = []
        tags = set(cats_info[str(topic["forum_id"])])

        # select posts for topic
        postcursor  = conn.cursor (MySQLdb.cursors.DictCursor)
        selectfields = ["p.post_id", "p.post_username", "pt.post_subject", "u.username", "p.post_time", "pt.post_text","p.enable_bbcode"]
        sql_str = """
            select """ + ','.join(selectfields) + """ from nuke_phpbb_posts p
            left join nuke_phpbb_posts_text pt on p.post_id = pt.post_id
            left join nuke_phpbb_users u on u.user_id = p.poster_id
            where topic_id = """ + str(topic['topic_id']) + " order by post_time"
        postcursor.execute (sql_str);
        rows = postcursor.fetchall()

        # loop over topic's posts
        for row in rows:
            postnode = dom.createElement('post')

            # un-escape htmlchars in subject
            row['post_subject'] = row['post_subject'].replace("&amp;","&").replace("&quot;",'"').replace("&lt;","<").replace("&gt;",">")

            # set attributes
            export_fields = ["post_username", "post_subject", "username", "post_id"]
            for attr in export_fields:
                postnode.setAttribute(attr, str(row[attr]).decode('latin-1'))

            tstruct = time.gmtime( row["post_time"])
            postnode.setAttribute('post_time', time.strftime("%m/%d/%Y, %H:%M:%S CET", tstruct))

            # add posting text
            posting_text = cleanTextFromControlChars(row['post_text'].decode('latin-1'))
            txt         = dom.createElement('text')
            if row['enable_bbcode']:
                posting_text  = transformPostingText(posting_text)
            txt.appendChild(dom.createCDATASection(posting_text))
            postnode.appendChild(txt)

            # add tags
            for t in tags:
                tagnode = dom.createElement('tag')
                tagnode.setAttribute('name', t)
                postnode.appendChild(tagnode)

            # add posting to thread
            threadnode.appendChild(postnode)

        # add topic/thread to export
        dom.childNodes[0].appendChild(threadnode)

        postcursor.close ()

        print "export ok topic", str(topic['topic_id'])
        topics_ok += 1
    except Exception as err:
        #print "error in row" , str(rowcount)
        print "FAIL export of topic ", str(topic['topic_id']), err
        #print rawtext
        topics_fail += 1

topiccursor.close()
conn.close ()

with open("export-posts.xml", "w") as f:
    f.write(dom.toprettyxml(encoding="UTF-8"))

print "done! ok:", topics_ok, ", failed:", topics_fail
