import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    hbcur=conn.cursor()
    dpaper={}
    hbcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in hbcur:
        dpaper[name]=term_id
    hbcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '河北日报' not in dpaper:
        print('未找到 河北日报 分类，正在新建 河北日报 分类...')
        hbcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("河北日报",quote("河北日报")))
        hbpid=hbcur.lastrowid
        hbcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(hbpid,hbpid,dpaper['日报']))
        hbcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('河北日报 分类建立完成！')
    else:
        print('河北日报 正在删除原有文章...')
        hbpid=dpaper['河北日报']
        hbcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(hbpid,))
        hbcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(hbpid,))
        hbcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(hbpid,))
        hbcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('河北日报 删除原有文章完成！')
    print('河北日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://hbrb.hebnews.cn/?')
    cathtml=Getproxy().Parserget(re.findall(r'url=(.+)"',indexhtml.text)[0])
    cathtml.encoding='utf-8'
    hbcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for hbcat in hbcats:
        hbcatname=hbcat[1].replace('版 ','版：')
        hbcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(hbcatname,quote(re.sub(r'\s+','-',(hbcat[1]+'-河北日报').replace('版 ','版：'))[0:22])))
        hbsubcatid=hbcur.lastrowid
        hbcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(hbsubcatid,hbsubcatid,hbpid))
        hbcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://hbrb.hebnews.cn/pc/paper/layout/%s'%hbcat[0])
        tlshtml.encoding='utf-8'
        hbtls=re.findall(r'<a href="(.+)" >(.+)</a>',tlshtml.text)
        for hbtl in hbtls:
            hbtitle=hbtl[1]
            hblink='http://hbrb.hebnews.cn/pc/paper/%s'%hbtl[0].replace('../','')
            contenthtml=Getproxy().Parserget(hblink)
            contenthtml.encoding='utf-8'
            hbcontents=re.findall(r'<p>(.+)</p>',contenthtml.text,flags=re.I)
            hbcontent=re.sub(r'</p><p>','<br><br>',''.join(hbcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(hblink,hblink)
            print('河北日报 %s 正在上传 %s...'%(hbcatname,hbtitle))
            hbcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            hbcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            hbcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(hbcontent,hbtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','河北日报-'+hbtitle))[0:22]))))
            hbcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(hbcur.lastrowid,hbsubcatid))
            hbcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(hbsubcatid,))
            print('河北日报 %s 完成上传 %s！'%(hbcatname,hbtitle))
    print('河北日报 获取最新文章完成！')
    conn.close()