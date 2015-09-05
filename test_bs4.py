# -*- coding: utf-8 -*-
import bs4
from bs4 import BeautifulSoup 
import json
import sys

reload(sys)  
sys.setdefaultencoding('utf-8')  

def get_beautiful_soup(html_doc):
    text = html_doc.decode('GBK')
    soup = BeautifulSoup(text, 'html.parser')
    word_of_mouth = soup.find_all("div", "mouthcon-cont fn-clear")
    return word_of_mouth


def get_add_comments_url(bs_obj):
    add_dl = bs_obj.find("dl", "add-dl")
    if add_dl is not None:
        add_dl_url = add_dl.find("a").get('href')
    else:
        add_dl_url = None       
    return add_dl_url 

def extract_mark(bs_obj):
    data = {}
    for choose_dl in bs_obj.find_all("dl", "choose-dl"):
        if choose_dl.dt.string is not None:
            parameter = choose_dl.dt.string.strip()
        else:
            continue
        
        tokens = []
        if choose_dl.dd.string is not None:
            tokens.append(choose_dl.dd.string.strip())
        else:
            for token in choose_dl.dd.contents:
                if token.string is not None and token.string.strip() != '':
                    token = token.string.strip()
                    tokens.append(token)
                else:
                    pass
        
        marks = ','.join(tuple(tokens))
        data[parameter] = marks
    return data

def extract_comment(bs_obj):
    text_cont = bs_obj.find("div", "text-cont")
    contents = text_cont.contents
    for i in range(len(contents)):
        if isinstance(contents[i], bs4.element.NavigableString):
            contents[i] = contents[i].string
        else:
            contents[i] = '\n'
    comment = ''.join(tuple(contents))
    return comment

if __name__ == "__main__":
    fp = open("res")
    word_of_mouth = get_beautiful_soup(fp.read())
    for sample in word_of_mouth:
        data = extract_mark(sample)
        comment = extract_comment(sample)
        data[u'口碑'] = comment
        #print get_add_comments_url(sample) 
        print json.dumps(data, ensure_ascii = False) 
