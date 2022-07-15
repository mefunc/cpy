import os,mariadb,configparser
inipath=os.path.dirname(os.path.abspath(__file__))+os.sep+'Wordpressconfig.ini'
def configok():
    if os.path.isfile(inipath):
        config=configparser.ConfigParser()
        config.optionxform=lambda option:option
        config.read(inipath)
        place=config['Wordpress']['place']
        host=config['Wordpress']['host']
        port=config['Wordpress']['port']
        database=config['Wordpress']['database']
        user=config['Wordpress']['user']
        password=config['Wordpress']['password']
        if not all([place,host,port,database,user,password]):
            print('配置信息不能为空，在配置文件Wordpressconfig.ini填写好对应信息后再运行')
            inimsg=[False]
        else:
            conn=mariadb.connect(host=host,port=int(port),database=database,user=user,password=password,autocommit=True)
            inimsg=[True,place,conn]
    else:
        print('正在生成配置文件...')
        config=configparser.ConfigParser(allow_no_value=True)
        config.optionxform=lambda option:option
        config['Wordpress']={}
        config['Wordpress']['#Mariadb数据库服务器的主机名或IP地址，例如localhost或192.0.2.1']=None
        config['Wordpress']['host']=''
        config['Wordpress']['#Mariadb数据库服务器的端口号，默认3306']=None
        config['Wordpress']['port']='3306'
        config['Wordpress']['#连接Mariadb数据库服务器时使用的数据库名称，例如wordpress']=None
        config['Wordpress']['database']=''
        config['Wordpress']['#用于向Mariadb数据库服务器进行身份验证的用户名，例如admin']=None
        config['Wordpress']['user']=''
        config['Wordpress']['#给定用户的密码，例如123456']=None
        config['Wordpress']['password']=''
        config['Wordpress']['#启用的地方名称拼音，可以在Localdailypaper文件夹下找到。多个地方用英文逗号隔开，例如people,beijing。默认all，启用所有']=None
        config['Wordpress']['place']='all'
        with open(inipath,'w') as file:
            config.write(file)
        print('配置文件Wordpressconfig.ini生成完成，填写好对应信息后再运行')
        inimsg=[False]
    return inimsg