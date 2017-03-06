#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 08:39:04 2016
基于DNSpod和淘宝ip的API
@author: mxhcbl
"""
try:
    import requests
except:
    print '并没有安装requests'
import json
def setConfig():
    domain_name = str(raw_input('输入您的域名，类似于imple.top\n'))
    sub_domain = str(raw_input('输入您的子域名，类似于www bbs blog @\n'))
    token_id = str(raw_input('输入您的dnspod token的ID\n'))
    token_key = str(raw_input('输入您的dnspod token的key\n'))
    config = {'domain_name':domain_name,'sub_domain':sub_domain,'token_id':token_id,'token_key':token_key,'mail':'2333@qq.com'}
    json_str = json.dumps(config,indent=2)
    try:
        with open('./pi_ddns.json','w') as f:
            f.write(json_str)
    except IOError as e:
        print 'Error : '+e
try:
    with open('./pi_ddns.json','r') as f:
        config = json.loads(f.read())
except:
    setConfig()
    print "请重新执行一下这个脚本，即可正常运行"
    exit()
public = {
    'login_token':config['token_id']+','+config['token_key'],
    'format':'json',
    'lang':'cn',
}
headers = {'User-Agent':'Pi ddns/1.0('+config['mail']+')'}
def getDomainId():
    parameter = public
    parameter['domain'] = config['domain_name']
    r = requests.post('https://dnsapi.cn/Domain.Info',parameter).json()
    if r['status']['code']=='1':
        return r['domain']['id']
    else:
        print r['status']['message']
        exit()
def getRecords():
    parameter = public
    parameter['domain_id'] = domain_id
    parameter['sub_domain'] = config['sub_domain']
    r = requests.post('https://dnsapi.cn/Record.List',parameter).json()
    if r['status']['code']=='1':
        for i in r['records']:
            if i['type'] == 'A':
                return {'domain_id':parameter['domain_id'],'record_id':i['id'],'ip':i['value']}
    else:
        print r['status']['message']
        exit()
def updateDns(ip):
    parameter = public
    parameter['domain_id'] = domain_id
    parameter['record_id'] = record_id
    parameter['sub_domain'] = config['sub_domain']
    parameter['record_type'] = 'A'
    parameter['record_line'] = u'默认'
    parameter['ttl'] = '600'
    parameter['value']=ip
    r = requests.post('https://dnsapi.cn/Record.Modify',parameter).json()
    if r['status']['code']=='1':
        print '更新成功'
    else:
        print r['status']['message']

domain_id = getDomainId()
record = getRecords()
record_id = record['record_id']
myip = requests.get('http://ip.taobao.com/service/getIpInfo2.php?ip=myip').json()['data']['ip']
if record['ip'] != myip:
    updateDns(myip)
else:
	print '并没有发生什么变化\(≧▽≦)/'