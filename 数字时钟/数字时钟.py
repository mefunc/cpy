import os,sys,time,winsound,webbrowser
import tkinter as tk
from tkinter import ttk,messagebox
from lunardate import SolarLunarCalendar
class Dc:
    def __init__(self):
        self.countnum=0
        self.aenum=1
        self.dalarm={}
    def settime(self):
        year,month,day,weekindex=time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'),int(time.strftime('%w'))
        dweek={1:'星期一',2:'星期二',3:'星期三',4:'星期四',5:'星期五',6:'星期六',0:'星期日'}
        week=dweek[weekindex]
        nl=SolarLunarCalendar('%s-%s-%s'%(year,month,day))
        nlyear,nlanimal,nlmonth,nlday=nl[0],nl[1],nl[2],nl[3]
        today=year+'年'+month+'月'+day+'日'+week
        todaynl='%s(%s)年%s%s%s'%(nlyear,nlanimal,nlmonth,nlday,week)
        curtime=time.strftime('%H:%M:%S')
        self.vartodaynl.set(todaynl)
        self.vartoday.set(today)
        self.varcurtime.set(curtime)
        self.root.after(1000,self.settime)
    def attr(self,v):
        self.root.attributes('-alpha',v)
    def Attr(self):
        atw=tk.Toplevel()
        atw.iconbitmap(iicon)
        atw.title('透明度设置')
        sc=tk.Scale(atw,from_=0,to=1,resolution=0.01,orient='horizontal',command=self.attr,length=230,label='当前透明度（0完全透明，1完全不透明）：')
        sc.set(1)
        sc.pack(expand=1)
    def cancelalarm(self):
        try:
            for i in self.treeam.selection():
                name=self.treeam.item(i)['text']
                self.treeam.delete(i)
                self.dalarm.pop(name)
        except:
            pass
    def rinws(self,aenum):
        winsound.PlaySound(None,winsound.SND_FILENAME)
        exec("self.ewi%s.after_cancel(self.rin2%s)"%(aenum,aenum))
        exec("self.varmsg%s.set('')"%aenum)
        exec("self.ertbt1%s.config(text='设定闹钟',command=lambda:self.rinb(aenum))"%aenum,dict(locals(),**globals()))
        self.cancelalarm()
    def rinw(self,aenum):
        exec("self.varmsg%s.set('正在响铃，请及时关闭闹钟！')"%aenum)
        exec("ahour,amin,asec=self.hour%s,self.min%s,self.sec%s"%(aenum,aenum,aenum))
        exec("adhour,admin,adsec='%.2d'%(int(ahour)),'%.2d'%(int(amin)),'%.2d'%(int(asec))")
        exec("self.varhour%s.set(adhour)"%aenum)
        exec("self.varmin%s.set(admin)"%aenum)
        exec("self.varsec%s.set(adsec)"%aenum)
        exec("self.ertbt1%s.config(text='关闭闹钟',command=lambda:self.rinws(aenum))"%aenum,dict(locals(),**globals()))
        winsound.PlaySound(isound,winsound.SND_FILENAME|winsound.SND_NOSTOP|winsound.SND_ASYNC)
        if self.n<6:
            self.n+=1
            exec("self.rin2%s=self.ewi%s.after(10250,lambda:self.rinw(aenum))"%(aenum,aenum),dict(locals(),**globals()))
        else:
            self.n=1
            exec("self.rin2%s=self.ewi%s.after(300250,lambda:self.rinw(aenum))"%(aenum,aenum),dict(locals(),**globals()))
    def rup(self,aenum):
        thour,tmin,tsec=int(time.strftime('%H')),int(time.strftime('%M')),int(time.strftime('%S'))
        exec("ahour,amin,asec=self.hour%s,self.min%s,self.sec%s"%(aenum,aenum,aenum))
        exec("adhour,admin,adsec='%.2d'%(int(ahour)),'%.2d'%(int(amin)),'%.2d'%(int(asec))")
        exec("if self.hour%s==thour and self.min%s==tmin and self.sec%s==tsec:\n\tself.n=1\n\tself.rinw(aenum)\nelse:\n\tself.varhour%s.set(adhour)\n\tself.varmin%s.set(admin)\n\tself.varsec%s.set(adsec)\n\tself.rin1%s=self.ewi%s.after(100,lambda:self.rup(aenum))"%((aenum,)*8),dict(locals(),**globals()))
    def rins(self,aenum):
        exec("self.ewi%s.after_cancel(self.rin1%s)"%(aenum,aenum))
        exec("self.varmsg%s.set('')"%aenum)
        exec("self.ertbt1%s.config(text='设定闹钟',command=lambda:self.rinb(aenum))"%aenum,dict(locals(),**globals()))
        self.cancelalarm()
    def rinb(self,aenum):
        if self.formaterr(aenum):
            exec("self.varmsg%s.set('闹钟已设定')"%aenum)
            exec("self.ertbt1%s.config(text='取消设定',command=lambda:self.rins(aenum))"%aenum,dict(locals(),**globals()))
            self.rup(aenum)
    def alarms(self,aenum):
        exec("if self.varmsg%s.get()=='闹钟已设定':\n\tself.alarmrs(aenum)\nelse:self.varmsg%s.set('未设定闹钟，先设定闹钟再保存！')"%(aenum,aenum))
    def alarmrs(self,aenum):
        self.ras=tk.Tk()
        self.ras.iconbitmap(iicon)
        self.ras.title('保存闹钟')
        tk.Label(self.ras,text='输入闹钟名称:',font=('',16)).pack()
        self.eas=tk.Entry(self.ras,font=('',16))
        self.eas.pack(expand=1,fill='x')
        panelbt=tk.Frame(self.ras)
        tk.Button(panelbt,text='保存',font=('',16),command=lambda:self.alarmsok(aenum)).pack(side='left')
        tk.Button(panelbt,text='取消',font=('',16),command=self.alarmscancel).pack(side='left')
        panelbt.pack()
    def alarmsok(self,aenum):
        name=self.eas.get()
        self.ras.destroy()
        if name=='':
            messagebox.showwarning('闹钟名称','闹钟名称不能为空！')
        elif name in self.dalarm:
            messagebox.showwarning('闹钟名称','闹钟名称已有，请重新输入！')
        else:
            exec("alarmtime=self.ehour%s.get()+':'+self.emin%s.get()+':'+self.esec%s.get()"%(aenum,aenum,aenum))
            exec("self.dalarm[name]=[alarmtime,self.ewi%s]"%aenum)
            exec("self.ewi%s.withdraw()"%aenum)
    def alarmscancel(self):
        self.ras.destroy()
    def dlupgrade(self,aenum):
        if eval("self.dltag%s"%aenum):
            exec("self.varmsg%s.set('倒计时正在运行')"%aenum)
            exec("if self.sec%s!=0:\n\tself.sec%s-=1\nelif self.min%s!=0:\n\tself.min%s-=1\n\tself.sec%s=59\nelif self.hour%s!=0:\n\tself.hour%s-=1\n\tself.min%s=59\n\tself.sec%s=59\nelse:\n\tself.varmsg%s.set('倒计时结束')\n\tself.ertbt2%s.config(text='开始倒计时',command=lambda:self.dl(aenum))\n\tself.dltag%s=False"%((aenum,)*12),dict(locals(),**globals()))
            exec("ahour,amin,asec=self.hour%s,self.min%s,self.sec%s"%(aenum,aenum,aenum))
            exec("adhour,admin,adsec='%.2d'%(int(ahour)),'%.2d'%(int(amin)),'%.2d'%(int(asec))")
            exec("self.varhour%s.set(adhour)"%aenum)
            exec("self.varmin%s.set(admin)"%aenum)
            exec("self.varsec%s.set(adsec)"%aenum)
            exec("self.up%s=self.ewi%s.after(1000,lambda:self.dlupgrade(aenum))"%(aenum,aenum),dict(locals(),**globals()))
    def dlstop(self,aenum):
        exec("self.ewi%s.after_cancel(self.up%s)"%(aenum,aenum))
        exec("self.varmsg%s.set('')"%aenum)
        exec("self.ertbt2%s.config(text='开始倒计时',command=lambda:self.dl(aenum))"%aenum,dict(locals(),**globals()))
    def dl(self,aenum):
        if self.formaterr(aenum):
            exec("self.ertbt2%s.config(text='停止倒计时',command=lambda:self.dlstop(aenum))"%aenum,dict(locals(),**globals()))
            exec("self.dltag%s=True"%aenum)
            self.dlupgrade(aenum)
    def rdreset(self,aenum):
        exec("self.varmsg%s.set('')"%aenum)
        exec("self.varhour%s.set('%.2d')"%(aenum,0))
        exec("self.varmin%s.set('%.2d')"%(aenum,0))
        exec("self.varsec%s.set('%.2d')"%(aenum,0))
    def formaterr(self,aenum):
        try:
            exec("self.hour%s,self.min%s,self.sec%s=int(self.ehour%s.get()),int(self.emin%s.get()),int(self.esec%s.get())"%((aenum,)*6))
            exec("if self.hour%s>=0 and 0<=self.min%s<=59 and 0<=self.sec%s<=59:\n\tformateok=True\nelse:\n\tself.varmsg%s.set('超出范围,请重新输入！')\n\tself.varhour%s.set('%.2d')\n\tself.varmin%s.set('%.2d')\n\tself.varsec%s.set('%.2d')\n\tformateok=False"%((aenum,)*4+(aenum,0)*3),dict(locals(),**globals()),globals())
        except:
            exec("self.varmsg%s.set('格式错误')"%aenum)
            formateok=False
        return globals()['formateok']
    def ewiclose(self,aenum):
        top=[]
        for value in self.dalarm.values():
            top.append(value[1])
        exec("if self.varmsg%s.get()=='闹钟已设定' or self.varmsg%s.get()=='正在响铃，请及时关闭闹钟！':\n\tif self.ewi%s in top:\n\t\tself.ewi%s.withdraw()\n\telse:\n\t\twinsound.PlaySound(None,winsound.SND_FILENAME)\n\t\tself.ewi%s.destroy()\nelse:\n\twinsound.PlaySound(None,winsound.SND_FILENAME)\n\tself.ewi%s.destroy()"%((aenum,)*6))
    def ert(self,ewn,aenum):
        self.aenum+=1
        exec("self.ewi%s=tk.Toplevel()"%aenum)
        exec("self.ewi%s.geometry('296x90')"%aenum)
        exec("self.ewi%s.iconbitmap(iicon)"%aenum)
        if ewn=='erb':
            exec("self.ewi%s.title('编辑闹钟')"%aenum)
        if ewn=='edl':
            exec("self.ewi%s.title('倒计时')"%aenum)
        exec('self.ewi%s.protocol("WM_DELETE_WINDOW",lambda:self.ewiclose(aenum))'%aenum,dict(locals(),**globals()))
        exec("self.varmsg%s=tk.StringVar()"%aenum)
        exec("self.varhour%s=tk.StringVar()"%aenum)
        exec("self.varmin%s=tk.StringVar()"%aenum)
        exec("self.varsec%s=tk.StringVar()"%aenum)
        exec("panelentry%s=tk.Frame(self.ewi%s)"%(aenum,aenum))
        exec("self.ehour%s=tk.Entry(panelentry%s,justify='center',textvariable=self.varhour%s,width=12)"%(aenum,aenum,aenum))
        exec("self.ehour%s.pack(side='left')"%aenum)
        exec("tk.Label(panelentry%s,text=':').pack(side='left')"%aenum)
        exec("self.emin%s=tk.Entry(panelentry%s,justify='center',textvariable=self.varmin%s,width=12)"%(aenum,aenum,aenum))
        exec("self.emin%s.pack(side='left')"%aenum)
        exec("tk.Label(panelentry%s,text=':').pack(side='left')"%aenum)
        exec("self.esec%s=tk.Entry(panelentry%s,justify='center',textvariable=self.varsec%s,width=12)"%(aenum,aenum,aenum))
        exec("self.esec%s.pack(side='left')"%aenum)
        exec("panelentry%s.pack(expand=1)"%aenum)
        exec("panelertbt%s=tk.Frame(self.ewi%s)"%(aenum,aenum))
        exec("self.varhour%s.set('%.2d')"%(aenum,0))
        exec("self.varmin%s.set('%.2d')"%(aenum,0))
        exec("self.varsec%s.set('%.2d')"%(aenum,0))
        exec("tk.Label(self.ewi%s,textvariable=self.varmsg%s,font=('',13)).pack(expand=1)"%(aenum,aenum))
        if ewn=='erb':
            exec("self.ertbt1%s=tk.Button(panelertbt%s,text='设定闹钟',font=('',13),command=lambda:self.rinb(aenum))"%(aenum,aenum),dict(locals(),**globals()))
            exec("self.ertbt1%s.pack(side='left')"%aenum)
            exec("self.ertbts%s=tk.Button(panelertbt%s,text='保存闹钟',font=('',13),command=lambda:self.alarms(aenum))"%(aenum,aenum),dict(locals(),**globals()))
            exec("self.ertbts%s.pack(side='left')"%aenum)
        if ewn=='edl':
            exec("self.ertbt2%s=tk.Button(panelertbt%s,text='开始倒计时',font=('',13),command=lambda:self.dl(aenum))"%(aenum,aenum),dict(locals(),**globals()))
            exec("self.ertbt2%s.pack(side='left')"%aenum)
        exec("tk.Button(panelertbt%s,text='复位',font=('',13),command=lambda:self.rdreset(aenum)).pack(side='left')"%aenum,dict(locals(),**globals()))
        exec("panelertbt%s.pack(expand=1)"%aenum)
    def swupdate(self,aenum):
        exec("self.se%s=time.time()-self.start%s"%(aenum,aenum))
        exec("self.swshow(self.se%s,aenum)"%aenum)
        exec("self.swtimer%s=self.win%s.after(50,lambda:self.swupdate(aenum))"%(aenum,aenum),dict(locals(),**globals()))
    def swshow(self,tm,aenum):
        minutes=int(tm/60)
        seconds=int(tm-minutes*60.0)
        hsec=int((tm-minutes*60.0-seconds)*100)
        exec("self.varsw%s.set('%.2d:%.2d:%.2d')"%(aenum,minutes,seconds,hsec))
    def swstart(self,aenum):
        exec("self.swbt1%s.config(text='停止计时',command=lambda:self.swstop(aenum))"%aenum,dict(locals(),**globals()))
        exec("self.start%s=time.time()-self.se%s"%(aenum,aenum))
        self.swupdate(aenum)
    def swstop(self,aenum):
        exec("self.win%s.after_cancel(self.swtimer%s)"%(aenum,aenum))
        exec("self.se%s=time.time()-self.start%s"%(aenum,aenum))
        exec("self.swshow(self.se%s,aenum)"%aenum)
        exec("self.swbt1%s.config(text='开始计时',command=lambda:self.swstart(aenum))"%aenum,dict(locals(),**globals()))
    def swcount(self,aenum):
        self.countnum+=1
        try:
            if not self.rct.winfo_exists():
                self.swrc()
        except:
            self.swrc()
        exec("self.treesw.insert('',index='end',text=self.countnum,values=[self.varsw%s.get()])"%aenum)
    def swrc(self):
        self.rct=tk.Toplevel()
        self.rct.iconbitmap(iicon)
        self.rct.title('计次')
        self.rct.protocol("WM_DELETE_WINDOW",self.swrclose)
        ygd=tk.Scrollbar(self.rct)
        ygd.pack(side='right',fill='y')
        self.treesw=ttk.Treeview(self.rct,columns=('time'),yscrollcommand=ygd.set)
        ygd.config(command=self.treesw.yview)
        self.treesw.heading('#0',text='序号')
        self.treesw.heading('#1',text='用时')
        self.treesw.pack(expand=1,fill='both')
    def swrclose(self):
        self.countnum=0
        self.rct.destroy()
    def swreset(self,aenum):
        exec("self.se%s=0"%aenum)
        exec("self.swshow(self.se%s,aenum)"%aenum)
    def swt(self,aenum):
        self.aenum+=1
        exec("self.se%s=0"%aenum)
        exec("self.win%s=tk.Toplevel()"%aenum)
        exec("self.win%s.geometry('250x100')"%aenum)
        exec("self.win%s.iconbitmap(iicon)"%aenum)
        exec("self.win%s.title('秒表')"%aenum)
        exec("self.varsw%s=tk.StringVar()"%aenum)
        exec("tk.Label(self.win%s,textvariable=self.varsw%s,font=('',35)).pack(expand=1)"%(aenum,aenum))
        exec("self.swshow(self.se%s,aenum)"%aenum)
        exec("panelsw%s=tk.Frame(self.win%s)"%(aenum,aenum))
        exec("panelsw%s.pack(expand=1)"%aenum)
        exec("self.swbt1%s=tk.Button(panelsw%s,text='开始计时',font=('',13),command=lambda:self.swstart(aenum))"%(aenum,aenum),dict(locals(),**globals()))
        exec("self.swbt1%s.pack(side='left')"%aenum)
        exec("self.swbt2%s=tk.Button(panelsw%s,text='计次',font=('',13),command=lambda:self.swcount(aenum))"%(aenum,aenum),dict(locals(),**globals()))
        exec("self.swbt2%s.pack(side='left')"%aenum)
        exec("tk.Button(panelsw%s,text='复位',font=('',13),command=lambda:self.swreset(aenum)).pack(side='left')"%aenum,dict(locals(),**globals()))
    def alarmedit(self):
        for i in self.treeam.selection():
            name=self.treeam.item(i)['text']
            self.dalarm[name][1].deiconify()
    def alarmdelete(self):
        winsound.PlaySound(None,winsound.SND_FILENAME)
        for i in self.treeam.selection():
            name=self.treeam.item(i)['text']
            self.treeam.delete(i)
            self.dalarm[name][1].destroy()
            self.dalarm.pop(name)
    def alarmalldelete(self):
        winsound.PlaySound(None,winsound.SND_FILENAME)
        for i in self.treeam.get_children():
            name=self.treeam.item(i)['text']
            self.treeam.delete(i)
            self.dalarm[name][1].destroy()
            self.dalarm.clear()
    def alarmm(self):
        self.ram=tk.Toplevel()
        self.ram.iconbitmap(iicon)
        self.ram.title('管理闹钟')
        ygd=tk.Scrollbar(self.ram)
        ygd.pack(side='right',fill='y')
        self.treeam=ttk.Treeview(self.ram,columns=('alarm'),yscrollcommand=ygd.set)
        self.popupmenu=tk.Menu(self.root,tearoff=0)
        self.popupmenu.add_command(label=u'编辑闹钟',command=self.alarmedit)
        self.popupmenu.add_command(label=u'删除',command=self.alarmdelete)
        self.popupmenu.add_command(label=u'全部删除',command=self.alarmalldelete)
        self.treeam.bind('<Button-3>',self.showPopupMenu)
        ygd.config(command=self.treeam.yview)
        self.treeam.heading('#0',text='名称')
        self.treeam.heading('#1',text='响铃时间')
        for key,value in self.dalarm.items():
            self.treeam.insert('',index='end',text=key,values=[value[0]])
        self.treeam.pack(expand=1,fill='both')
    def showPopupMenu(self,event):
        self.popupmenu.post(event.x_root,event.y_root)
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
    def dc(self):
        self.root=tk.Tk()
        self.root.iconbitmap(iicon)
        self.root.title('数字时钟')
        self.root.protocol("WM_DELETE_WINDOW",self.callback)
        self.root.call('package','require','Winico')
        self.icon=self.root.call('winico','createfrom',iicon)
        self.root.call('winico','taskbar','add',self.icon,'-callback',(self.root.register(self.menuf),'%m','%x','%y'),'-pos',0,'-text',u'数字时钟')
        self.menu=tk.Menu(self.root,tearoff=0)
        self.menu.add_command(label=u'显示主页面',command=self.root.deiconify)
        self.menu.add_command(label=u'编辑闹钟',command=lambda:self.ert('erb',self.aenum))
        self.menu.add_command(label=u'管理闹钟',command=self.alarmm)
        self.menu.add_command(label=u'关于',command=self.about)
        self.menu.add_command(label=u'隐藏主页面',command=self.root.withdraw)
        self.menu.add_command(label=u'退出',command=self.allquit)
        self.vartodaynl=tk.StringVar(self.root)
        self.vartoday=tk.StringVar(self.root)
        self.varcurtime=tk.StringVar(self.root)
        tk.Label(self.root,textvariable=self.vartodaynl,font=('',21)).pack(expand=1)
        tk.Label(self.root,textvariable=self.vartoday,font=('',25)).pack(expand=1)
        tk.Label(self.root,textvariable=self.varcurtime,font=('Arial',45)).pack(expand=1)
        self.settime()
        panelrootbt=tk.Frame(self.root)
        tk.Button(panelrootbt,text='透明度',font=('',15),command=self.Attr).pack(side='left')
        tk.Button(panelrootbt,text='编辑闹钟',font=('',15),command=lambda:self.ert('erb',self.aenum)).pack(side='left')
        tk.Button(panelrootbt,text='管理闹钟',font=('',15),command=self.alarmm).pack(side='left')
        tk.Button(panelrootbt,text='倒计时',font=('',15),command=lambda:self.ert('edl',self.aenum)).pack(side='left')
        tk.Button(panelrootbt,text='秒表',font=('',15),command=lambda:self.swt(self.aenum)).pack(side='left')
        tk.Button(panelrootbt,text='退出',font=('',15),command=self.allquit).pack(side='left')
        panelrootbt.pack(expand=1)
        self.root.mainloop()
if getattr(sys,'frozen',False):
        odir=sys._MEIPASS
else:
    odir=os.path.dirname(os.path.abspath(__file__))
iicon=os.path.join(odir,'数字时钟.ico')
isound=os.path.join(odir,'闹钟.wav')
Dc().dc()