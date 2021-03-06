from xml.etree.ElementTree import iterparse
from lxml import etree
import re
outf = open('out600.txt', 'w',encoding='utf-8')
context = etree.iterparse('F:\data\enwiki-20210101-pages-articles-multistream.xml')
#context = iter(context)
cnt = 0
flag = False
id = ''
text = ''
title = ''
for event, elem in context:
    cnt+=1
   # print(elem.tag)
   # print(elem.text)
    if(elem.tag== 'shal'):print(1)

    if(elem.tag=='{http://www.mediawiki.org/xml/export-0.10/}sha1'):
        #print(1)
        flag = True
        #print(cnt)
        continue
    if flag:
        if(elem.tag=='{http://www.mediawiki.org/xml/export-0.10/}id'):
            flag = False
            id = elem.text
           # print(id)
            continue

    if(elem.tag=='{http://www.mediawiki.org/xml/export-0.10/}title'):
        title = elem.text
        continue
        #print(title)
    if (elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text'):
        text = elem.text
        if (text==None or len(text) < 3): continue
        text = re.sub('\n', 'SSSSSS', text)
        text = re.sub(r"{{Infobox",'EEEEEE',text)
        #text = re.sub(r"EEEEEE(.*)SSSSSS\|",' ',text)

        loc = re.search(r"(SSSSSS)(.{0,10})'''",text)
        if(loc != None):loc = loc.span()[0]
        else: loc = -1
        #if id!='' and int(id) == 595:
        #    print(text)
         #   break
        if(loc!=-1):
            loceq = -1
            for a in re.finditer('==', text):
                if(a.span()[0]>loc):
                    loceq = a.span()[0]
                    break
            print(id)
            text = text[loc:loceq]

            text = re.sub(r"'''|''|\t",'',text)
            text = re.sub(r'<ref(.*?)(</ref>|/>)', ' ', text)
            text = re.sub(r'{{(.*?)({{(.*?)({{(.*?)}}?)(.*?)}}?)(.*?)}}', '', text)
            text = re.sub(r'{{(.*?)}}','',text)
            text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)]]', r'\1', text)

            text = re.sub(r'SSSSSS|EEEEEE','',text)
            #print(re.findall(r'<ref(.*?)</ref>|/>',text))
            st = ''.join([id,'\t',title,'\t',text[:1000],'\n'])
            outf.write(st)
    elem.clear()
    # 选取当前节点的所有先辈（父、祖父等）以及当前节点本身
    for ancestor in elem.xpath('ancestor-or-self::*'):
        # 如果当前节点还有前一个兄弟，则删除父节点的第一个子节点。getprevious():返回当前节点的前一个兄弟或None。
        while ancestor.getprevious() is not None:
            # 删除父节点的第一个子节点，getparent()：返回当前节点的父元素或根元素或None。
            del ancestor.getparent()[0]