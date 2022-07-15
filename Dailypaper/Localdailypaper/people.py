import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    timeheaders={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36'}
    timehtml=Getproxy().Parserget('https://www.beijing-time.org/t/time.asp',headers=timeheaders)
    curtime=re.findall(r'nyear=(.+);\s+nmonth=(.+);\s+nday=(.+);',timehtml.text)
    nyear=int(curtime[0][0])
    nmonth=int(curtime[0][1])
    nday=int(curtime[0][2])
    daydate='%d-%02d/%02d'%(nyear,nmonth,nday)
    conn=configok()[2]
    peoplecur=conn.cursor()
    dpaper={}
    peoplecur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in peoplecur:
        dpaper[name]=term_id
    peoplecur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '人民日报' not in dpaper:
        print('未找到 人民日报 分类，正在新建 人民日报 分类...')
        peoplecur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("人民日报",quote("人民日报")))
        peoplepid=peoplecur.lastrowid
        peoplecur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(peoplepid,peoplepid,dpaper['日报']))
        peoplecur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('人民日报 分类建立完成！')
    else:
        print('人民日报 正在删除原有文章...')
        peoplepid=dpaper['人民日报']
        peoplecur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(peoplepid,))
        peoplecur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(peoplepid,))
        peoplecur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(peoplepid,))
        peoplecur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('人民日报 删除原有文章完成！')
    print('人民日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://paper.people.com.cn/rmrb/paperindex.htm')
    cathtml=Getproxy().Parserget('http://paper.people.com.cn/rmrb/'+re.findall(r'URL=(.+)"',indexhtml.text)[0])
    peoplecats=re.findall(r'<a id=pageLink href=(.+)>(.+)</a>',cathtml.text)
    for peoplecat in peoplecats:
        peoplecur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(peoplecat[1],quote(re.sub(r'\s+','-',(peoplecat[1]+'-人民日报').replace(':',''))[0:22])))
        peoplesubcatid=peoplecur.lastrowid
        peoplecur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(peoplesubcatid,peoplesubcatid,peoplepid))
        peoplecur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://paper.people.com.cn/rmrb/html/%s/%s'%(daydate,peoplecat[0].replace('./','')))
        peopletls=re.findall(r'<a href=(.+?)>(.+?)  </a>',tlshtml.text)
        for peopletl in peopletls:
            peopletitle=peopletl[1]
            peoplelink='http://paper.people.com.cn/rmrb/html/%s/%s'%(daydate,peopletl[0])
            contenthtml=Getproxy().Parserget(peoplelink)
            peoplecontents=re.findall(r'<P>(.+)</P><!--/enpcontent-->\s+<INPUT',contenthtml.text,flags=re.I)
            peoplecontent=re.sub(r'</P><P>','<br><br>',''.join(peoplecontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(peoplelink,peoplelink)
            print('人民日报 %s 正在上传 %s...'%(peoplecat[1],peopletitle))
            peoplecur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            peoplecur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            peoplecur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(peoplecontent,peopletitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','人民日报-'+peopletitle))[0:22]))))
            peoplecur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(peoplecur.lastrowid,peoplesubcatid))
            peoplecur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(peoplesubcatid,))
            print('人民日报 %s 完成上传 %s！'%(peoplecat[1],peopletitle))
    print('人民日报 获取最新文章完成！')
    conn.close()