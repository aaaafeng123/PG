#!/usr/bin/env python3

import sys
import re
import json
import requests
import time

p=re.compile(r'.*/s/(.*)')
reqcount=1

def getlist(shareid, fileid):
    global reqcount

    reqcount += 1
    if reqcount % 5 == 0:
        print(f"reqcount:{reqcount} shareid:{shareid} fileid:{fileid}",file=sys.stderr)
        time.sleep(1)
    resp = requests.get(f'http://192.168.101.188:9978/proxy?do=pikpak&type=list&share_id={shareid}&file_id={fileid}&pass_code=')
    content = resp.content.decode('utf-8')
    linearr = content.split('\t')
    if len(linearr)>2:
        print(content)
        if linearr[2] == "folder":
            m = p.match(linearr[0])
            if m:
                arr = m.group(1).split("/")
                shareid=arr[0]
                fileid=arr[1] if len(arr)>1 else ""
                print(shareid,fileid)
                getlist(shareid,fileid)

    
def main():
    with(open(sys.argv[1],"r",encoding="utf-8")) as f:
        j = json.load(f)
        for c in j:
            shareid=c.get("type_id")
            fileid=""
            m = p.match(shareid)
            if m:
                arr = m.group(1).split("/")
                shareid=arr[0]
                fileid=arr[1] if len(arr)>1 else ""
            getlist(shareid,fileid)

main()

