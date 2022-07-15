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
    tjcur=conn.cursor()
    dpaper={}
    tjcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in tjcur:
        dpaper[name]=term_id
    tjcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '天津日报' not in dpaper:
        print('未找到 天津日报 分类，正在新建 天津日报 分类...')
        tjcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("天津日报",quote("天津日报")))
        tjpid=tjcur.lastrowid
        tjcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(tjpid,tjpid,dpaper['日报']))
        tjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('天津日报 分类建立完成！')
    else:
        print('天津日报 正在删除原有文章...')
        tjpid=dpaper['天津日报']
        tjcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(tjpid,))
        tjcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(tjpid,))
        tjcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(tjpid,))
        tjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('天津日报 删除原有文章完成！')
    print('天津日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://epaper.tianjinwe.com/tjrb')
    cathtml=Getproxy().Parserget('http://epaper.tianjinwe.com/tjrb/'+re.findall(r'URL=(.+)"',indexhtml.text)[0])
    cathtml.encoding='utf-8'
    tjcats=re.findall(r'<a id=pageLink href="(.+)">(.+)</a>',cathtml.text)
    for tjcat in tjcats:
        tjcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(tjcat[1],quote(re.sub(r'\s+','-',(tjcat[1]+'-天津日报').replace(':',''))[0:22])))
        tjsubcatid=tjcur.lastrowid
        tjcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(tjsubcatid,tjsubcatid,tjpid))
        tjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://epaper.tianjinwe.com/tjrb/html/%s/%s'%(daydate,tjcat[0]))
        tlshtml.encoding='utf-8'
        tjtls=re.findall(r'<a href="(.+)">(.+)</a></div>',tlshtml.text)
        for tjtl in tjtls:
            tjtitle=tjtl[1]
            tjlink='http://epaper.tianjinwe.com/tjrb/html/%s/%s'%(daydate,tjtl[0])
            contenthtml=Getproxy().Parserget(tjlink)
            contenthtml.encoding='utf-8'
            tjcontents=re.findall(r'<P>(.+)<P>',contenthtml.text,flags=re.I)
            tjcontent=re.sub(r'<P>','<br><br>',''.join(tjcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(tjlink,tjlink)
            print('天津日报 %s 正在上传 %s...'%(tjcat[1],tjtitle))
            tjcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            tjcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            tjcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(tjcontent,tjtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','天津日报-'+tjtitle))[0:22]))))
            tjcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(tjcur.lastrowid,tjsubcatid))
            tjcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(tjsubcatid,))
            print('天津日报 %s 完成上传 %s！'%(tjcat[1],tjtitle))
    print('天津日报 获取最新文章完成！')
    conn.close()