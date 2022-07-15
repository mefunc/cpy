import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    amcur=conn.cursor()
    dpaper={}
    amcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in amcur:
        dpaper[name]=term_id
    amcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '澳門日報' not in dpaper:
        print('未找到 澳門日報 分类，正在新建 澳門日報 分类...')
        amcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("澳門日報",quote("澳門日報")))
        ampid=amcur.lastrowid
        amcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(ampid,ampid,dpaper['日报']))
        amcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('澳門日報 分类建立完成！')
    else:
        print('澳門日報 正在删除原有文章...')
        ampid=dpaper['澳門日報']
        amcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(ampid,))
        amcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(ampid,))
        amcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(ampid,))
        amcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('澳門日報 删除原有文章完成！')
    print('澳門日報 正在获取最新文章...')
    cathtml=Getproxy().Parserget('https://xiangyu-macau.oss-cn-hongkong.aliyuncs.com/app/szb/pc/layout/index.html')
    cathtml.encoding='utf-8'
    amcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for amcat in amcats:
        amcatname=amcat[1].replace('版 ','版：')
        amcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(amcatname,quote(re.sub(r'\s+','-',(amcat[1]+'-澳門日報').replace('版 ','版：'))[0:22])))
        amsubcatid=amcur.lastrowid
        amcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(amsubcatid,amsubcatid,ampid))
        amcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('https://xiangyu-macau.oss-cn-hongkong.aliyuncs.com/app/szb/pc/layout/%s'%amcat[0])
        tlshtml.encoding='utf-8'
        amtls=re.findall(r'<a href="(.+)" >(.+)</a></li>',tlshtml.text)
        for amtl in amtls:
            amtitle=amtl[1]
            amlink='https://xiangyu-macau.oss-cn-hongkong.aliyuncs.com/app/szb/pc/%s'%amtl[0].replace('../','')
            contenthtml=Getproxy().Parserget(amlink)
            contenthtml.encoding='utf-8'
            amcontents=re.findall(r'<p>(.+)</p>',contenthtml.text,flags=re.I)
            amcontent=re.sub(r'</p><p>','<br><br>',''.join(amcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(amlink,amlink)
            print('澳門日報 %s 正在上传 %s...'%(amcatname,amtitle))
            amcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            amcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            amcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(amcontent,amtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','澳門日報-'+amtitle))[0:22]))))
            amcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(amcur.lastrowid,amsubcatid))
            amcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(amsubcatid,))
            print('澳門日報 %s 完成上传 %s！'%(amcatname,amtitle))
    print('澳門日報 获取最新文章完成！')
    conn.close()