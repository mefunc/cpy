import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    xhcur=conn.cursor()
    dpaper={}
    xhcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in xhcur:
        dpaper[name]=term_id
    xhcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '新华日报' not in dpaper:
        print('未找到 新华日报 分类，正在新建 新华日报 分类...')
        xhcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("新华日报",quote("新华日报")))
        xhpid=xhcur.lastrowid
        xhcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(xhpid,xhpid,dpaper['日报']))
        xhcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('新华日报 分类建立完成！')
    else:
        print('新华日报 正在删除原有文章...')
        xhpid=dpaper['新华日报']
        xhcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(xhpid,))
        xhcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(xhpid,))
        xhcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(xhpid,))
        xhcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('新华日报 删除原有文章完成！')
    print('新华日报 正在获取最新文章...')
    indexhtml=Getproxy().Parserget('http://xh.xhby.net')
    cathtml=Getproxy().Parserget(re.findall(r'window.location.href="(.+)"',indexhtml.text)[1])
    cathtml.encoding='utf-8'
    xhcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for xhcat in xhcats:
        xhcatname=xhcat[1].replace('版 ','版：')
        xhcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(xhcatname,quote(re.sub(r'\s+','-',(xhcat[1]+'-新华日报').replace('版 ','版：'))[0:22])))
        xhsubcatid=xhcur.lastrowid
        xhcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(xhsubcatid,xhsubcatid,xhpid))
        xhcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://xh.xhby.net/pc/layout/%s'%xhcat[0])
        tlshtml.encoding='utf-8'
        xhtls=re.findall(r'<h3><a href="(.+)"\s+>(.+)</a></h3>',tlshtml.text)
        for xhtl in xhtls:
            xhtitle=xhtl[1]
            xhlink='http://xh.xhby.net/pc/%s'%xhtl[0].replace('../','')
            contenthtml=Getproxy().Parserget(xhlink)
            contenthtml.encoding='utf-8'
            xhcontents=re.findall(r'<!--enpcontent--><p>(.+)</p><!--/enpcontent-->',contenthtml.text,flags=re.I)
            xhcontent=re.sub(r'</p><p>','<br><br>',''.join(xhcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(xhlink,xhlink)
            print('新华日报 %s 正在上传 %s...'%(xhcatname,xhtitle))
            xhcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            xhcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            xhcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(xhcontent,xhtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','新华日报-'+xhtitle))[0:22]))))
            xhcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(xhcur.lastrowid,xhsubcatid))
            xhcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(xhsubcatid,))
            print('新华日报 %s 完成上传 %s！'%(xhcatname,xhtitle))
    print('新华日报 获取最新文章完成！')
    conn.close()