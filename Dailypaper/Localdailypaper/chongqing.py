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
    cqcur=conn.cursor()
    dpaper={}
    cqcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in cqcur:
        dpaper[name]=term_id
    cqcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '重庆日报' not in dpaper:
        print('未找到 重庆日报 分类，正在新建 重庆日报 分类...')
        cqcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("重庆日报",quote("重庆日报")))
        cqpid=cqcur.lastrowid
        cqcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(cqpid,cqpid,dpaper['日报']))
        cqcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('重庆日报 分类建立完成！')
    else:
        print('重庆日报 正在删除原有文章...')
        cqpid=dpaper['重庆日报']
        cqcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(cqpid,))
        cqcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(cqpid,))
        cqcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(cqpid,))
        cqcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('重庆日报 删除原有文章完成！')
    print('重庆日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('https://epaper.cqrb.cn/html/cqrb')
    cathtml=Getproxy().Parserget('https://epaper.cqrb.cn/html/cqrb/'+re.findall(r"URL=(.+)'",indexhtml.text)[0])
    cathtml.encoding='utf-8'
    cqcats=re.findall(r'(.+)</span>：<a href="(.+)">(.+)</a> </td>',cathtml.text)
    for cqcat in cqcats:
        cqcatname=cqcat[0]+'：'+cqcat[2]
        cqcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(cqcatname,quote(re.sub(r'\s+','-',cqcatname+'-重庆日报')[0:22])))
        cqsubcatid=cqcur.lastrowid
        cqcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(cqsubcatid,cqsubcatid,cqpid))
        cqcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('https://epaper.cqrb.cn%s'%cqcat[1])
        tlshtml.encoding='utf-8'
        cqtls=re.findall(r"href=(.+?) alt='(.+?)'",tlshtml.text)
        for cqtl in cqtls:
            cqtitle=cqtl[1]
            cqlink='https://epaper.cqrb.cn/html/cqrb/%s/%s/%s'%(daydate,cqcat[0][1:-1],cqtl[0][1:-1])
            contenthtml=Getproxy().Parserget(cqlink)
            contenthtml.encoding='utf-8'
            cqcontents=re.findall(r'<p>(.+)</p>',contenthtml.text,flags=re.I)
            cqcontent=re.sub(r'</p><p>','<br><br>',''.join(cqcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(cqlink,cqlink)
            print('重庆日报 %s 正在上传 %s...'%(cqcatname,cqtitle))
            cqcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            cqcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            cqcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(cqcontent,cqtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','重庆日报-'+cqtitle))[0:22]))))
            cqcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(cqcur.lastrowid,cqsubcatid))
            cqcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(cqsubcatid,))
            print('重庆日报 %s 完成上传 %s！'%(cqcatname,cqtitle))
    print('重庆日报 获取最新文章完成！')
    conn.close()