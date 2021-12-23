import json
import os
import subprocess
import time

def main():
    consumer="node9-13"
    producer="node9-21"
    namePath = findTheParth(consumer,producer)
    ipPath = getIPlist(namePath)
    print(namePath)
    print(ipPath)
    configureNodes(ipPath)


def configureNodes(ipPathlist):
    #content = subprocess.run("nc -l -p 7998", shell=True)
    content = "/temp2"
    print(content)
    #iplist = ["10.10.10.29","10.10.10.4", "10.10.10.19"]
    for i in range(len(ipPathlist)-1):
        print(ipPathlist[i])
        #create face
        addfacecmd = 'echo "ndnaddface tcp4://%s" | nc -q 1 %s 8000 &'%(ipPathlist[i+1], ipPathlist[i])
        subprocess.run(addfacecmd, shell=True)
        time.sleep(1)
        #register content to the next face
        registercmd = 'echo "ndnregister %s tcp4://%s" | nc -q 1 %s 8000 &'%(content, ipPathlist[i+1], ipPathlist[i])
        subprocess.run(registercmd, shell=True)
        time.sleep(1)




def findTheParth(consumer,producer):
    nodesInfo=getNodesInfo()
    nodesPath = []
    endNode = False
    nodesPath.append(consumer)
    consumerBMAC=getBMACFromNodesInfo(nodesInfo,consumer)
    producerBMAC=getBMACFromNodesInfo(nodesInfo,producer)
    consumerWMAC=getWMACFromNodesInfo(nodesInfo,consumer)
    producerWMAC=getWMACFromNodesInfo(nodesInfo,producer)
    originators = getNodeOriginators(consumerBMAC)
    while endNode == False:
        walking = False
        for i in originators:
            if i['orig_address']==producerWMAC and i['neigh_address']==producerWMAC:
                nodesPath.append(producer)
                walking = True
                endNode = True
                break
        if endNode == False:
            for i in originators:
                if i['orig_address']==producerWMAC:
                    nextHopWMAC=i['neigh_address']
                    nextHopName=getNodeNameFromWMAC(nodesInfo,nextHopWMAC)
                    nodesPath.append(nextHopName)
                    #print(nextHopName)
                    nextHopBMAC=getBMACFromNodesInfo(nodesInfo,nextHopName)
                    originators=getNodeOriginators(nextHopBMAC)
                    walking = True
                    break
        if walking == False:
            print("There is NOT path for this producer node")
    return nodesPath
    
def getIPlist(namePath):
    ipPath = []
    nodesInfo=getNodesInfo()
    for i in namePath:
        nodeIP=getIPFromName(nodesInfo,i)
        ipPath.append(nodeIP)
    return ipPath


def getNodesInfo():
    file1 = open('nodesinfo', 'r')
    file1lines = file1.readlines()
    nodesinfo=[]
    for i in file1lines:
        i = i.replace('", "','" : "')
        i = i.replace(' },',' }')
        data = json.loads(i)
        content = list(data.values())[0]
        content = content.replace("'",'"')
        nodeinfo = json.loads(content)
        nodesinfo.append(nodeinfo)
    file1 .close()
    return nodesinfo

def getNodeOriginators(nodeBMAC):
    file2 = open('bestoriginators', 'r')
    file2lines = file2.readlines()
    originators = []
    for i in file2lines:
        #print(i)
        i = i.replace('", "','" : "')
        i = i.replace(' },',' }')
        #print(i)
        data = json.loads(i)
        if nodeBMAC in data:
             originators=data[nodeBMAC]
             originators = originators.replace("'",'"')
             originators = originators.replace('True','"True"')
             originators = json.loads(originators)
    #    print(data2['ip'])
    return originators
    file2 .close()

def getBMACFromNodesInfo(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             bMac=i["bmac"]
    return bMac

def getWMACFromNodesInfo(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             wMac=i["wmac"]
    return wMac

def getNodeNameFromWMAC(nodesInfo,wMAC):
    for i in nodesInfo:
        if i['wmac'] == wMAC:
             name=i["name"]
    return name

def getIPFromName(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             name=i["ip"]
    return name

if __name__ == "__main__":
    #while True:
            main()








