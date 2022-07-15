import os,winreg,configparser
from telethon.sync import TelegramClient
if os.path.isfile('Tgconfig.ini'):
    config=configparser.ConfigParser()
    config.optionxform=lambda option:option
    config.read('Tgconfig.ini',encoding='utf-8-sig')
    api_id=config['Tg']['api_id']
    api_hash=config['Tg']['api_hash']
    phone=int(config['Tg']['phone'])
    password=config['Tg']['password']
    ignored_chats=config['Tg']['ignored_chats']
    if not all([api_id,api_hash,phone]):
        print('配置信息不能为空，在配置文件Tgconfig.ini填写好对应信息后再运行')
        os.system('pause')
    else:
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings')
        count=winreg.QueryInfoKey(key)[1]
        for i in range(count):
            name=winreg.EnumValue(key,i)[0]
            command=winreg.EnumValue(key,i)[1]
            if name=='ProxyEnable':
                proxyenable=command
            if name=='ProxyServer':
                if proxyenable==0:
                    proxyserver=''
                else:
                    proxyserver=command
        winreg.CloseKey(key)
        proxyhost=proxyserver[0:proxyserver.find(':')]
        proxyport=proxyserver[proxyserver.find(':')+1:len(proxyserver)]
        print('正在登录...')
        try:
            client=TelegramClient('session',int(api_id),api_hash,proxy=('http',proxyhost,int(proxyport)))
            client.start(phone=phone,password=password)
        except:
            client=TelegramClient('session',int(api_id),api_hash,connection_retries=0)
            client.start(phone=phone,password=password)
        ldialogs=[]
        for dialog in client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                if not dialog.entity.title in ignored_chats.split('||'):
                    ldialogs.append(dialog)
        holdermsg='message'
        holderfile=client.upload_file('message.png')
        for dialog in ldialogs:
            for message in client.iter_messages(dialog.entity.id,from_user='me'):
                try:
                    message.edit(holdermsg,file=holderfile)
                except:
                    pass
                try:
                    message.delete()
                    print('删除成功："%s" "%s"'%(dialog.entity.title,message.text))
                except:
                    print('删除失败："%s" "%s"'%(dialog.entity.title,message.text))
        print('删除完成')
        os.system('pause')
else:
    print('正在生成配置文件...')
    config=configparser.ConfigParser(allow_no_value=True)
    config.optionxform=lambda option:option
    config['Tg']={}
    config['Tg']['#在my.telegram.org申请的api_id，例如00000000']=None
    config['Tg']['api_id']=''
    config['Tg']['#在my.telegram.org申请的api_hash，例如aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']=None
    config['Tg']['api_hash']=''
    config['Tg']['#电话号码，例如+8600000000000']=None
    config['Tg']['phone']='+86'
    config['Tg']['#2FA的密码，例如123456，没有不填']=None
    config['Tg']['password']=''
    config['Tg']['#排除的频道/群组名，没有不填。多个频道/群组用||隔开，例如name1||name2']=None
    config['Tg']['ignored_chats']=''
    with open('Tgconfig.ini','w',encoding='utf-8-sig') as file:
        config.write(file)
    print('配置文件Tgconfig.ini生成完成，填写好对应信息后再运行')
    os.system('pause')