# -*- coding: utf-8 -*-
import collective.setuphandlertools as sht
import logging
logger = logging.getLogger("g24.importer")

cat = (
    'deine-htu',
    'beratung',
    'studienvertretungen',
    'veranstaltungen',
    'services',
)

def setup_html_transform(context):
    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return
    sht.unsafe_html_transform(logger)

def setup_content(context):

    if sht.isNotThisProfile(context, 'g24.importer-setup_content.txt'):
        return

    site = context.getSite()

    sht.delete_items(site, ('front-page', 'news', 'events'), logger)

    sht.add_user(site, 'thet', 'thet',
                 email='johannes@raggam.co.at', fullname="Johannes Raggam",
                 groups=['Administrators'], logger=logger)


    content_structure = [

        {'type': 'Folder',
         'id': 'news',
         'title': u'News',
         'opts': {'setLayout': 'newslisting',
                  'setDefault': True,
                  'setImmediatelyAddableTypes': ['Folderish News Item'],
                  'setExcludeFromNav': True,},
         'childs': [

            {'type': 'Folderish News Item',
             'title': NEWS1_TITLE,
             'data': {'description': NEWS1_DESC,
                      'image':sht.load_file(globals(), NEWS1_IMG),
                      'hottopic': NEWS1_HOT,
                      'category': NEWS1_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS2_TITLE,
             'data': {'description': NEWS2_DESC,
                      'teaserText': NEWS2_DESC,
                      'image':sht.load_file(globals(), NEWS2_IMG),
                      'hottopic': NEWS2_HOT,
                      'category': NEWS2_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS3_TITLE,
             'data': {'description': NEWS3_DESC,
                      'image':sht.load_file(globals(), NEWS3_IMG),
                      'hottopic': NEWS3_HOT,
                      'category': NEWS3_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS4_TITLE,
             'data': {'description': NEWS4_DESC,
                      'teaserText': NEWS4_DESC,
                      'image':sht.load_file(globals(), NEWS4_IMG),
                      'hottopic': NEWS4_HOT,
                      'category': NEWS4_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS5_TITLE,
             'data': {'description': NEWS5_DESC,
                      'image':sht.load_file(globals(), NEWS5_IMG),
                      'hottopic': NEWS5_HOT,
                      'category': NEWS5_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS6_TITLE,
             'data': {'description': NEWS6_DESC,
                      'teaserText': NEWS6_DESC,
                      'image':sht.load_file(globals(), NEWS6_IMG),
                      'hottopic': NEWS6_HOT,
                      'category': NEWS6_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS7_TITLE,
             'data': {'description': NEWS7_DESC,
                      'image':sht.load_file(globals(), NEWS7_IMG),
                      'hottopic': NEWS7_HOT,
                      'category': NEWS7_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS8_TITLE,
             'data': {'description': NEWS8_DESC,
                      'teaserText': NEWS8_DESC,
                      'image':sht.load_file(globals(), NEWS8_IMG),
                      'hottopic': NEWS8_HOT,
                      'category': NEWS8_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS9_TITLE,
             'data': {'description': NEWS9_DESC,
                      'text': NEWS9_TEXT,
                      'image':sht.load_file(globals(), NEWS9_IMG),
                      'hottopic': NEWS9_HOT,
                      'category': NEWS9_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS10_TITLE,
             'data': {'description': NEWS10_DESC,
                      'teaserText': NEWS10_DESC,
                      'image':sht.load_file(globals(), NEWS10_IMG),
                      'subtitle': NEWS10_SUB,
                      'hottopic': NEWS10_HOT,
                      'category': NEWS10_CAT,
            }},

            {'type': 'Folderish News Item',
             'title': NEWS11_TITLE,
             'data': {'description': NEWS11_DESC,
                      'teaserText': NEWS11_DESC,
                      'text': NEWS11_TEXT,
                      'image':sht.load_file(globals(), NEWS11_IMG),
                      'imageCaption': u'Das Winterride Festival ist eine Veranstaltung mit über tausend wintersportbegeisterten, jungen Leuten in Partylaune.',
                      'copyright': u'Max Mustermann',
                      'subtitle': NEWS11_SUB,
                      'hottopic': NEWS11_HOT,
                      'category': NEWS11_CAT,},
            'childs': [
                {'type': 'Image',
                 'title': 'img A',
                 'data': {'description': u'Aurora.',
                          'copyright': u'spaceweather.com',
                          'image':sht.load_file(globals(), NEWS10_IMG)}},
                {'type': 'Image',
                 'title': 'img B',
                 'data': {'description': u'Aurora 2.',
                          'copyright': u'spaceweather.com',
                          'image':sht.load_file(globals(), NEWS9_IMG)}},
                {'type': 'File',
                 'title': 'Cms Vendor Map',
                 'data': {'description': u'Einordnung von Plone in der CMS Vendor Map.',
                          'image':sht.load_file(globals(), 'setupdata/RSG-Vendor-Subway-Map-June2010.pdf')}},
                {'type': 'Link',
                 'title': 'g24.at',
                 'data': {'description': u'Community Website für Graz.',
                          'remoteUrl': 'http://g24.at/'}},
                {'type': 'Link',
                 'title': 'Radio Helsinki',
                 'data': {'description': u'Freies Community Radio in Graz.',
                          'remoteUrl': 'http://helsinki.at/'}},
                 ],
             },

            {'type': 'Folderish News Item',
             'title': NEWS12_TITLE,
             'data': {'description': NEWS12_DESC,
                      'teaserText': NEWS12_DESC,
                      'image':sht.load_file(globals(), NEWS12_IMG),
                      'copyright': u'spaceweather.com',
                      'imageCaption': u'Nordlichter.',
                      'hottopic': NEWS12_HOT,
                      'category': NEWS12_CAT,
            }},


            {'type': 'Folderish News Item',
             'title': NEWS13_TITLE,
             'data': {'description': NEWS13_DESC,
                      'teaserText': NEWS13_DESC,
                      'image':sht.load_file(globals(), NEWS13_IMG),
                      'copyright': u'spaceweather.com',
                      'imageCaption': u'Aurora.',
                      'hottopic': NEWS13_HOT,
                      'category': NEWS13_CAT,
            }},


            {'type': 'Folderish News Item',
             'title': NEWS14_TITLE,
             'data': {'description': NEWS14_DESC,
                      'teaserText': NEWS14_DESC,
                      'image':sht.load_file(globals(), NEWS14_IMG),
                      'copyright': u'spaceweather.com',
                      'imageCaption': u'Aurora.',
                      'subtitle': NEWS14_SUB,
                      'hottopic': NEWS14_HOT,
                      'category': NEWS14_CAT,
            }},


            {'type': 'Folderish News Item',
             'title': NEWS15_TITLE,
             'data': {'description': NEWS15_DESC,
                      'teaserText': NEWS15_DESC,
                      'image':sht.load_file(globals(), NEWS15_IMG),
                      'copyright': u'spaceweather.com',
                      'imageCaption': u'Aurora.',
                      'hottopic': NEWS15_HOT,
                      'category': NEWS15_CAT,
            }},


         ],
        },

        {'type': 'Folder',
         'id': 'deine-htu',
         'title': u'Deine HTU',
         'opts': {'setLayout': 'traverse_view',},
         'childs': [

             {'type': 'Folderish Document',
              'id': 'sekretariat',
              'title': u'Sekretariat',
             },

             {'type': 'Folderish Document',
              'id': 'vorsitz',
              'title': u'Vorsitz',
             },

             {'type': 'Folderish Document',
              'id': 'universitatsvertretung',
              'title': u'Universitätsvertretung',
             },

             {'type': 'Folderish Document',
              'id': 'studienvertretungen',
              'title': u'Studienvertretungen',
             },
            ]
        },

        {'type': 'Folder',
         'id': 'beratung',
         'title': u'Beratung',
         'opts': {'setLayout': 'traverse_view',},
         'childs': [

             {'type': 'Folderish Document',
              'id': 'soziales',
              'title': u'Soziales',
             },

             {'type': 'Folderish Document',
              'id': 'studium',
              'title': u'Studium',
             },

             {'type': 'Folderish Document',
              'id': 'lesbischwule',
              'title': u'LesBiSchwule',
             },

             {'type': 'Folderish Document',
              'id': 'internationales',
              'title': u'Internationales',
             },

         ]
        },

        {'type': 'Folderish Document',
         'id': 'studienvertretungen',
         'title': u'Studienvertretungen',
         'data': {'text': STV_TEXT},
         'opts': {'setLayout': 'studienvertretungen',},
         'childs': [

            {'type': 'Link',
             'id': 'stv-architektur',
             'title': 'StV Architektur (FAKarch)',
             'data': {'remoteUrl': u'http://arch.htu.tugraz.at/',
                      'description': u'Studienvertretung Fakultät Architektur TU Graz'},
            },

            {'type': 'Link',
             'id': 'stv-bauingenieurwissenschaften',
             'title': 'StV Bauingenieurwissenschaften (fv bau)',
             'data': {'remoteUrl': 'http://bau.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-vermessung-und-geoinformation',
             'title': 'StV Vermessung und Geoinformation',
             'data': {'remoteUrl': 'http://www.htu.tugraz.at/geodesy',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-maschinenbau-und-wirtschaftswissenschaften',
             'title': 'StV Maschinenbau und Wirtschaftswissenschaften (fak-MB)',
             'data': {'remoteUrl': 'http://maschinenbau.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-verfahrenstechnik',
             'title': 'StV Verfahrenstechnik',
             'data': {'remoteUrl': 'http://www.verfahrenstechnik.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-elektrotechnik',
             'title': 'StV Elektrotechnik',
             'data': {'remoteUrl': 'http://et.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-biomedical-engineering',
             'title': 'StV Biomedical Engineering',
             'data': {'remoteUrl': 'http://et.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-elektrotechnik-toningenieur',
             'title': 'StV Elektrotechnik - Toningenieur',
             'data': {'remoteUrl': 'http://www.toningenieur-graz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-telematik',
             'title': 'StV Telematik',
             'data': {'remoteUrl': 'http://www.telematik.edu/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-informatik-und-softwareentwicklung',
             'title': 'StV Informatik und Softwareentwicklung',
             'data': {'remoteUrl': 'http://bis.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-chemie',
             'title': 'StV Chemie',
             'data': {'remoteUrl': 'http://chemie.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-technische-mathematik',
             'title': 'StV Technische Mathematik',
             'data': {'remoteUrl': 'http://mathematik.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-technische-physik',
             'title': 'StV Technische Physik',
             'data': {'remoteUrl': 'http://physik.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-lehramtsstudium-darstellende-geometrie',
             'title': 'StV Lehramtsstudium Darstellende Geometrie',
             'data': {'remoteUrl': 'mailto:dg@htu.tugraz.at',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-molekularbiologie',
             'title': 'StV Molekularbiologie',
             'data': {'remoteUrl': 'http://www.biologie-graz.at/',
                      'description': u''},
            },

            {'type': 'Link',
             'id': 'stv-doktoratsstudien',
             'title': 'StV Doktoratsstudien',
             'data': {'remoteUrl': 'http://doktorat.htu.tugraz.at/',
                      'description': u''},
            },

            {'type': 'Folder',
             'id': 'telematik',
             'title': u'Telematik',
             'opts': {'lang': '', 'setExcludeFromNav': True,},
            },

            {'type': 'Folder',
             'id': 'informatik-und-softwareentwicklung',
             'title': u'Informatik und Softwareentwicklung',
             'opts': {'lang': '', 'setExcludeFromNav': True,},
            },

            {'type': 'Folder',
             'id': 'architektur',
             'title': u'Architektur',
             'opts': {'lang': '', 'setExcludeFromNav': True,},
            },

         ]
        },

        {'type': 'Folder',
         'id': 'veranstaltungen',
         'title': u'Veranstaltungen',
         'opts': {'setLayout': 'traverse_view',},
         'childs': [

             {'type': 'Folderish Document',
              'id': 'gesellschaftliches',
              'title': u'Gesellschaftliches',
             },

             {'type': 'Folderish Document',
              'id': 'politisches',
              'title': u'Politisches',
             },

             {'type': 'Folderish Document',
              'id': 'feste',
              'title': u'Feste',
             },

             {'type': 'Folder',
              'id': 'bildergalerien',
              'title': u'Bildergalerien',
              'opts': {'setLayout': 'albums_view',
                       'setImmediatelyAddableTypes': ['Folder']},
              'childs': [
                  {'type': 'Folder',
                   'title': u'Unsere Reise in den Weltraum',
                   'opts': {'setLayout': 'prettyPhoto_album_view'},
                   'childs': [
                       {'type': 'Image', 'title': u'A',
                        'data': {'image': sht.load_file(globals(), ALBUM_IMG1)}},
                       {'type': 'Image', 'title': u'B',
                        'data': {'image': sht.load_file(globals(), ALBUM_IMG2)}},
                       {'type': 'Image', 'title': u'C',
                        'data': {'image': sht.load_file(globals(), ALBUM_IMG3)}},
                       {'type': 'Image', 'title': u'D',
                        'data': {'image': sht.load_file(globals(), ALBUM_IMG4)}},
                       {'type': 'Image', 'title': u'E',
                        'data': {'image': sht.load_file(globals(), ALBUM_IMG5)}},
                    ]
                  },
                ]
            },
          ]
        },

        {'type': 'Folder',
         'id': 'services-downloads',
         'title': u'Services & Downloads',
         'opts': {'setLayout': 'traverse_view',},
         'childs': [

             {'type': 'Folderish Document',
              'id': 'copyshop',
              'title': u'Copyshop',
             },

             {'type': 'Folderish Document',
              'id': 'prufungsbeispielsammlungen',
              'title': u'Prüfungsbeispielsammlungen',
             },

             {'type': 'Folderish Document',
              'id': 'campusboard',
              'title': u'Campusboard',
             },

             {'type': 'Folderish Document',
              'id': 'sozialleistungen',
              'title': u'Sozialleistungen',
             },

             {'type': 'Folderish Document',
              'id': 'sonderprojektetopf',
              'title': u'Sonderprojektetopf',
             },

             {'type': 'Folderish Document',
              'id': 'sonstige-formulare',
              'title': u'Sonstige Formulare',
             },

         ]
        },

        {'type': 'Folderish Document',
         'id': 'kontakt',
         'title': u'Kontakt',
         'opts': {'setExcludeFromNav': True,},
         },

        {'type': 'Folderish Document',
         'id': 'impressum',
         'title': u'Impressum',
         'opts': {'setExcludeFromNav': True,},
        },

        {'type': 'Folder', 'title':u'Teasers',
         'opts': {'setLayout': 'folder_summary_view',
                  'setExcludeFromNav': True,
                  'workflow': None, # leave private
                  'setImmediatelyAddableTypes': ['Teaser']},
         'childs': [
             {'type': 'Teaser',
              'title': TEASER1_TITLE,
              'data': {'image':sht.load_file(globals(), TEASER1_IMG),
                       'link_external': TEASER1_LINK,
                       'importance': '3'}},
             ]
         },

        {'type': 'Folder', 'title':u'Partner',
         'opts': {'setLayout': 'folder_summary_view',
                  'setExcludeFromNav': True,
                  'workflow': None, # leave private
                  'setImmediatelyAddableTypes': ['Teaser']},
         'childs': [

            {'type': 'Image',
             'id': 'icon_facebook1.png',
             'title': 'Facebook',
             'data': {'image':sht.load_file(globals(), 'setupdata/icon_facebook1.png')}},

            {'type': 'Image',
             'id': 'icon_google1.png',
             'title': 'Google+',
             'data': {'image':sht.load_file(globals(), 'setupdata/icon_google1.png')}},

            {'type': 'Image',
             'id': 'icon_twitter1.png',
             'title': 'Facebook',
             'data': {'image':sht.load_file(globals(), 'setupdata/icon_twitter1.png')}},

            {'type': 'Image',
             'id': 'icon_rss1.png',
             'title': 'Facebook',
             'data': {'image':sht.load_file(globals(), 'setupdata/icon_rss1.png')}},


             {'type': 'Teaser',
              'title': LOGO1_TITLE,
              'data': {'image':sht.load_file(globals(), LOGO1_IMG),
                       'link_external': LOGO1_LINK,
                       'importance': '3'}},
             {'type': 'Teaser',
              'title': LOGO2_TITLE,
              'data': {'image':sht.load_file(globals(), LOGO2_IMG),
                       'link_external': LOGO2_LINK,
                       'importance': '2'}},
             ]
         },

        {'type': 'Topic',
         'id': 'site-feed',
         'title':u'HTU Graz - RSS Feed',
         'opts': {'lang': '', 'setExcludeFromNav': True,},
        },

    ]

    sht.create_item_runner(site, content_structure, lang='de', logger=logger)

    site.setLayout('traverse_view')

    try:
        topic = site['site-feed']
        topic.limitNumber = True
        topic.itemCount = 10
        sort_crit = topic.addCriterion('created','ATSortCriterion')
        sort_crit.setReversed(True)
        topic.reindexObject()
        logger.info('configured topic %s' % topic.id)
    except:
        pass



STV_TEXT = u"""
<article class="info-box">
<h2>Aufgaben der Studienvertretung</h2>
<p>Die Studienvertretung (StV) ist die Anlaufstelle für alle
Anliegen, die mit dem Studium zu tun haben. Ein möglichst reibungsloser
Studienablauf für die StudienkollegInnen ist das Ziel der Studienvertretung.
Darauf wird einerseits durch die Mitarbeit in der Studienkommission, wo der
Studienplan entworfen und weiterentwickelt wird, andererseits durch
individuelle Beratung für die Studierenden hingearbeitet. Das reicht von der
Erstsemestrigenberatung über Hilfe bei der Überwindung diverser bürokratischer
Hürden bis zur Intervention bei Problemen mit ProfessorInnen oder
AssistentInnen. Mit Fragen zu neuen Studienplänen und anderen Anrechnungen ist
man bei der Studienvertretung an der richtigen Adresse. Die Zusammensetzung
deiner Studienvertretung kannst du selbst bestimmen. Bei jeder ÖH-Wahl (alle
        zwei Jahre) werden die StV-MandatarInnen direkt gewählt (Personenwahl).
Je nach Anzahl der HörerInnen der Studienrichtung gibt es drei bis fünf
MandatarInnen.</p>
</article>
<hr>
<h2>Links zu den Studienrichtungsvertretungen</h2>
"""


LOGO1_TITLE = 'TU Graz'
LOGO1_IMG = 'setupdata/partner_tu_logo_neu.png'
LOGO1_LINK = 'http://tugraz.at/'

LOGO2_TITLE = 'Dein Copyshop'
LOGO2_IMG = 'setupdata/partner_copyshop.png'
LOGO2_LINK = 'http://deincopyshop.htu.tugraz.at/'

TEASER1_TITLE = 'Occupy'
TEASER1_IMG = 'setupdata/aside_Shepard_Fairey_Occupy_Poster.png'
TEASER1_LINK = 'http://g24.at'


NEWS15_TITLE = "Studiengebühren im SS 2012"
NEWS15_IMG = "setupdata/Peter-Sayers-IMGP7047_1324320135.jpg"
NEWS15_DESC = u"""
Da durch die HTU Graz geführte VfGH-Klage die Studiengebühren vom
Verfassungsgerichtshof als gesetzeswidrig per 29.2.2012 aufgehoben wurden,
werden an der TU Graz im Sommersemester 2012 KEINE Studiengebühren eingehoben.
"""
NEWS15_TEXT  = u"""
<p>
Im TUGRAZonline wurden außerdem bereits die Beiträge für das Sommersemester
eingetragen, ihr habt nur den ÖH-Beitrag in der Höhe von 16,50€ + 0,50€
Versicherung (=17,00€) zu zahlen! Es ist davon auszugehen, dass die Zahlscheine
für das nächste Semester diese Tage bei euch im Postfach liegen werden.
</p>
"""
NEWS15_CAT = cat[4]
NEWS15_HOT = False

NEWS14_TITLE = "MaturantInnenberatung 13.-17.2.2012"
NEWS14_IMG = "setupdata/Maximilian-Teodorescu-cometa-Garradd-august-29_1314744647.jpg"
NEWS14_SUB = u"Matura, was nun?"
NEWS14_DESC = u"""
Wo: ReSoWi-Zentrum, KFU, Universitätsstraße 15
Wann: Mo.-Fr. 9-15 Uhr (Vorträge alle 2 Stunden, durchgehende Beratung)
Jeweils um 09:00, 11:00 und 13:00 finden Vorträge mit den Themen: Studium, ÖH und Soziales statt
NEU: Abendeinheit am Do. 18-20 Uhr
"""
NEWS14_TEXT = u"""
<p>
Für all jene die sich noch nicht sicher sind, welchen Weg sie nach der Matura
einschlagen möchten, gibt es auch heuer wieder die MaturantInnenberatung
diesmal im ReSoWi. Gemeinsam mit der Karl-Franzens Uni, der Kunst- und der
Med-Uni, der Montanuni Leoben, den Grazer Fachhochschulen, Kollegs, Pädaks, dem
AMS und der psychologischen Studierendenberatung, laden wir, die HTU, euch
herzlich dazu ein, Informationen aus erster Hand von VertreterInnen all dieser
Organisationen und Studierenden aller Studienrichtungen zu holen.
</p><p>
Für weitere Informationen wendet euch bitte an studberatref (at) htu.tugraz.at
</p>
"""
NEWS14_CAT = cat[3]
NEWS14_HOT = False

NEWS13_TITLE = "2.o.UV-Sitzung im WS11"
NEWS13_IMG = "setupdata/Nenne-Aman1.jpg"
NEWS13_DESC = u"""
Am Freitag, den 20. Jänner 2011 um 16:00 Uhr, findet im Raum ATEG036 (HS XII)
(Rechbauerstraße 12 / EG 8010 Graz) die 2. ordentliche Sitzung der
Universitätsvertretung der Hochschülerinnen- und Hochschülerschaft an der TU
Graz im Wintersemester 2011/12 statt.
"""
NEWS13_TEXT = u"""
<p>
Die Tagesordnungspunkte sind:
</p>
<ol>
<li>Begrüßung, Feststellung der ordnungsgemäßen Einladung, der Anwesenheit und der Beschlussfähigkeit</li>
<li>Wahl der Schriftführerin bzw. des Schriftführers</li>
<li>Genehmigung der Tagesordnung</li>
<li>Genehmigung der Protokolle der letzten Sitzungen</li>
<li>Berichte der Vorsitzenden</li>
<li>Berichte der Vorsitzenden der Studienvertretungen</li>
<li>Berichte der von der Universitätsvertretung in akademische Gremien entsandten Studierendenvertreterinnen und – vertreter</li>
<li>Entsendung in akademische Gremien: Arbeitskreis für Gleichbehandlungsfragen, AG Gender & Diversity</li>
<li>Berichte der Referentinnen und Referenten</li>
<li>Berichte aus den Ausschüssen</li>
<li>HTU GmbH Neubesetzung</li>
<li>Homepage</li>
<li>Bericht E-Voting</li>
<li>Allfälliges</li>
</ol>
<p>
Auf euer kommen freut sich das Vorsitzteam,
Rudi, Flo und David
</p>
"""
NEWS13_CAT = cat[0]
NEWS13_HOT = False

NEWS12_TITLE = "Stellungnahme der HTU Graz zur Studiengebührendebatte"
NEWS12_IMG = "setupdata/Minoru-Yoneto1_strip.jpg"
NEWS12_DESC = u"""Kaum ein Tag vergeht, an dem es nicht neue Beiträge zu der
Debatte rund um die Studiengebühren gibt. Und allzu oft wären diese durchaus
entbehrlich, denn zumeist wird mit einem stark ideologisch motivierten
Hintergrund der eigene Standpunkt beton(ier)t. Dass die Vorschläge dabei des
Öfteren recht deutlich an der Realität vorbeigehen, ist also kein allzu großes
Wunder."""
NEWS12_TEXT = u"""
<p>
Zuerst sei einmal erwähnt, dass die HTU Graz mitverantwortlich für die aktuelle
Situation ist. Warum? Ganz einfach, wir waren es, die die Verfassungsklage ins
Rollen gebracht und aktiv unterstützt haben, welche zur Aufhebung der
Studiengebühren geführt hat. Das war auch absolut notwendig, da mit der
Quasi-Aufhebung im Herbst 2008 am Gesetz dermaßen schlampig herumgepfuscht
wurde, sodass eine Klage der einzige sinnvolle Schritt war. Und sie war
gerechtfertigt, sonst hätte der VfGH ja das Gesetz nicht aufgehoben.
</p><p>
Was nun durch die Politik und insbesondere durch das BMWF aufgeführt wird, ist
aber noch viel schlimmer: Da wird ein Gutachten eingeholt, welches von vielen
anerkannten JuristInnen in Österreich massiv angezweifelt wird, welches besagt,
dass die Universitäten nun autonom Studiengebühren einheben dürfen. Dahinter
steckt nichts anderes als parteipolitische Taktiererei, da in der Regierung
keine Einigkeit über Studiengebühren herrscht. Es ist absolut fahrlässig, den
Universitäten den schwarzen Peter zuzuschieben, da in vielen Passagen des
Universitätsgesetzes ganz klar darauf verwiesen wird, dass die Studiengebühren
vom Gesetzgeber festzulegen sind. Davon abgesehen würden die Universitäten ein
allfälliges Klagerisiko (und die ÖH würde mit Garantie jede einzelne
Universität klagen) selbst tragen müssen, da sie in unseren Augen ihre
Kompetenzen weit überschreiten würden.
</p><p>
Eine weitere Tatsache zu den Studiengebühren ist jene, dass sie KEINE
Zusatzeinnahmen für die Universitäten bedeuten. Warum? Schon bei der Einführung
im Jahr 2001 wurde versprochen, dass sie das Budget der Universitäten
aufstocken würden. Das war im Rückblick eine glatte Lüge, denn die Budgets der
Universitäten wurden postwendend um etwa die Summe gekürzt, die die
Studiengebühren zusätzlich einbrachten. Und niemand kann dafür garantieren,
dass dies nicht wieder passiert, sollten Studiengebühren in jeglicher Form
erneut eingeführt werden. Außerdem wird den Universitäten per Gesetz der Ersatz
für entfallene Studiengebühren garantiert, und zwar bis Oktober 2013.
</p><p>
Die Universitäten stehen vor schwersten budgetären Herausforderungen, keine
Frage. An der TU Graz droht ein realer Budgetrückgang von knapp 10%, sollte es
keine zusätzliche Mittel seitens des Finanzministeriums für die Universitäten
zur Verfügung gestellt werden. Das würde einen finanziellen, personellen und
damit fachlichen Kahlschlag für die Universität bedeuten, der auch an unserem
Studienalltag nicht spurlos vorübergehen würde. Schon jetzt gibt es kaum noch
Einsparungsmöglichkeiten und nennenswerten finanziellen Spielraum im Budget
kann man nur noch im Personalbereich erzielen.
</p><p>
Insofern ist die Politik nun gefordert, Farbe zu bekennen und Verantwortung zu
übernehmen: Entweder man finanziert die Universitäten so weit, dass diese
international anerkannte Lehre und Forschung bieten können oder man bekennt
sich offen dazu, dass (Aus)Bildung in Österreich keinen Stellenwert mehr hat.
In alter Manier weiterwursteln geht nicht mehr, das wurde nun viel zu lange
betrieben.
</p>
"""
NEWS12_CAT = cat[1]
NEWS12_HOT = True

NEWS11_TITLE = "Das Winterride Festival"
NEWS11_IMG = "setupdata/topStory_Imagebild.png"
NEWS11_DESC = u"""Es freut uns euch eine spektakuläre Schneesport- und
Musikfestivalreise vorstellen zu können: Das Winterride Festival ist eine
Veranstaltung mit über tausend wintersportbegeisterten, jungen Leuten in
Partylaune. Die französischen Alpen bieten dabei die perfekte Kulisse und ein
atemberaubendes Ambiente für dieses Event-Highlight."""
NEWS11_TEXT = u"""
<p>Carlo Pedersoli wurde 1929 in Neapel als Sohn eines Industriellen geboren. 1937 begann er in einem örtlichen Schwimmverein mit dem Schwimmsport. 1940 zog die Familie nach Rom, wo Pedersoli, nachdem er zwei Schulklassen übersprungen hatte, 1946 ein Chemiestudium an einer römischen Universität begann. Da seine Familie ein Jahr später nach Südamerika umzog, musste er das Studium jedoch abbrechen. In Südamerika übernahm er mehrere kurze Arbeiten: Er war Fließbandarbeiter in Rio de Janeiro, Bibliothekar in Buenos Aires und Sekretär in der italienischen Botschaft in Uruguay.</p>
<h3><br />Schwimmkarriere und erste Filmrollen</h3>
<p>Seine Leidenschaft für das Schwimmen blieb erhalten. 1948 kehrte der 19-jährige nach Italien zurück und schrieb sich als Student der Rechtswissenschaften ein, betrieb jedoch hauptsächlich das Schwimmen. Er wurde italienischer Meister im Brustschwimmen und über 100-Meter-Freistil, er schwamm am 19. September 1950 als erster Italiener unter einer Minute. Die italienische Meisterschaft gewann er sieben Jahre in Folge.<br />1950 hatte Pedersoli seine erste (Statisten-)Rolle</p>
<ul>
<li>als Prätorianer in Kaiser Neros Garde im Monumentalfilm Quo Vadis.und so weiter, zweizeiliges list-item</li>
<li>Es folgten weitere Kleinrollen in italienischen Produktionen: </li>
<li>Siluri umani (1954, deutscher Titel: Torpedomänner greifen an), </li>
</ul>
<p>Un Eroe dei nostri tempi (1955, deutscher Titel: Ein Held unserer Tage), Il Cocco di mamma (1957), In einem anderen Land (1957).<br />1951 nahm Pedersoli an den Mittelmeerspielen teil und gewann mit 59,7 s die Silbermedaille über 100 m[2].</p>
<blockquote class="pullquote">1952 nahm er an den Olympischen Spielen in Helsinki teil und wurde bei den Schwimmwettbewerben mit 58,9 s Fünfter im Vorlauf über 100 m Freistil. Mit der italienischen 4×200-Meter-Freistilstaffel</blockquote>
<p>erreichte er nicht das Finale. Er wurde wegen seiner sportlichen Erfolge mit anderen begabten Sportlern von der Universität Yale eingeladen und verbrachte einige Monate in den USA. 1956 nahm er an den Olympischen Spielen in Melbourne teil und erreichte über 100-Meter-Freistil den 11. Platz. 1957 beendete er mit 27 Jahren seine Schwimmkarriere und kehrte nach Südamerika zurück. Er sagte damals selbst: "Denn kommt der Ruhm zu schnell, steigt er einem leicht zu Kopf. Bei mir war es kurz davor."<br /><br /></p>
"""
NEWS11_SUB = u"Spektakuläre Schneesport- und Musikfestivalreise"
NEWS11_CAT = cat[3]
NEWS11_HOT = True

NEWS10_TITLE = "Inskription und Voranmeldung"
NEWS10_IMG = "setupdata/Francis-Anderson1.jpg"
NEWS10_DESC = u"""
Ab dem kommenden Wintersemester ist eine verpflichtende Voranmeldung für alle Erstsemestrigen sowie alle Studierenden, die ein Masterstudium ..."""
NEWS10_SUB = u"Achtung: Verpflichtende Voranmeldung nur bis 31. August"
NEWS10_CAT = cat[1]
NEWS10_HOT = False

NEWS9_TITLE = "Demo gegen die Kürzung der Familienbeihilfe"
NEWS9_IMG = "setupdata/Peter-Sayers-IMGP7047_1324320135.jpg"
NEWS9_DESC = u"""
Heute findet eine weitere Demonstration gegen die Belastungsmaßnahaamen für Studierende und deren Eltern seitens der Bundesregierung statt ..."""
NEWS9_TEXT = u"""
<h3>Protest wirkt: Polen legt Piraterieabkommen ACTA auf Eis</h3>
<p>"So lange nicht alle Zweifel ausgeräumt sind, so lange wird der Ratifizierungsprozess ausgesetzt"<br /><br /><b>"Argumente der Netzgemeinde berechtigt" - Ratifizierung ausgesetzt</b></p>
<p>Die Gegner des internationalen Urheberrechtsabkommens ACTA feiern einen ersten Erfolg: Die polnische Regierung hat am Freitag die Ratifizierung des Vertragswerks ausgesetzt.<br /><br /><b>Argumente der Netzgemeinde berechtigt</b></p>
<blockquote class="pullquote">"Ich teile die Ansicht derjenigen, die von unvollständigen Beratungen sprechen". Das sagte Ministerpräsident Donald Tusk in Warschau. Die Argumente der Netzgemeinde seien berechtigt. Auch in Österreich und anderen Ländern stößt das Handelsabkommen zur Abwehr von Fälschungen (Anti-Counterfeiting Trade Agreement) auf Widerstand.</blockquote>
<p class="pullquote">"So lange nicht alle Zweifel ausgeräumt sind, so lange wird der Ratifizierungsprozess ausgesetzt"<br /><br />Bei den Beratungen seien Internetnutzer nicht gehört worden, bemängelte Tusk. Stattdessen seien vor allem Gespräche mit den Inhabern von Urheberrechten geführt worden. "So lange nicht alle Zweifel ausgeräumt sind, so lange wird der Ratifizierungsprozess ausgesetzt", betonte Tusk. Es müsse zudem geprüft werden, ob ACTA mit dem Landesrecht vereinbar sei. Für eine Gültigkeit des Abkommens ist die Zustimmung von Parlament und Präsident notwendig.</p>
<h3 class="pullquote">Demos</h3>
<p class="pullquote">In Polen hatten Netzaktivisten tagelang Webseiten der Regierung blockiert, darunter auch das Internet-Angebot von Tusks Regierungskanzlei. In zahlreichen polnischen Städten gab es Demonstrationen gegen das Abkommen, auch Datenschützer meldeten Bedenken an.</p>
<h3 class="pullquote">Anonymous</h3>
<p class="pullquote">Teile der Anonymous-Bewegung griffen am Freitag die Webseite des griechischen Justizministeriums an. Statt der Inhalte des Ministeriums wurden etwa vier Stunden lang Proteste gegen die Sparmaßnahmen der griechischen Regierung und gegen die Teilnahme Griechenlands am ACTA-Abkommen verbreitet. Die Hacker gaben der Regierung zwei Wochen Zeit, aus ACTA auszusteigen. Andernfalls sollen neue Attacken folgen.<br /><br />Verschärfung des Urheberrechts<br /><br />Das nach Initiative der USA und Japans in mehrjährigen Verhandlungen 2011 fertiggestellte Abkommen sieht unter anderem vor, dass Internet-Anbieter für Urheberrechtsverletzungen von Kunden haftbar gemacht werden können. Kritiker sehen daher ACTA in einer Reihe mit Bestrebungen zur Verschärfung des Urheberrechts.<br /><br />Zustimmung des EU-Parlaments<br /><br />ACTA wurde am 26. Januar von der EU unterzeichnet. Das Abkommen verpflichtet zur Kooperation und Schaffung neuer Gesetze, die die Durchsetzung von Urheberrechten, vor allem im Kampf gegen gefälschte Arzneimittel und Datendiebstahl, erleichtern soll. Österreichs Regierung entschloss sich Ende Jänner zur Unterzeichnung. Vor dem In-Kraft-Treten von ACTA ist eine Zustimmung des EU-Parlaments erforderlich.<br /><br />Kritiker  haben für den 11. Februar zu Protesten aufgerufen - der WebStandard berichtete.  (APA/dpa)</p>
"""
NEWS9_CAT = cat[1]
NEWS9_HOT = True

NEWS8_TITLE = "Bücherbazar an der TU-Bibliothek"
NEWS8_IMG = "setupdata/Maximilian-Teodorescu-cometa-Garradd-august-29_1314744647.jpg"
NEWS8_DESC = u"""
Die Universitätsbibliothek veranstaltet vor Weihnachten wieder einen Bücherbazar, dieses Mal zum Thema Architektur. Hier die Eckdaten: Donnerstag, 16. Dezember 2010, - 9.00 - 15.00 Uhr, im Foyer der Hauptbibliothek, Technikerstraße 4, EG ..."""
NEWS8_CAT = cat[3]
NEWS8_HOT = False

NEWS7_TITLE = "Demonstration gegen die Kürzung der Familienbeihilfe"
NEWS7_IMG = "setupdata/Minoru-Yoneto1_strip.jpg"
NEWS7_DESC = u"""
Heute findet eine weitere Demonstration gegen die Belastungsmaßnahmen für Studierende und deren Eltern seitens der Bundesregierung statt. Die HTU Graz ruft euch auf, mitzumarschieren, denn es steht nicht nur eure Zukunft, sondern auch die Zukunft unseres Landes auf dem Spiel. Zum Ablauf der Demonstration:"""
NEWS7_CAT = cat[1]
NEWS7_HOT = False

NEWS6_TITLE = "Wahl11 - Das Ergebnis"
NEWS6_IMG = "setupdata/Nenne-Aman1.jpg"
NEWS6_DESC = u"""
Ergebnis der ÖH-Wahlen 2011 auf Universitätsebene ..."""
NEWS6_CAT = cat[0]
NEWS6_HOT = False

NEWS5_TITLE = "6.000 Studis darf man nicht überhören!"
NEWS5_IMG = "setupdata/Minoru-Yoneto1_strip.jpg"
NEWS5_DESC = u"""
Heute Nachmittag machten die Grazer Studierenden ihrem Unmut Luft und nahmen an ..."""
NEWS5_CAT = cat[1]
NEWS5_HOT = False

NEWS4_TITLE = "Resolution"
NEWS4_IMG = "setupdata/Francis-Anderson1.jpg"
NEWS4_DESC = u"""
Der Vollversammlung der Technischen Universität Graz. Das Rektorat der TU Graz wurde im Rahmen ..."""
NEWS4_CAT = cat[1]
NEWS4_HOT = False

NEWS3_TITLE = "2.o.UV-Sitzung im WS2010"
NEWS3_IMG = "setupdata/Peter-Sayers-IMGP7047_1324320135.jpg"
NEWS3_DESC = u"""
Am Donnerstag, dem 24.1.2011, findet die 2. o. Sitzung des WS2010/11 der Universitätsvertretung ..."""
NEWS3_CAT = cat[0]
NEWS3_HOT = False

NEWS2_TITLE = "Studien- und MaturantInnenberatung"
NEWS2_IMG = "setupdata/Maximilian-Teodorescu-cometa-Garradd-august-29_1314744647.jpg"
NEWS2_DESC = u"""
Auch heuer findet wieder die Studien- und MaturantInnenberatung in den Semesterferien statt."""
NEWS2_CAT = cat[1]
NEWS2_HOT = False

NEWS1_TITLE = "Ausschreibung für Homepage"
NEWS1_IMG = "setupdata/Nenne-Aman1.jpg"
NEWS1_DESC = u"""
& Benutzerverwaltungssystem der HochschülerInnenschaft an der TU Graz"""
NEWS1_CAT = cat[4]
NEWS1_HOT = False

ALBUM_IMG1 = NEWS11_IMG
ALBUM_IMG2 = NEWS10_IMG
ALBUM_IMG3 = NEWS9_IMG
ALBUM_IMG4 = NEWS8_IMG
ALBUM_IMG5 = NEWS6_IMG
ALBUM_IMG5 = NEWS5_IMG
