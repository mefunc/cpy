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
    daydate='%d-%02d-%02d'%(nyear,nmonth,nday)
    conn=configok()[2]
    jfcur=conn.cursor()
    dpaper={}
    jfcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in jfcur:
        dpaper[name]=term_id
    jfcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '解放日报' not in dpaper:
        print('未找到 解放日报 分类，正在新建 解放日报 分类...')
        jfcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("解放日报",quote("解放日报")))
        jfpid=jfcur.lastrowid
        jfcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jfpid,jfpid,dpaper['日报']))
        jfcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('解放日报 分类建立完成！')
    else:
        print('解放日报 正在删除原有文章...')
        jfpid=dpaper['解放日报']
        jfcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jfpid,))
        jfcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(jfpid,))
        jfcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(jfpid,))
        jfcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('解放日报 删除原有文章完成！')
    print('解放日报 正在获取最新文章...')
    cathtml=Getproxy().Parserget('https://www.jfdaily.com/staticsg/data/journal/%s/navi.json'%daydate)
    jfcats=re.findall(r'"pname":"(.+?)".+?"id":(\d+),"pnumber":"(\d+)"',cathtml.text)
    jftls=re.findall(r'"pid":(\d+),"id":(\d+).+?"title":"(.+?)"',cathtml.text)
    for jfcat in jfcats:
        jfcatname=jfcat[2]+'版：'+jfcat[0]
        jfcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(jfcatname,quote(re.sub(r'\s+','-',jfcatname+'-解放日报')[0:22])))
        jfsubcatid=jfcur.lastrowid
        jfcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(jfsubcatid,jfsubcatid,jfpid))
        jfcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        for jftl in jftls:
            if jftl[0]==jfcat[1]:
                jftitle=jftl[2]
                jflink='https://www.jfdaily.com/staticsg/data/journal/%s/%s/article/%s.json'%(daydate,jfcat[2],jftl[1])
                jfrefer='https://www.jfdaily.com/staticsg/res/html/journal/detail.html?date=%s&id=%s&page=%s'%(daydate,jftl[1],jfcat[2])
                contenthtml=Getproxy().Parserget(jflink)
                contenthtml.encoding='utf-8'
                jfcontent=contenthtml.json()['article']['content']+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(jfrefer,jfrefer)
                print('解放日报 %s 正在上传 %s...'%(jfcatname,jftitle))
                jfcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
                jfcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
                jfcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(jfcontent,jftitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','解放日报-'+jftitle))[0:22]))))
                jfcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(jfcur.lastrowid,jfsubcatid))
                jfcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(jfsubcatid,))
                print('解放日报 %s 完成上传 %s！'%(jfcatname,jftitle))
    print('解放日报 获取最新文章完成！')
    conn.close()