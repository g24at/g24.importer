from postmarkup import render_bbcode
import postmarkup
import re

def transformPostingText(text):
    weird_strings = set(re.findall("\[[^:]*(:[a-zA-Z0-9]+\])",  text))
    for str in weird_strings:
        text = re.sub(str,"]", text)

    pm = postmarkup.create(annotate_links=False)
    xhtml = pm.render_to_html(text, auto_urls=False, cosmetic_replace=False)
    #xhtml = render_bbcode(text)
    xhtml = pm.standard_unreplace(xhtml)    # unescape html tags
    return xhtml


def cleanTextFromControlChars(text):
    cleaned = []
    for line in text.split("\n"):
        cleaned.append(''.join(c for c in line if ord(c) >= 32))
    return "\n".join(cleaned)


