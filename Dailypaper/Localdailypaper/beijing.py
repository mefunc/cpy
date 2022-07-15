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
    daydate='%d/%d%02d%02d'%(nyear,nyear,nmonth,nday)
    conn=configok()[2]
    bjcur=conn.cursor()
    dpaper={}
    bjcur.execute('SELECT term_id,name FROM wp_terms;')
    for term_id,name in bjcur:
        dpaper[name]=term_id
    bjcur.execute('ALTER TABLE wp_terms MODIFY COLUMN slug longtext;')
    if '北京日报' not in dpaper:
        print('未找到 北京日报 分类，正在新建 北京日报 分类...')
        bjcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',("北京日报",quote("北京日报")))
        bjpid=bjcur.lastrowid
        bjcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(bjpid,bjpid,dpaper['日报']))
        bjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('北京日报 分类建立完成！')
    else:
        print('北京日报 正在删除原有文章...')
        bjpid=dpaper['北京日报']
        bjcur.execute('DELETE wp_posts,wp_term_relationships FROM wp_posts,wp_term_relationships WHERE wp_posts.ID=wp_term_relationships.object_id AND wp_term_relationships.term_taxonomy_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(bjpid,))
        bjcur.execute('DELETE FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE parent=?);',(bjpid,))
        bjcur.execute('DELETE FROM wp_term_taxonomy WHERE parent=?;',(bjpid,))
        bjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        print('北京日报 删除原有文章完成！')
    print('北京日报 正在获取最新文章...')
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36'}
    indexhtml=Getproxy().Parserget('https://bjrbdzb.bjd.com.cn/bjrb/paperindex.htm',headers=headers)
    cattlshtml=Getproxy().Parserget('https://bjrbdzb.bjd.com.cn/bjrb/'+re.findall(r'href="(.+)"',indexhtml.text)[0].replace('./',''),headers=headers)
    cattlshtml.encoding='utf-8'
    bjcats=re.findall(r'pdf_href=.+>(.+)</div>',cattlshtml.text)
    bjtls=re.findall(r'data-href="(.+)">(.+)</a>',cattlshtml.text)
    for bjcat in bjcats:
        bjcur.execute('INSERT INTO wp_terms(name,slug) VALUES(?,?);',(bjcat,quote(re.sub(r'\s+','-',(bjcat+'-北京日报').replace(':',''))[0:22])))
        bjsubcatid=bjcur.lastrowid
        bjcur.execute('INSERT INTO wp_term_taxonomy(term_taxonomy_id,term_id,taxonomy,description,parent) VALUES(?,?,"category","",?);',(bjsubcatid,bjsubcatid,bjpid))
        bjcur.execute('UPDATE wp_options SET option_value="" WHERE option_name="category_children";')
        for bjtl in bjtls:
            if int(bjtl[0][bjtl[0].find('page')+4:len(bjtl[0])])==int(bjcat[bjcat.find('第')+1:bjcat.find('版')])-1:
                bjtitle=bjtl[1]
                bjlink='https://bjrbdzb.bjd.com.cn/bjrb/mobile/%s/%s'%(daydate,bjtl[0].replace('./',''))
                contenthtml=Getproxy().Parserget(bjlink,headers=headers)
                contenthtml.encoding='utf-8'
                bjcontents=re.findall(r'<P>([^/]+)</P>',contenthtml.text,flags=re.I)
                bjcontent='<br><br>'.join(bjcontents)+'<br><br><strong>来源：<a href="%s" target="_blank">%s</a></strong>'%(bjlink,bjlink)
                print('北京日报 %s 正在上传 %s...'%(bjcat,bjtitle))
                bjcur.execute('ALTER TABLE wp_posts MODIFY COLUMN post_name longtext;')
                bjcur.execute('SELECT ID FROM wp_posts ORDER BY ID DESC LIMIT 1;')
                bjcur.execute('INSERT INTO wp_posts(post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered) VALUES(1,now(),DATE_ADD(now(),INTERVAL "-8" HOUR),?,?,"","publish",?,"","",now(),DATE_ADD(now(),INTERVAL "-8" HOUR),"");',(bjcontent,bjtitle,re.sub(r'-+$','',quote(re.sub(r'\s+|\.','-',re.sub(r'<br>|:|%','','北京日报-'+bjtitle))[0:22]))))
                bjcur.execute('INSERT INTO wp_term_relationships(object_id,term_taxonomy_id) VALUES(?,?);',(bjcur.lastrowid,bjsubcatid))
                bjcur.execute('UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id=?;',(bjsubcatid,))
                print('北京日报 %s 完成上传 %s！'%(bjcat,bjtitle))
    print('北京日报 获取最新文章完成！')
    conn.close()