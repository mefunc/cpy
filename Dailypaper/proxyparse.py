import re,requests
from threading import Barrier,Thread
class Getproxy:
    def __init__(self):
        self.proxyservers=[]
        self.proxybarrier=Barrier(4)
    def Threadgetproxy(self):
        Thread(target=self.Pdb).start()
        Thread(target=self.Jxl).start()
        Thread(target=self.Kdl).start()
        self.proxybarrier.wait()
        return self.proxyservers
    def Parserget(self,url,headers=None,timeout=5):
        try:
            resp=requests.get(url,headers=headers)
            if resp.status_code==200:
                return resp
            else:
                return self.Proxyparse(url,headers,timeout)
        except:
            return self.Proxyparse(url,headers,timeout)
    def Proxyparse(self,url,headers,timeout):
        proxyservers=self.Threadgetproxy()
        for proxyserver in proxyservers:
            try:
                resp=requests.get(url,headers=headers,proxies={'http':proxyserver,'https':proxyserver},timeout=timeout)
                if resp.status_code==200:
                    return resp
            except:
                pass
    def Generateproxy(self,proxys):
        for proxy in proxys:
            proxyserver=proxy[0]+':'+proxy[1]
            self.proxyservers.append(proxyserver)
    def Pdb(self):
        try:
            resp=requests.get('http://proxydb.net/?country=CN',headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36'})
            proxys=re.findall(r'<a href=".+">(.+):(.+)</a>',resp.text)
            self.Generateproxy(proxys)
        except:
            pass
        self.proxybarrier.wait()
    def Jxl(self):
        try:
            resp=requests.get('https://ip.jiangxianli.com/country/中国?country=中国')
            proxys=re.findall(r'<tr><td>(.+?)</td><td>(\d+)</td>',resp.text)
            self.Generateproxy(proxys)
        except:
            pass
        self.proxybarrier.wait()
    def Kdl(self):
        try:
            resp=requests.get('https://www.kuaidaili.com/free',headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)''AppleWebKit/537.36 (KHTML, like Gecko)''Chrome/83.0.4103.97 Safari/537.36'})
            proxys=re.findall(r'<td data-title="IP">(.+)</td>\s+<td data-title="PORT">(.+)</td>',resp.text)
            self.Generateproxy(proxys)
        except:
            pass
        self.proxybarrier.wait()