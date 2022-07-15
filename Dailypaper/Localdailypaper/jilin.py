import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    jlcur=conn.cursor()
    dpaper={}
    jlcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in jlcur:
        dpaper[name]=term_id
    jlcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '吉林日报' not in dpaper:
        print('未找到 吉林日报 分类，正在新建 吉林日报 分类...')
        jlcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("吉林日报",quote("吉林日报")))
        jlpid=jlcur.lastrowid
        jlcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jlpid,jlpid,dpaper['日报']))
        jlcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('吉林日报 分类建立完成！')
    else:
        print('吉林日报 正在删除原有文章...')
        jlpid=dpaper['吉林日报']
        jlcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jlpid,))
        jlcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jlpid,))
        jlcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(jlpid,))
        jlcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('吉林日报 删除原有文章完成！')
    print('吉林日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://jlrbszb.dajilin.com')
    cathtml=Getproxy().Parserget('http://jlrbszb.dajilin.com/'+re.findall(r'href="(.+)"',indexhtml.text)[1].replace('./',''))
    cathtml.encoding='utf-8'
    jlcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for jlcat in jlcats:
        jlcatname=jlcat[1].replace('版 ','版：')
        jlcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(jlcatname,quote(re.sub(r'\s+','-',(jlcatname+'-吉林日报').replace(':',''))[0:22])))
        jlsubcatid=jlcur.lastrowid
        jlcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jlsubcatid,jlsubcatid,jlpid))
        jlcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://jlrbszb.dajilin.com/pc/paper/layout/%s'%jlcat[0])
        tlshtml.encoding='utf-8'
        jltls=re.findall(r'<a href="(.+)" >(.+)</a></li>',tlshtml.text)
        for jltl in jltls:
            jltitle=jltl[1]
            jllink='http://jlrbszb.dajilin.com/pc/paper/%s'%jltl[0].replace('../','')
            contenthtml=Getproxy().Parserget(jllink)
            contenthtml.encoding='utf-8'
            jlcontents=re.findall(r'<!--enpcontent--><p>(.+)</p><!--/enpcontent-->',contenthtml.text,flags=re.I)
            jlcontent=re.sub(r'</p><p>','<br><br>',''.join(jlcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(jllink,jllink)
            print('吉林日报 %s 正在上传 %s...'%(jlcatname,jltitle))
            jlcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            jlcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            jlcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(jlcontent,jltitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','吉林日报-'+jltitle))[0:22]))))
            jlcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(jlcur.lastrowid,jlsubcatid))
            jlcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(jlsubcatid,))
            print('吉林日报 %s 完成上传 %s！'%(jlcatname,jltitle))
    print('吉林日报 获取最新文章完成！')
    conn.close()