# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:53:31 2020

@author: User
"""


import requests
import pandas as pd
import time

def SMS_message_generator(station_local):
    sms_temp=''
    for i in range(len(station_local)):
        sms_temp=station_local[i]+'\n'+sms_temp
    return sms_temp

def lineNotifyMessage(token, msg):
    headers = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def information():
    new = a1['records']['earthquake'][0]
    earthquake_center = new['earthquakeInfo']['epiCenter']['location']
    scale = new['earthquakeInfo']['magnitude']['magnitudeValue']
    depth = new["earthquakeInfo"]['depth']['value']
    origintime = new["earthquakeInfo"]['originTime']

    shakingarea = new['intensity']['shakingArea']
    local = []
    tainan = []
    Kao = []
    for i in range(len(shakingarea)):
        local_earthquake = shakingarea[i]
        if local_earthquake['areaDesc'][:4] == "最大震度":
            a=local_earthquake['areaDesc']+'：'+local_earthquake['areaName']
            local.append(a)
        elif local_earthquake['areaDesc'][:3] == "臺南市":
            for j in range(len(local_earthquake['eqStation'])):
                stationName=local_earthquake['eqStation'][j]['stationName']
                stationintensity=local_earthquake['eqStation'][j]['stationIntensity']['value']
                b = stationName+'：'+str(stationintensity)+'級'
                tainan.append(b)
        elif local_earthquake['areaDesc'][:3] == "高雄市":
            for k in range(len(local_earthquake['eqStation'])):
                Kao_stationName = local_earthquake['eqStation'][k]['stationName']
                Kao_staionintensity = local_earthquake['eqStation'][k]['stationIntensity']['value']
                c = Kao_stationName+'：'+str(Kao_staionintensity)+'級'
                Kao.append(c)
    msg='\n'+'時間：'+origintime+'\n'+'震央：'+earthquake_center+'\n'+'芮氏規模：'+str(scale)+'\n'+'地震深度：'+str(depth)+'公里'


    SMS_tainan = '\n'+'臺南各測站震度'+'\n'+SMS_message_generator(tainan)
    SMS_Kao = '\n'+'高雄各測站震度'+'\n'+SMS_message_generator(Kao)

    with open('profile.txt','a') as profile:
        profile.writelines('\n'+'============================'+msg+'\n'+'============================')
        profile.close()
    send = [msg,tainan,Kao,SMS_tainan,SMS_Kao]

    return send



#發送LINE訊息
def Line_message():
    q = information()
    token = '4yAYxRh5VeFmCR4LgvE8TAI0zZ0V1iFuobc1fzT5sOX'
    lineNotifyMessage(token, q[0])
    if bool(q[2]) == False and bool(q[1])==True:
        lineNotifyMessage(token, q[3])
    elif bool(q[1]) == False and bool(q[2])==True:
        lineNotifyMessage(token, q[4])
    elif len(q[1])*len(q[2])!= 0:
        lineNotifyMessage(token, q[3])
        lineNotifyMessage(token, q[4])
    else:
        None





while True:
    keys = ['https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWB-6C525CB2-02B0-4A6D-A3B9-2D6FE39CC4DE','https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-6C525CB2-02B0-4A6D-A3B9-2D6FE39CC4DE']

    for api_key in keys:
        url = requests.get(api_key)
        a1= url.json()

        new = a1['records']['earthquake'][0]
        scale = new['earthquakeInfo']['magnitude']['magnitudeValue']
        origintime = new["earthquakeInfo"]['originTime']
        data = [origintime,scale]

        csv_read = pd.read_csv('test.csv',encoding='utf-8').drop(['Unnamed: 0'],axis=1).sort_values(by=['時間'],ascending=True)
#取得CSV檔中，最新一筆資料。
        last_data = csv_read.iloc[-1:].values.tolist()
        data_list = csv_read.values.tolist()
    

#Requests資料和CSV檔最新資料比較
        if data not in data_list:
            csv_read_new=pd.DataFrame({"時間":[data[0]],"芮氏規模":[data[1]]})
            csv_read = csv_read.append(csv_read_new,ignore_index=True)
            print(csv_read)
            print('地震更新')
            print("時間:"+data[0])
            print("地震規模:"+str(data[1]))
            csv_read.to_csv('test.csv',encoding='utf_8_sig')
            time.sleep(20)
            Line_message()
        else:
            '''
            print('最近一次地震')
            print("時間:"+last_data[0][0])
            print("地震規模:"+str(last_data[0][1]))
            '''
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now)
            time.sleep(20)

