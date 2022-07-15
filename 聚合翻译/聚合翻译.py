import os,re,sys,json,random,winreg,base64,js2py,hashlib,requests,threading,webbrowser
import tkinter as tk
class Tr:
    def __init__(self):
        self.dbt={'百度翻译':['bd'],'彩云翻译':['cy'],'谷歌翻译':['gg'],'搜狗翻译':['sg'],'有道翻译':['yd']}
        self.lock=threading.Lock()
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings')
        count=winreg.QueryInfoKey(key)[1]
        for i in range(count):
            name=winreg.EnumValue(key,i)[0]
            command=winreg.EnumValue(key,i)[1]
            if name=='ProxyEnable':
                proxyenable=command
            if name=='ProxyServer':
                if proxyenable==0:
                    self.proxyserver=''
                else:
                    self.proxyserver=command
        winreg.CloseKey(key)
    def Createtop(self,btname,bttext):
        try:
            exec("if not self.root%s.winfo_exists():\n\tself.Ntop(btname,bttext)"%btname)
        except:
            self.Ntop(btname,bttext)
    def Ntop(self,btname,bttext):
        exec("self.root%s=tk.Toplevel()"%btname)
        exec("self.root%s.iconbitmap(iicon)"%btname)
        exec("self.root%s.title(bttext)"%btname)
        exec("panel1=tk.Frame(self.root%s)"%btname)
        exec("xgd1=tk.Scrollbar(panel1,orient='horizontal')")
        exec("ygd1=tk.Scrollbar(panel1)")
        exec("xgd1.pack(side='bottom',fill='x')")
        exec("ygd1.pack(side='right',fill='y')")
        exec("self.text%s1=tk.Text(panel1,wrap='none',xscrollcommand=xgd1.set,yscrollcommand=ygd1.set)"%btname)
        exec("self.text%s1.pack(fill='both')"%btname)
        exec("panel1.pack(fill='both')")
        exec("xgd1.config(command=self.text%s1.xview)"%btname)
        exec("ygd1.config(command=self.text%s1.yview)"%btname)
        exec("panel2=tk.Frame(self.root%s)"%btname)
        exec("self.bt%sr=tk.Button(panel2,text='%s(%s)',font=('',16),command=lambda:self.Topr(None,btname))"%(btname,bttext,btname[0].title()),dict(locals(),**globals()))
        exec("self.bt%sr.pack(side='left')"%btname)
        exec("self.bt%sc=tk.Button(panel2,text='清屏',font=('',16),command=lambda:self.Topc(btname,bttext))"%btname,dict(locals(),**globals()))
        exec("self.bt%sc.pack(side='left')"%btname)
        exec("self.bt%so=tk.Button(panel2,text='复制原文',font=('',16),command=lambda:self.Topo(btname))"%btname,dict(locals(),**globals()))
        exec("self.bt%so.pack(side='left')"%btname)
        exec("self.bt%st=tk.Button(panel2,text='复制译文',font=('',16),command=lambda:self.Topt(btname))"%btname,dict(locals(),**globals()))
        exec("self.bt%st.pack(side='left')"%btname)
        exec("panel2.pack()")
        exec("panel3=tk.Frame(self.root%s)"%btname)
        exec("xgd2=tk.Scrollbar(panel3,orient='horizontal')")
        exec("ygd2=tk.Scrollbar(panel3)")
        exec("xgd2.pack(side='bottom',fill='x')")
        exec("ygd2.pack(side='right',fill='y')")
        exec("self.text%s2=tk.Text(panel3,wrap='none',xscrollcommand=xgd2.set,yscrollcommand=ygd2.set)"%btname)
        exec("self.text%s2.pack(fill='both')"%btname)
        exec("panel3.pack(fill='both')")
        exec("xgd2.config(command=self.text%s2.xview)"%btname)
        exec("ygd2.config(command=self.text%s2.yview)"%btname)
        exec("self.root%s.bind('<Alt-%s>',lambda event:self.Topr(None,btname))"%(btname,btname[0]),dict(locals(),**globals()))
    def Topr(self,event,btname):
        exec("threading.Thread(target=self.%sg,daemon=True).start()"%btname.title())
    def Bdg(self):
        self.btbdr.config(text='正在翻译...')
        strings=self.textbd1.get(1.0,'end').split('\n')
        for string in strings:
            if string=='':
                continue
            else:
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Cookie':'BAIDUID=4650B0B34048BBAA1E0B909B42F5A564:FG=1;BIDUPSID=4650B0B34048BBAA1E0B909B42F5A564;PSTM=1537177909;BDUSS=w0VmEzUFFWTTh0bld5VWVhNVo5MEEyV2ZKdTk3U2stMGZmWVQ1TTRuSnVkOHBiQVFBQUFBJCQAAAAAAAAAAAEAAAD0GzcNaG9uZ3F1YW4xOTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7qoltu6qJbTk;pgv_pvi=6774493184;uc_login_unique=19e6fd48035206a8abe89f98c3fc542a;uc_recom_mark=cmVjb21tYXJrXzYyNDU4NjM%3D;MCITY=-218%3A;cflag=15%3A3;SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02893452711;locale=zh;Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1539333192;from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D;REALTIME_TRANS_SWITCH=1;FANYI_WORD_SWITCH=1;HISTORY_SWITCH=1;SOUND_SPD_SWITCH=1;SOUND_PREFER_SWITCH=1;to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D;Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1539333307'}
                html=requests.get('https://fanyi.baidu.com',headers=headers,proxies={'http':self.proxyserver,'https':self.proxyserver})
                gtk=re.findall("window.gtk = '(.*?)';",html.text)[0]
                js=js2py.EvalJs()
                js.execute('function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}')
                sign=js.hash(string,gtk)
                token=re.findall("token: '(.+)',",html.text)[0]
                landata={'query':string}
                lanhtml=requests.post('https://fanyi.baidu.com/langdetect',data=landata,proxies={'http':self.proxyserver,'https':self.proxyserver})
                lan=lanhtml.json()['lan']
                if lan=='zh':
                    to='en'
                else:
                    to='zh'
                data={'from':lan,'to':to,'query':string,'sign':'%s'%sign,'token':'%s'%token}
                resp=requests.post('https://fanyi.baidu.com/v2transapi',data=data,headers=headers,proxies={'http':self.proxyserver,'https':self.proxyserver})
                result=resp.json()['trans_result']['data'][0]['dst']+'\n'
                self.textbd2.insert('end',result)
        self.textbd2.delete(self.textbd2.index('end-1c'),'end')
        self.btbdr.config(text='翻译完成')
        self.btbd.config(text='翻译完成')
        try:
            self.lock.acquire()
            self.boolnum+=1
            self.lock.release()
        except:
            pass
    def Cyg(self):
        self.btcyr.config(text='正在翻译...')
        strings=(self.textcy1.get(1.0,'end')).split('\n')
        for string in strings:
            if string=='':
                continue
            else:
                encrypt=hashlib.md5()
                encrypt.update(''.join(random.choices('qweasdzxcrtyfghvbnuiopjklm1234567890',k=10)).encode())
                brower_id=encrypt.hexdigest()
                authdata={'browser_id':brower_id}
                authdata=json.dumps(authdata)
                authheaders={'X-Authorization':'token:qgemv4jr1y38jyq6vhvi','Content-Type':'application/json;charset=UTF-8'}
                html=requests.post('https://api.interpreter.caiyunai.com/v1/user/jwt/generate',data=authdata,headers=authheaders,proxies={'http':self.proxyserver,'https':self.proxyserver})
                auth=html.json()['jwt']
                landata={'query':string}
                lanhtml=requests.post('https://fanyi.baidu.com/langdetect',data=landata,proxies={'http':self.proxyserver,'https':self.proxyserver})
                lan=lanhtml.json()['lan']
                if lan=='zh':
                    to='en'
                else:
                    to='zh'
                data={'browser_id':brower_id,'detect':'true','source':string,'trans_type':'auto2%s'%to}
                data=json.dumps(data)
                headers={'T-Authorization':auth}
                resp=requests.post('https://api.interpreter.caiyunai.com/v1/translator',data=data,headers=headers,proxies={'http':self.proxyserver,'https':self.proxyserver})
                preresult=json.loads(resp.text)['target']
                t='NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
                o='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                s=[]
                for i in list(preresult):
                    index=o.find(i)
                    if index>-1:
                        s.append(t[index])
                    else:
                        s.append(i)
                result=base64.b64decode(''.join(s)).decode('utf-8')+'\n'
                self.textcy2.insert('end',result)
        self.textcy2.delete(self.textcy2.index('end-1c'),'end')
        self.btcyr.config(text='翻译完成')
        self.btcy.config(text='翻译完成')
        try:
            self.lock.acquire()
            self.boolnum+=1
            self.lock.release()
        except:
            pass
    def Ggg(self):
        self.btggr.config(text='正在翻译...')
        strings=(self.textgg1.get(1.0,'end')).split('\n')
        for string in strings:
            if string=='':
                continue
            else:
                landata={'query':string}
                lanhtml=requests.post('https://fanyi.baidu.com/langdetect',data=landata,proxies={'http':self.proxyserver,'https':self.proxyserver})
                lan=lanhtml.json()['lan']
                if lan=='zh':
                    to='en'
                else:
                    to='zh-CN'
                url='https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
                data={'f.req':r'[[["MkEWBc","[[\"%s\",\"auto\",\"%s\",true],[null]]",null,"generic"]]]'%(string,to)}
                resp=requests.post(url,data=data,proxies={'http':self.proxyserver,'https':self.proxyserver})
                result=re.findall(r'null,\[\[\\"(.+?)\\",null,null,null',resp.text)[0]+'\n'
                self.textgg2.insert('end',result)
        self.textgg2.delete(self.textgg2.index('end-1c'),'end')
        self.btggr.config(text='翻译完成')
        self.btgg.config(text='翻译完成')
        try:
            self.lock.acquire()
            self.boolnum+=1
            self.lock.release()
        except:
            pass
    def Sgg(self):
        self.btsgr.config(text='正在翻译...')
        strings=(self.textsg1.get(1.0,'end')).split('\n')
        for string in strings:
            if string=='':
                continue
            else:
                fsheaders={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;''q=0.9,image/webp,image/apng,*/*;''q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
                html=requests.get('https://fanyi.sogou.com',headers=fsheaders,proxies={'http':self.proxyserver,'https':self.proxyserver})
                FUV=html.cookies.get_dict()['FUV']
                SNUID=html.cookies.get_dict()['SNUID']
                landata={'query':string}
                lanhtml=requests.post('https://fanyi.baidu.com/langdetect',data=landata,proxies={'http':self.proxyserver,'https':self.proxyserver})
                lan=lanhtml.json()['lan']
                if lan=='zh':
                    lan='zh-CHS'
                    to='en'
                else:
                    to='zh-CHS'
                sign=lan+to+string+'109984457'
                m=hashlib.md5()
                m.update(sign.encode('utf-8'))
                data={'from':lan,'s':m.hexdigest(),'text':string,'to':to}
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;''q=0.9,image/webp,image/apng,*/*;''q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8','Cookie':'FUV=%s;SNUID=%s'%(FUV,SNUID)}
                resp=requests.post('https://fanyi.sogou.com/api/transpc/text/result',data=data,headers=headers,proxies={'http':self.proxyserver,'https':self.proxyserver})
                result=resp.json()['data']['translate']['dit']+'\n'
                self.textsg2.insert('end',result)
        self.textsg2.delete(self.textsg2.index('end-1c'),'end')
        self.btsgr.config(text='翻译完成')
        self.btsg.config(text='翻译完成')
        try:
            self.lock.acquire()
            self.boolnum+=1
            self.lock.release()
        except:
            pass
    def Ydg(self):
        self.btydr.config(text='正在翻译...')
        strings=(self.textyd1.get(1.0,'end')).split('\n')
        for string in strings:
            if string=='':
                continue
            else:
                data={'doctype':'json','i':string}
                resp=requests.post('http://fanyi.youdao.com/translate',data=data,proxies={'http':self.proxyserver,'https':self.proxyserver})
                result=resp.json()['translateResult'][0][0]['tgt']+'\n'
                self.textyd2.insert('end',result)
        self.textyd2.delete(self.textyd2.index('end-1c'),'end')
        self.btydr.config(text='翻译完成')
        self.btyd.config(text='翻译完成')
        try:
            self.lock.acquire()
            self.boolnum+=1
            self.lock.release()
        except:
            pass
    def Topc(self,btname,bttext):
        exec("self.text%s1.delete(1.0,'end')"%btname)
        exec("self.text%s2.delete(1.0,'end')"%btname)
        exec("self.bt%sr.config(text='%s(%s)')"%(btname,bttext,btname[0].title()))
        exec("self.bt%s.config(text=bttext)"%btname)
    def Topo(self,btname):
        exec("self.text%s1.clipboard_clear()"%btname)
        exec("self.text%s1.clipboard_append(self.text%s1.get(1.0,'end').strip())"%(btname,btname))
    def Topt(self,btname):
        exec("self.text%s2.clipboard_clear()"%btname)
        exec("self.text%s2.clipboard_append(self.text%s2.get(1.0,'end').strip())"%(btname,btname))
    def Fy(self,event):
        self.btjh.config(text='正在翻译...')
        self.boolnum=self.countnum=0
        for key,value in self.dbt.items():
            if value[1].get()==True:
                exec("self.bt%s.config(text='正在翻译...')"%value[0])
                self.countnum+=1
                self.Createtop(value[0],key)
                exec("self.text%s1.insert('end',self.textjh.get(1.0,'end').strip())"%value[0])
                self.Topr(None,value[0])
                self.done()
    def done(self):
        loop=self.root.after(100,self.done)
        if self.boolnum==self.countnum:
            self.btjh.config(text='翻译完成')
            self.root.after_cancel(loop)
    def Clear(self,event):
        for key,value in self.dbt.items(): 
            try:
                exec("self.text%s1.delete(1.0,'end')"%value[0])
                exec("self.text%s2.delete(1.0,'end')"%value[0])
                exec("self.bt%sr.config(text='%s(%s)')"%(value[0],key,value[0][0].title()))
            except:
                pass
        self.textjh.delete(1.0,'end')
        self.btbd.config(text='百度翻译')
        self.btcy.config(text='彩云翻译')
        self.btgg.config(text='谷歌翻译')
        self.btsg.config(text='搜狗翻译')
        self.btyd.config(text='有道翻译')
        self.btjh.config(text='聚合翻译(A)')
    def callback(self):
        self.root.withdraw()
    def menuf(self,event,x,y):
        if event=='WM_RBUTTONDOWN':
            self.menu.tk_popup(x,y)
        if event=='WM_LBUTTONDOWN':
            self.root.deiconify()
        if event=='WM_MBUTTONDOWN':
            self.root.withdraw()
    def about(self):
        webbrowser.open('https://github.com/mefunc/cpy',new=0)
    def allquit(self):
        self.root.call('winico','taskbar','delete',self.icon)
        self.root.quit()
    def Root(self):
        self.root=tk.Tk()
        self.root.iconbitmap(iicon)
        self.root.title('聚合翻译')
        self.root.protocol("WM_DELETE_WINDOW",self.callback)
        self.root.call('package','require','Winico')
        self.icon=self.root.call('winico','createfrom',iicon)
        self.root.call('winico','taskbar','add',self.icon,'-callback',(self.root.register(self.menuf),'%m','%x','%y'),'-pos',0,'-text',u'聚合翻译')
        self.menu=tk.Menu(self.root,tearoff=0)
        self.menu.add_command(label=u'显示主页面',command=self.root.deiconify)
        self.menu.add_command(label=u'关于',command=self.about)
        self.menu.add_command(label=u'隐藏主页面',command=self.root.withdraw)
        self.menu.add_command(label=u'退出',command=self.allquit)
        panel1=tk.Frame(self.root)
        xgd=tk.Scrollbar(panel1,orient='horizontal')
        ygd=tk.Scrollbar(panel1)
        xgd.pack(side='bottom',fill='x')
        ygd.pack(side='right',fill='y')
        self.textjh=tk.Text(panel1,wrap='none',xscrollcommand=xgd.set,yscrollcommand=ygd.set)
        self.textjh.pack(fill='both',expand=1)
        panel1.pack(fill='both',expand=1)
        xgd.config(command=self.textjh.xview)
        ygd.config(command=self.textjh.yview)
        panel2=tk.Frame(self.root)
        self.btjh=tk.Button(panel2,text='聚合翻译(A)',font=('',16),command=lambda:self.Fy(None))
        self.btjh.pack(side='left')
        panel2.pack()
        panel3=tk.Frame(self.root)
        tk.Button(panel3,text='清屏(C)',font=('',16),command=lambda:self.Clear(None)).pack(side='left')
        panel3.pack()
        for text,value in self.dbt.items():
            name=value[0]
            self.dbt[text].append(tk.BooleanVar())
            if text in ['彩云翻译','谷歌翻译']:
                self.dbt[text][1].set(True)
            tk.Checkbutton(panel2,text=text,font=('',12),variable=self.dbt[text][1]).pack(side='left')
            exec("self.bt%s=tk.Button(panel3,text=text,font=('',16),command=lambda:self.Createtop(name,text))"%name,dict(locals(),**globals()))
            exec("self.bt%s.pack(side='left')"%name)
        self.root.bind('<Alt-a>',self.Fy)
        self.root.bind('<Alt-c>',self.Clear)
        self.root.mainloop()
if getattr(sys,'frozen',False):
        odir=sys._MEIPASS
else:
    odir=os.path.dirname(os.path.abspath(__file__))
iicon=os.path.join(odir,'聚合翻译.ico')
Tr().Root()