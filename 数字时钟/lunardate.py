import math,ephem
yuefen=["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","冬月","腊月"]
nlrq=["初一","初二","初三","初四","初五","初六","初七","初八","初九","初十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十","廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"]
tiangan=["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi=["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
gz=['']*60
for i in range(60):
	gz[i]=tiangan[i%10]+dizhi[i%12]
def EquinoxSolsticeJD(year,angle):
	if 0<=angle<90:
		date=ephem.next_vernal_equinox(year)
	elif 90<=angle<180:
		date=ephem.next_summer_solstice(year)
	elif 180<=angle<270:
		date=ephem.next_autumn_equinox(year)
	else:
		date=ephem.next_winter_solstice(year)
	JD=ephem.julian_date(date)
	return JD
def SolarLongitube(JD):
	date=ephem.Date(JD-2415020)
	s=ephem.Sun(date)
	sa=ephem.Equatorial(s.ra,s.dec,epoch=date)
	se=ephem.Ecliptic(sa)
	L=se.lon/ephem.degree/180*math.pi
	return L
def SolarTerms(year,angle):
    if angle>270:
        year-=1
    if year==0:
        year-=1
    JD=EquinoxSolsticeJD(str(year),angle)
    JD1=JD
    while True:
        JD2=JD1
        L=SolarLongitube(JD2)
        JD1+=math.sin(angle*math.pi/180-L)/math.pi*180
        if abs(JD1-JD2)<0.00001:
            break
    return JD1
def DateCompare(JD1,JD2):
    JD1+=0.5+8/24
    JD2+=0.5+8/24
    if int(JD1)>=int(JD2):
        return True
    else:
        return False
def dzs_search(year):
    if year==1:
        year-=1
    dz=ephem.next_solstice(str(year-1)+'/12')
    jd=ephem.julian_date(dz)
    date1=ephem.next_new_moon(ephem.Date(jd-2415020-0))
    jd1=ephem.julian_date(date1)
    date2=ephem.next_new_moon(ephem.Date(jd-2415020-29))
    jd2=ephem.julian_date(date2)
    date3=ephem.next_new_moon(ephem.Date(jd-2415020-31))
    jd3=ephem.julian_date(date3)
    if DateCompare(jd,jd1):
        return date1
    elif DateCompare(jd,jd2)and (not DateCompare(jd,jd1)):
        return date2
    elif DateCompare(jd,jd3):
        return date3
def Animals(date):
    animals=['猴','鸡','狗','猪','鼠','牛','虎','兔','龙','蛇','马','羊']
    year=date[0:date.find('-')]
    index=int(year)%12
    animal=animals[index]
    return animal
def SolarLunarCalendar(date):
    JD=ephem.julian_date(date)-8/24
    year=ephem.Date(JD+8/24-2415020).triple()[0]
    shuo=[]
    shuo.append(dzs_search(year))
    sJD1=ephem.julian_date(shuo[0])
    next_dzs=dzs_search(year+1)
    dzsJD=ephem.julian_date(next_dzs)
    if DateCompare(JD,dzsJD):
        shuo[0]=next_dzs
        next_dzs=dzs_search(year+2)
        dzsJD=ephem.julian_date(next_dzs)
    run=''
    szy=0
    i=-2
    j=-1
    zry=99
    flag=False
    while not DateCompare(sJD1,dzsJD):
        i+=1
        j+=1
        sJD1=ephem.julian_date(shuo[j])
        if DateCompare(JD,sJD1):
            szy+=1
            newmoon=int(sJD1+8/24+0.5)
        shuo.append(ephem.next_new_moon(shuo[j]))
        if j==0:
            continue
        sJD2=ephem.julian_date(shuo[j+1])
        angle=(-90+30*i)%360
        if j==1:
            nian1=ephem.Date(sJD1+8/24-2415020).triple()[0]
            qJD1=SolarTerms(nian1,angle)
        else:
            qJD1=qJD2
        nian2=ephem.Date(sJD2+8/24-2415020).triple()[0]
        qJD2=SolarTerms(nian2,(angle+30)%360)
        if not DateCompare(qJD1,sJD1)and DateCompare(qJD2,sJD2)and flag==False:
                zry=j+1
                i-=1
                flag=True
    rq=int(JD+8/24+0.5)-newmoon
    if j==12 and zry!=99:
        zry=99
    if szy%12==zry%12 and zry!=99:
        run='闰'
    if szy>=zry%12 and zry!=99:
        szy-=1
    month=ephem.Date(date).triple()[1]
    angle=(-135+30*month)%360
    jJD2=SolarTerms(year,(angle+30)%360)
    if angle==225:
        jJD3=SolarTerms(year+1,(angle+60)%360)
    else:
        jJD3=SolarTerms(year,(angle+60)%360)
    if angle==255:
        jJD1=SolarTerms(year-1,angle)
    else:
        jJD1=SolarTerms(year,angle)
    daxue=False
    if DateCompare(JD,jJD3):
        jq=ephem.Date(jJD3+8/24-2415020)
        month2=(angle+15-210)//30%12
        if angle==225:
            daxue=True
    elif DateCompare(JD,jJD2):
        jq=ephem.Date(jJD2+8/24-2415020)
        month2=(angle+15-240)//30%12
        if angle==225 or (jq.triple()[1]==12 and angle==255):
            daxue=True
    else:
        jq=ephem.Date(jJD1+8/24-2415020)
        month2=(angle+15-270)//30%12
        if angle==255:
            daxue=True
    nian2=jq.triple()[0]
    if nian2<0:
        nian2+=1
    if daxue==True:
        nian2+=1
    jqy=gz[(nian2*12+month2+12)%60]
    if (szy-3)%12>=10 and ephem.Date(date).triple()[1]<=3:
        year-=1
    if year<0:
        year+=1
    nlyear,nlmonth,nlday=gz[(year-4)%60],run+yuefen[(szy-3)%12],nlrq[rq]
    nlanimal=Animals(date)
    return nlyear,nlanimal,nlmonth,nlday