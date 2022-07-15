import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    ahcur=conn.cursor()
    dpaper={}
    ahcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in ahcur:
        dpaper[name]=term_id
    ahcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '安徽日报' not in dpaper:
        print('未找到 安徽日报 分类，正在新建 安徽日报 分类...')
        ahcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("安徽日报",quote("安徽日报")))
        ahpid=ahcur.lastrowid
        ahcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(ahpid,ahpid,dpaper['日报']))
        ahcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('安徽日报 分类建立完成！')
    else:
        print('安徽日报 正在删除原有文章...')
        ahpid=dpaper['安徽日报']
        ahcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(ahpid,))
        ahcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(ahpid,))
        ahcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(ahpid,))
        ahcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('安徽日报 删除原有文章完成！')
    print('安徽日报 正在获取最新文章...')
    cathtml=Getproxy().Parserget('https://szb.ahnews.com.cn/ahrb/layout/index.html')
    cathtml.encoding='utf-8'
    ahcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for ahcat in ahcats:
        ahcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(ahcat[1],quote(re.sub(r'\s+','-',(ahcat[1]+'-安徽日报').replace(':',''))[0:22])))
        ahsubcatid=ahcur.lastrowid
        ahcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(ahsubcatid,ahsubcatid,ahpid))
        ahcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('https://szb.ahnews.com.cn/ahrb/layout/%s'%ahcat[0])
        tlshtml.encoding='utf-8'
        ahtls=re.findall(r'<a href="(.+)" >(.+)</a>',tlshtml.text)
        for ahtl in ahtls:
            ahtitle=ahtl[1]
            ahlink='https://szb.ahnews.com.cn/ahrb/%s'%ahtl[0].replace('../','')
            contenthtml=Getproxy().Parserget(ahlink)
            contenthtml.encoding='utf-8'
            ahcontents=re.findall(r'<!--enpcontent--><p>(.+)</p><!--/enpcontent-->',contenthtml.text,flags=re.I)
            ahcontent=re.sub(r'</p><p>','<br><br>',''.join(ahcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(ahlink,ahlink)
            print('安徽日报 %s 正在上传 %s...'%(ahcat[1],ahtitle))
            ahcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            ahcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            ahcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(ahcontent,ahtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','安徽日报-'+ahtitle))[0:22]))))
            ahcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(ahcur.lastrowid,ahsubcatid))
            ahcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(ahsubcatid,))
            print('安徽日报 %s 完成上传 %s！'%(ahcat[1],ahtitle))
    print('安徽日报 获取最新文章完成！')
    conn.close()