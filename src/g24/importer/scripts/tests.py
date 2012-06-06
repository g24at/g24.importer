 # -*- coding: utf -*-
import unittest
from pnexport import transformPostingText

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None


    def test_oneliners(self):
        
        cases = []
        
        # simple B
        cases.append (("text, 1234:test [b:479bf42510]test, something:else, test [/b:479bf42510], ende!", 
                       "text, 1234:test <strong>test, something:else, test </strong>, ende!"))
        
        # img with url between tags
        cases.append (("text, [img:9f40f45e57]http://adamstrang.widerstand.org/images/flyer/flyer666.jpg[/img:9f40f45e57], ende!", 
                       'text, <img src="http://adamstrang.widerstand.org/images/flyer/flyer666.jpg"></img>, ende!'))

        # transforms bare urls into links
        #cases.append (("text, http://www.mapec.at/program2.html ende!", 
        #               'text, <a href="http://www.mapec.at/program2.html">http://www.mapec.at/program2.html</a> ende!'))

        # leaves bare urls alone
        cases.append (("text, http://www.mapec.at/program2.html ende!", 
                       'text, http://www.mapec.at/program2.html ende!'))


        # keeps the tags 
        cases.append (("<h1>headline&gt; &lt;</h1> &gt; &lt;", 
                       '<h1>headline&gt; &lt;</h1> &gt; &lt;'))
        
        # email transform
