import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    hljcur=conn.cursor()
    dpaper={}
    hljcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in hljcur:
        dpaper[name]=term_id
    hljcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '黑龙江日报' not in dpaper:
        print('未找到 黑龙江日报 分类，正在新建 黑龙江日报 分类...')
        hljcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("黑龙江日报",quote("黑龙江日报")))
        hljpid=hljcur.lastrowid
        hljcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(hljpid,hljpid,dpaper['日报']))
        hljcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('黑龙江日报 分类建立完成！')
    else:
        print('黑龙江日报 正在删除原有文章...')
        hljpid=dpaper['黑龙江日报']
        hljcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(hljpid,))
        hljcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(hljpid,))
        hljcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(hljpid,))
        hljcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('黑龙江日报 删除原有文章完成！')
    print('黑龙江日报 正在获取最新文章...')
    cathtml=Getproxy().Parserget('http://epaper.hljnews.cn/hljrb/pc/layout/index.html')
    cathtml.encoding='utf-8'
    hljcats=re.findall(r'<a href="(.+)" target="_blank">\s+.+\s+<br/>\s+(.+?)\s+</a>',cathtml.text)
    for hljcat in hljcats:
        hljcatname=hljcat[1].replace('版 ','版：')
        hljcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(hljcatname,quote(re.sub(r'\s+','-',(hljcat[1]+'-黑龙江日报').replace('版 ','版：'))[0:22])))
        hljsubcatid=hljcur.lastrowid
        hljcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(hljsubcatid,hljsubcatid,hljpid))
        hljcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://epaper.hljnews.cn/hljrb/pc/layout/%s'%hljcat[0])
        tlshtml.encoding='utf-8'
        hljtls=re.findall(r'<h3><a href="(.+)">(.+)</a></h3>',tlshtml.text)
        for hljtl in hljtls:
            hljtitle=hljtl[1]
            hljlink='http://epaper.hljnews.cn/hljrb/pc/%s'%hljtl[0].replace('../','')
            contenthtml=Getproxy().Parserget(hljlink)
            contenthtml.encoding='utf-8'
            hljcontents=re.findall(r'<!--enpcontent--><p>(.+)</p><!--/enpcontent-->',contenthtml.text,flags=re.I)
            hljcontent=re.sub(r'</p><p>','<br><br>',''.join(hljcontents),flags=re.I)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(hljlink,hljlink)
            print('黑龙江日报 %s 正在上传 %s...'%(hljcatname,hljtitle))
            hljcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            hljcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            hljcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(hljcontent,hljtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','黑龙江日报-'+hljtitle))[0:22]))))
            hljcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(hljcur.lastrowid,hljsubcatid))
            hljcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(hljsubcatid,))
            print('黑龙江日报 %s 完成上传 %s！'%(hljcatname,hljtitle))
    print('黑龙江日报 获取最新文章完成！')
    conn.close()