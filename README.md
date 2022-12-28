### Py Connect!
This is an FiberHome OLT Class for manager your device! Actually utilizing only Telnet mode (TL1 comming soon)


### How to use:
```python

from telnet import Fiberhome


OLT_ADDR = "172.16.1.2"
OLT_USER = "GEPON"
OLT_PASS = "GEPON"
OLT_USER_2 = "EN"
OLT_PASS_2 = "GEPON"
OLT_PORT = 23


if __name__ == '__main__':
    fb = Fiberhome(OLT_ADDR)
    login = fb.login(
        OLT_USER, 
        OLT_PASS, 
        OLT_USER_2, 
        OLT_PASS_2, 
        OLT_PORT)
    
    if(login):
        print("successfull logged-in")
    else:
        print("can't logged-in")
    

    fb.logout()
```


### Main functions
#### Classed funcions:
```python
getOnuAuth(mac)
getOnuUnAuth(mac)
getOnuBoard(mac)
getOnuPon(mac)
getOnuId(mac)
getOnuInfo(mac)
getOnuModel(mac)
getOnuSoftVersion(mac)
getOnuHardVersion(mac)
getOnuLanMacs(mac, port=1)
getOnuSignal(mac)
getOnuPortIsolation(mac)
getOnuPortInfo(board, pon, onuid)
getOnuPortSpeed(board, pon, onuid, port)
getOnuPortStatus(board, pon, onuid)
getOnuPortDuplex(board, pon, onuid, port)
getOnuAuthInfo(board, pon, onuid)
getDeviceUnauthiruzedOnus()
getModelUnauthorizedOnus()
getUnaunthorizedOnus()
getUnaunthorizedOnuInfo(mac)
getOnuServiceVlans(board, pon, onuid)
isOnuBridge(board, pon, onuid)
isOnuRouter(board, pon, onuid)
getOnuWanIndex(board, pon, onuid)
getOnuWanVlan(board, pon, onuid)
getOnuWanCos(board, pon, onuid)
getOnuWanModel(board, pon, onuid)
getOnuWanIpAddr(board, pon, onuid)
getOnuWanMask(board, pon, onuid)
getOnuWanGateway(board, pon, onuid)
getOnuWanDns1(board, pon, onuid)
getOnuWanDns2(board, pon, onuid)
```

##### Static funcs
```python
isFH(mac)
setOnuBridge(placa, pon, onuid, port, vlanid, vlantype='T')
setOnuDefaultConfig(placa, pon, onuid, defconf=1)
setOnuDHCPServer(placa, pon, onuid, gateway_addr, netmask, dhcp_start, dhcp_end, dns1, dns2,  enabled="enable", lease=1, type='pc'):
setOnuDisableDHCP(placa, pon, onuid)
rebootONU(placa, pon, onuid)
ConfigureOnuBridge(placa, pon, onuid, port, vlanid, vlantype='T', disabledhcp=True)
```



### Testing
This is tested on RP1000 and RP1200  Fiberhome version. and python 3.8.