#        cases.append (("oder schickt mir ein mail an  [email]testeamil@gmx.net[/email]...", 
#                       'oder schickt mir ein mail an  <a href="mailto:testeamil@gmx.net">testeamil@gmx.net</a>...'))        
        

        for case in cases:
            output = transformPostingText(case[0])
            self.assertEqual(case[1], output)


    def test_escapeing(self):
        
        src="""[b:3e68732ebc]BLACK HOLE[/b:3e68732ebc]

[b:3e68732ebc]Fr. 28.11.2003 - 21.00 Uhr[/b:3e68732ebc]
@ Uhrturmkasematten, GRAZ - Schlossberg - direkt unter dem Uhrturm 

special lineup: 

&gt;&gt;&gt; Live 
[b:3e68732ebc]Dan Doormouse[/b:3e68732ebc] (Addict Records - Miami/USA) 
[b:3e68732ebc]Abelcain[/b:3e68732ebc] (Zhark, Zod, Low Res - Madison/USA) 
[b:3e68732ebc]Ripit[/b:3e68732ebc] (Riposte Records - Paris/France) 
[b:3e68732ebc]Hecate[/b:3e68732ebc] (Zhark, Praxis - Basel/CH)"""

        expected="<strong>BLACK HOLE</strong><br/><br/><strong>Fr. 28.11.2003 - 21.00 Uhr</strong><br/>@ Uhrturmkasematten, GRAZ - Schlossberg - direkt unter dem Uhrturm <br/><br/>special lineup: <br/><br/>&gt;&gt;&gt; Live <br/><strong>Dan Doormouse</strong> (Addict Records - Miami/USA) <br/><strong>Abelcain</strong> (Zhark, Zod, Low Res - Madison/USA) <br/><strong>Ripit</strong> (Riposte Records - Paris/France) <br/><strong>Hecate</strong> (Zhark, Praxis - Basel/CH)"
        
        output = transformPostingText(src)
        self.assertEqual(expected, output)
        
    def test_mixed_tags(self):
        
        """ behavoir for auto-urls False """
        
        src = 'test some url: http://singleurl.com ' \
                'html tag <a href="http://testme.com/abc">click here</a> ' \
                'bbtag [url]http://hallo.at/test/test[/url]'
        
        expected = u'test some url: http://singleurl.com ' \
                'html tag <a href="http://testme.com/abc">click here</a> ' \
                'bbtag <a href="http://hallo.at/test/test">http://hallo.at/test/test</a>'

        output = transformPostingText(src)
        print output      
        
        self.assertEqual(expected, output)
        
    def DONTRUNtest_complex(self):
        src = """
test text vor tags
[b:479bf42510] tag text : nochmal test [/b:479bf42510]
zwischen text abc: defgh i !
insgesamt handelt es sich dabei um material von  [b:479bf42510] 871 stück!!!!!!!!!
vinyl...[/b:479bf42510]
http://www.somelink.at in die news rubrik
oder schickt mir ein mail an  [email]testeamil@gmx.net[/email]...
        """     
        
        expected=u'<br/>test text vor tags<br/><strong> tag text : nochmal test </strong><br/>zwischen text abc: defgh i !<br/>insgesamt handelt es sich dabei um material von  <strong> 871 stück!!!!!!!!!<br/>vinyl...</strong><br/><a href="http://www.somelink.at">http://www.somelink.at</a> in die news rubrik<br/>oder schickt mir ein mail an  <a href="mailto:testeamil@gmx.net">testeamil@gmx.net</a>...'
        expected=u'<br/>test text vor tags<br/><strong> tag text : nochmal test </strong><br/>zwischen text abc: defgh i !<br/>insgesamt handelt es sich dabei um material von  <strong> 871 st��ck!!!!!!!!!<br/>vinyl&#8230;</strong><br/><a href="http://www.somelink.at">http://www.somelink.at</a> in die news rubrik<br/>oder schickt mir ein mail an  testeamil@gmx.net&#8230;<br/>  '
        output = transformPostingText(src)
                
        self.assertEqual(expected, output)   
        
        
    def test_posting_of_death(self):
        src = """
g24.at empfiehlt aus aktuellem Anlass einen Blick auf den aktuellen DVD Release des Films &quot;The Crisis Of Civilization&quot; zu werfen, der am Elevate Festival 2011 seine Weltpremiere feierte!

[img:efb3d193d1]http://g24.at/images/_teaser/elevate11_documentary_film_selection_110826_emblem_cut_200.png[/img:efb3d193d1]

DVD + Online Release als Torrent warten auf euch: http://crisisofcivilization.com/dvdandonlinerelease/
Torrent hier: https://thepiratebay.se/torrent/7099987/The.Crisis.Of.Civilization.2011.DOCU.720p.HQ

Bestellt die DVD um den Filmemacher zu unterstützen!

<h1>DVD and Online release! March 14th!</h1>
                                      <a href="http://crisisofcivilization.com/dvdandonlinerelease/"><img src="http://crisisofcivilization.com/wp-content/uploads/2012/03/LAUNCH.gif" class="attachment-full wp-post-image" alt="LAUNCH" title="LAUNCH" height="258" width="298"></a>                  <h2><strong><em><a href="http://crisisofcivilization.com/watch/" target="_blank">WATCH IT !</a></h2></em></strong>
We are proud to announce that <em>The Crisis of Civilization</em> will be available on DVD or to watch online from <em><strong>Wednesday March 14th 2012</strong></em>. You&#8217;ll be able to watch and download the film for free, and buy the DVD (from the website or from Amazon) with loads of lovely extras for you to get your teeth into.
<h3>&#8220;a film which offers a glimmer of hope to the overwhelmed.&#8221; &#8211; Little White Lies</h3>
<p><img class="alignnone  wp-image-3219" title="backandfront" src="http://crisisofcivilization.com/wp-content/uploads/2012/03/backandfront-1024x719.gif" alt="" height="431" width="614"></p>
<p>The DVD will be available in both PAL and NTSC formats, comes in 100% recycled packaging (of course!), and includes over an hour of bonus material, deleted scenes, remix films, and additional interview footage.</p>
http://crisisofcivilization.com/dvdandonlinerelease/
<p>Also including subtitles in English, Spanish, Portuguese, French, German, Swedish and Chinese!</p>
<h3>&quot;A unique film. Everyone should see it&quot;<em> Nick Broomfield</em></h3>
<p>Finally, you&#8217;ll have the chance to show the film to your friends and family or put on a screening in your community whenever you want &#8211; and help us to get the message out there to as many people as possible!</p>
<p><strong><em>So put the date in your diary, forward this to your friends, blog about it and help spread the word because THE CRISIS OF CIVILIZATION is breaking loose!</em></strong><br>
<strong><em>Read a review of the DVD over at <a href="http://www.littlewhitelies.co.uk/dvds/the-crisis-of-civilization-18010" target="_blank">LITTLE WHITE LIES</a> (leading UK independent film magazine)<br>
</em></strong></p>

http://crisisofcivilization.com/dvdandonlinerelease/
"""
        #output = transformPostingText(src)
        #print output

if __name__ == '__main__':
    unittest.main()