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
    jxcur=conn.cursor()
    dpaper={}
    jxcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in jxcur:
        dpaper[name]=term_id
    jxcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '江西日报' not in dpaper:
        print('未找到 江西日报 分类，正在新建 江西日报 分类...')
        jxcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("江西日报",quote("江西日报")))
        jxpid=jxcur.lastrowid
        jxcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jxpid,jxpid,dpaper['日报']))
        jxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('江西日报 分类建立完成！')
    else:
        print('江西日报 正在删除原有文章...')
        jxpid=dpaper['江西日报']
        jxcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jxpid,))
        jxcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jxpid,))
        jxcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(jxpid,))
        jxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('江西日报 删除原有文章完成！')
    print('江西日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://epaper.jxwmw.cn')
    cathtml=Getproxy().Parserget('http://epaper.jxwmw.cn/'+re.findall(r'URL=(.+)"',indexhtml.text)[0])
    cathtml.encoding='utf-8'
    jxcats=re.findall(r'<a class="rigth_bmdh_href" href="(.+)">(.+)</a>',cathtml.text)
    for jxcat in jxcats:
        jxcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(jxcat[1],quote(re.sub(r'\s+','-',(jxcat[1]+'-江西日报').replace(':',''))[0:22])))
        jxsubcatid=jxcur.lastrowid
        jxcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jxsubcatid,jxsubcatid,jxpid))
        jxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://epaper.jxwmw.cn/html/%s/%s'%(daydate,jxcat[0]))
        tlshtml.encoding='utf-8'
        jxtls=re.findall(r'<a href="(.+)">(.+)</a></div>',tlshtml.text)
        for jxtl in jxtls:
            jxtitle=jxtl[1]
            jxlink='http://epaper.jxwmw.cn/html/%s/%s'%(daydate,jxtl[0])
            contenthtml=Getproxy().Parserget(jxlink)
            contenthtml.encoding='utf-8'
            jxcontents=re.findall(r'<P>(.+)<P>',contenthtml.text,flags=re.I)
            jxcontent=re.sub(r'<P>','<br><br>',''.join(jxcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(jxlink,jxlink)
            print('江西日报 %s 正在上传 %s...'%(jxcat[1],jxtitle))
            jxcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            jxcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            jxcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(jxcontent,jxtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','江西日报-'+jxtitle))[0:22]))))
            jxcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(jxcur.lastrowid,jxsubcatid))
            jxcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(jxsubcatid,))
            print('江西日报 %s 完成上传 %s！'%(jxcat[1],jxtitle))
    print('江西日报 获取最新文章完成！')
    conn.close()