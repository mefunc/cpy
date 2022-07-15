import re
from iniconfig import configok
from urllib.parse import quote
from proxyparse import Getproxy
def Upload():
    conn=configok()[2]
    sxcur=conn.cursor()
    dpaper={}
    sxcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in sxcur:
        dpaper[name]=term_id
    sxcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '山西日报' not in dpaper:
        print('未找到 山西日报 分类，正在新建 山西日报 分类...')
        sxcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("山西日报",quote("山西日报")))
        sxpid=sxcur.lastrowid
        sxcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(sxpid,sxpid,dpaper['日报']))
        sxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('山西日报 分类建立完成！')
    else:
        print('山西日报 正在删除原有文章...')
        sxpid=dpaper['山西日报']
        sxcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(sxpid,))
        sxcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(sxpid,))
        sxcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(sxpid,))
        sxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('山西日报 删除原有文章完成！')
    print('山西日报 正在获取最新文章...')
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36'}
    cathtml=Getproxy().Parserget('http://epaper.sxrb.com/index.shtml',headers=headers)
    sxcats=re.findall(r'<a href="(.+)" target="_top">(.+)</a>',cathtml.text)
    for sxcat in sxcats:
        sxcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(sxcat[1],quote(re.sub(r'\s+','-',(sxcat[1]+'-山西日报').replace(':',''))[0:22])))
        sxsubcatid=sxcur.lastrowid
        sxcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(sxsubcatid,sxsubcatid,sxpid))
        sxcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        tlshtml=Getproxy().Parserget('http://epaper.sxrb.com%s'%sxcat[0],headers=headers)
        sxtls=re.findall(r'<a href="(.+)"  target="_top" title="(.*?)"',tlshtml.text)
        for sxtl in sxtls:
            sxtitle=sxtl[1]
            sxlink='http://epaper.sxrb.com%s'%sxtl[0]
            contenthtml=Getproxy().Parserget(sxlink,headers=headers)
            sxcontent=re.findall(r'<div class="details">\s+(.+?)\s+</div>',contenthtml.text,flags=re.S)[0]+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(sxlink,sxlink)
            print('山西日报 %s 正在上传 %s...'%(sxcat[1],sxtitle))
            sxcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
            sxcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
            sxcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(sxcontent,sxtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','山西日报-'+sxtitle))[0:22]))))
            sxcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(sxcur.lastrowid,sxsubcatid))
            sxcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(sxsubcatid,))
            print('山西日报 %s 完成上传 %s！'%(sxcat[1],sxtitle))
    print('山西日报 获取最新文章完成！')
    conn.close()