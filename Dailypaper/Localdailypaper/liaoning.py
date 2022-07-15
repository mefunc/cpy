import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    lncur=conn.cursor()
    dpaper={}
    lncur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in lncur:
        dpaper[name]=term_id
    lncur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '辽宁日报' not in dpaper:
        print('未找到 辽宁日报 分类，正在新建 辽宁日报 分类...')
        lncur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("辽宁日报",quote("辽宁日报")))
        lnpid=lncur.lastrowid
        lncur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(lnpid,lnpid,dpaper['日报']))
        lncur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('辽宁日报 分类建立完成！')
    else:
        print('辽宁日报 正在删除原有文章...')
        lnpid=dpaper['辽宁日报']
        lncur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(lnpid,))
        lncur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(lnpid,))
        lncur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(lnpid,))
        lncur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('辽宁日报 删除原有文章完成！')
    print('辽宁日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://epaper.lnd.com.cn/lnrbindex.html')
    cathtml=Getproxy().Parserget('http://epaper.lnd.com.cn/'+re.findall(r'location.href="(.+)"',indexhtml.text)[1].replace('./',''))
    cathtml.encoding='utf-8'
    lncats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for lncat in lncats:
        lncatname=lncat[1].replace('版 ','版：')
        lncur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(lncatname,quote(re.sub(r'\s+','-',(lncat[1]+'-辽宁日报').replace('版 ','版：'))[0:22])))
        lnsubcatid=lncur.lastrowid
        lncur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(lnsubcatid,lnsubcatid,lnpid))
        lncur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://epaper.lnd.com.cn/lnrbepaper/pc/layout/%s'%lncat[0])
        tlshtml.encoding='utf-8'
        lntls=re.findall(r'<h3>\s+<a href="(.+)">(.+)<',tlshtml.text)
        for lntl in lntls:
            lntitle=lntl[1]
            lnlink='http://epaper.lnd.com.cn/lnrbepaper/pc/%s'%lntl[0].replace('../','')
            contenthtml=Getproxy().Parserget(lnlink)
            contenthtml.encoding='utf-8'
            lncontents=re.findall(r'<!--enpcontent--><p>(.+)</p><!--/enpcontent-->',contenthtml.text,flags=re.I)
            lncontent=re.sub(r'</p><p>','<br><br>',''.join(lncontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(lnlink,lnlink)
            print('辽宁日报 %s 正在上传 %s...'%(lncatname,lntitle))
            lncur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            lncur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            lncur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(lncontent,lntitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','辽宁日报-'+lntitle))[0:22]))))
            lncur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(lncur.lastrowid,lnsubcatid))
            lncur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(lnsubcatid,))
            print('辽宁日报 %s 完成上传 %s！'%(lncatname,lntitle))
    print('辽宁日报 获取最新文章完成！')
    conn.close()