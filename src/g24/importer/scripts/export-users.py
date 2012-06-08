import MySQLdb
from xml.dom.minidom import Document

from ConfigParser import ConfigParser

cfg = ConfigParser()
cfg.read('../config.ini')

conn = MySQLdb.connect (host = cfg.get('default', 'mysql.host'),
                           user = cfg.get('default', 'mysql.user'),
                           passwd = cfg.get('default', 'mysql.passwd'),
                           db = cfg.get('default', 'mysql.db'))

# cursor = conn.cursor ()
cursor = conn.cursor (MySQLdb.cursors.DictCursor)

"""
mysql> describe nuke_phpbb_users;
+-----------------------+-----------------------+------+-----+----------------+-------+
| Field                 | Type                  | Null | Key | Default        | Extra |
+-----------------------+-----------------------+------+-----+----------------+-------+
| user_id               | mediumint(8)          | NO   | PRI | 0              |       |
| user_active           | tinyint(1)            | YES  |     | 1              |       |
| username              | varchar(25)           | NO   |     |                |       |
| user_password         | varchar(32)           | NO   |     |                |       |
| user_session_time     | int(11)               | NO   | MUL | 0              |       |
| user_session_page     | smallint(5)           | NO   |     | 0              |       |
| user_lastvisit        | int(11)               | NO   |     | 0              |       |
| user_regdate          | int(11)               | NO   |     | 0              |       |
| user_level            | tinyint(4)            | YES  |     | 0              |       |
| user_posts            | mediumint(8) unsigned | NO   |     | 0              |       |
| user_timezone         | decimal(5,2)          | NO   |     | 0.00           |       |
| user_style            | tinyint(4)            | YES  |     | NULL           |       |
| user_lang             | varchar(255)          | YES  |     | NULL           |       |
| user_dateformat       | varchar(14)           | NO   |     | %Y, %b %d - %I |       |
| user_new_privmsg      | smallint(5) unsigned  | NO   |     | 0              |       |
| user_unread_privmsg   | smallint(5) unsigned  | NO   |     | 0              |       |
| user_last_privmsg     | int(11)               | NO   |     | 0              |       |
| user_emailtime        | int(11)               | YES  |     | NULL           |       |
| user_viewemail        | tinyint(1)            | YES  |     | NULL           |       |
| user_attachsig        | tinyint(1)            | YES  |     | NULL           |       |
| user_allowhtml        | tinyint(1)            | YES  |     | 1              |       |
| user_allowbbcode      | tinyint(1)            | YES  |     | 1              |       |
| user_allowsmile       | tinyint(1)            | YES  |     | 1              |       |
| user_allowavatar      | tinyint(1)            | NO   |     | 1              |       |
| user_allow_pm         | tinyint(1)            | NO   |     | 1              |       |
| user_allow_viewonline | tinyint(1)            | NO   |     | 1              |       |
| user_notify           | tinyint(1)            | NO   |     | 0              |       |
| user_notify_pm        | tinyint(1)            | NO   |     | 0              |       |
| user_popup_pm         | tinyint(1)            | NO   |     | 0              |       |
| user_rank             | int(11)               | YES  |     | 0              |       |
| user_avatar           | varchar(100)          | YES  |     | NULL           |       |
| user_avatar_type      | tinyint(4)            | NO   |     | 0              |       |
| user_email            | varchar(255)          | YES  |     | NULL           |       |
| user_icq              | varchar(15)           | YES  |     | NULL           |       |
| user_website          | varchar(100)          | YES  |     | NULL           |       |
| user_from             | varchar(100)          | YES  |     | NULL           |       |
| user_sig              | text                  | YES  |     | NULL           |       |
| user_sig_bbcode_uid   | varchar(10)           | YES  |     | NULL           |       |
| user_aim              | varchar(255)          | YES  |     | NULL           |       |
| user_yim              | varchar(255)          | YES  |     | NULL           |       |
| user_msnm             | varchar(255)          | YES  |     | NULL           |       |
| user_occ              | varchar(100)          | YES  |     | NULL           |       |
| user_interests        | varchar(255)          | YES  |     | NULL           |       |
| user_actkey           | varchar(32)           | YES  |     | NULL           |       |
| user_newpasswd        | varchar(32)           | YES  |     | NULL           |       |
| user_login_tries      | smallint(5) unsigned  | NO   |     | 0              |       |
| user_last_login_try   | int(11)               | NO   |     | 0              |       |
+-----------------------+-----------------------+------+-----+----------------+-------+
"""

dom = Document()
dom.appendChild(dom.createElement('export'))

cursor.execute ("SELECT * from nuke_phpbb_users");
rows = cursor.fetchall()
for row in rows:
    user = dom.createElement('user')
    #export_fields = row.keys()
    export_fields = ["user_id", "user_active", "username", "user_level"]
    for attr in export_fields:
        user.setAttribute(attr, str(row[attr]).decode('latin-1'))
    dom.childNodes[0].appendChild(user)

cursor.close ()
conn.close ()

with open("userexport.xml", "w") as f:
    f.write(dom.toprettyxml(encoding="UTF-8"))
