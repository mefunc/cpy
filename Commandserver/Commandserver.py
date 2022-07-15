import tkinter as tk
import os,sys,traceback,subprocess,webbrowser
from threading import Thread
from urllib.parse import unquote_plus
from http.server import HTTPServer,BaseHTTPRequestHandler
class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html;charset=utf-8")
        self.end_headers()
        cliproot=tk.Toplevel()
        try:
            clipstring=cliproot.clipboard_get().replace('\n','')
        except:
            clipstring=''
        cliproot.destroy()
        buf='''
        <!DOCTYPE HTML>
        <html>
        <head>
            <title>Commandserver</title>
        </head>
        <body>
            <form id="commandform" action="result" method="post" target="_blank">
                命令输入框：<br><textarea name="commandinput" rows="10" cols="100"></textarea><br>
                <input type="submit" value="执行" style="width: 100px;height: 50px" /><button type="button" onclick="Clear()" style="width: 100px;height: 50px">清除</button><br>
                快捷命令：<button type="button" onclick="Copy()" style="width: 100px;height: 50px">复制到剪贴板</button><button type="button" onclick="Paste()" style="width: 100px;height: 50px">从剪贴板粘贴</button><button type="button" onclick="Shutdown()" style="width: 100px;height: 50px">关机</button><button type="button" onclick="Reboot()" style="width: 100px;height: 50px">重启</button>
            </form>
            <script type="text/javascript">
                var commandform=document.getElementById("commandform"),
                    commandinput=document.getElementsByName("commandinput")[0];
                function Clear() {
                    commandinput.value="";
                }
                function Copy() {
                    commandinput.value="echo "+commandinput.value+"|clip";
                    commandform.submit();
                }
                function Paste() {
                    commandinput.value="%s";
                }
                function Shutdown() {
                    commandinput.value="shutdown /s /f /t 0";
                    commandform.submit();
                }
                function Reboot() {
                    commandinput.value="shutdown /r /f /t 0";
                    commandform.submit();
                }
            </script>
        </body>
        </html>
        '''%clipstring
        self.wfile.write(buf.encode())
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type","text/html;charset=utf-8")
        self.end_headers()
        datas=unquote_plus(self.rfile.read(int(self.headers['content-length'])).decode())
        command=datas[datas.find('=')+1:len(datas)]
        htmlstart='''
        <!DOCTYPE HTML>
        <html>
            <head>
                <title>执行结果</title>
            </head>
            <body>
                命令：%s<br>结果：
        '''%command
        self.wfile.write(htmlstart.encode())
        try:
            execresult=subprocess.Popen(command,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            while execresult.poll()==None:
                result=execresult.stdout.readline().decode('gbk')
                htmlresult='''
                <br>%s
                '''%result
                self.wfile.write(htmlresult.encode())
        except:
            htmlresult='''
                <br>%s
            '''%traceback.format_exc()
            self.wfile.write(htmlresult.encode())
        htmlend='''
            </body>
        </html>
        '''
        self.wfile.write(htmlend.encode())
class Commandserver:
    def __init__(self):
        self.flag=True
        self.ip=self.Queryip()
    def Queryip(self):
        os.system('ipconfig>ip.txt')
        with open('ip.txt') as tmps:
            for tmp in tmps:
                if 'IPv4 地址' in tmp:
                    ip=tmp[tmp.rfind(' ')+1:len(tmp)].strip()
        os.remove('ip.txt')
        return ip
    def Control(self):
        if self.flag:
            if self.varcport.get():
                self.port=self.vareport.get()
            else:
                self.port=8888
            self.varlip.set(self.ip+':'+str(self.port))
            host=(self.ip,self.port)
            self.server=HTTPServer(host,Resquest)
            Thread(target=self.server.serve_forever,daemon=True).start()
            self.bc.config(text='关闭服务器')
            self.flag=False
        else:
            self.server.shutdown()
            self.server.server_close()
            self.bc.config(text='开启服务器')
            self.flag=True
    def Changeport(self):
        if self.varcport.get():
            self.eport.config(state='normal')
        else:
            self.eport.config(state='disabled')
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
        try:
            self.server.shutdown()
            self.server.server_close()
        except:
            pass
        self.root.call('winico','taskbar','delete',self.icon)
        self.root.quit()
    def Root(self):
        self.root=tk.Tk()
        self.root.iconbitmap(iicon)
        self.root.title('Commandserver')
        self.root.protocol("WM_DELETE_WINDOW",self.callback)
        self.root.call('package','require','Winico')
        self.icon=self.root.call('winico','createfrom',iicon)
        self.root.call('winico','taskbar','add',self.icon,'-callback',(self.root.register(self.menuf),'%m','%x','%y'),'-pos',0,'-text',u'Commandserver')
        self.menu=tk.Menu(self.root,tearoff=0)
        self.menu.add_command(label=u'显示主页面',command=self.root.deiconify)
        self.menu.add_command(label=u'关于',command=self.about)
        self.menu.add_command(label=u'隐藏主页面',command=self.root.withdraw)
        self.menu.add_command(label=u'退出',command=self.allquit)
        self.varlip=tk.StringVar()
        self.varlip.set(self.ip+':8888')
        tk.Label(self.root,textvariable=self.varlip,font=('',25)).pack(expand=1)
        panelport=tk.Frame(self.root)
        self.bc=tk.Button(panelport,text='开启服务器',font=('',16),command=self.Control)
        self.bc.pack(side='left')
        self.varcport=tk.BooleanVar()
        tk.Checkbutton(panelport,text='自定义端口',font=('',16),variable=self.varcport,command=self.Changeport).pack(side='left')
        self.vareport=tk.IntVar()
        self.vareport.set(8888)
        self.eport=tk.Entry(panelport,state='disabled',textvariable=self.vareport,font=('',16),width=8)
        self.eport.pack(side='left')
        panelport.pack(expand=1)
        self.root.mainloop()
if getattr(sys,'frozen',False):
    odir=sys._MEIPASS
else:
    odir=os.path.dirname(os.path.abspath(__file__))
iicon=os.path.join(odir,'Commandserver.ico')
Commandserver().Root()