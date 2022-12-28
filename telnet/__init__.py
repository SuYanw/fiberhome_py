import os
import sys
import telnetlib
import re
import time

DEFAULT_TELNET_TIMEOUT = 0.9



class Fiberhome:

    def __init__(self, ipaddr):
        self.ip = ipaddr

        print("Cadastrado OLT IP: {}" .format(ipaddr))
        
        self.__connected = False






    '''
        @doc: login
        @description: log-in on OLT
        @input_params: Username, Password and Port (default telnet)
        @output_type: bool
        @output_params: if logged return true, returns false if not
    '''   
    def login(self, user1, password1, user2, password2, port=23):    

        print("Tentando acessar OLT")

        try:
            self.acessa_olt = telnetlib.Telnet(self.ip, port, 
                    timeout = 2)

        except Exception as e:
            print("Erro: {}".format(e))
            sys.exit("nao acessou telnet: {}".format(e))
        
        print("Tentando autenticar na OLT")
        self.acessa_olt.write(("{}\n{}\n{}\n{}\n". format(user1, password1,user2, password2).encode('ascii')))

        time.sleep(DEFAULT_TELNET_TIMEOUT)

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        if(re.search("#", str(self.acessa_olt.read_very_eager())) is not None):
            self.__connected = True
            return 1
        else:
            return 0






    '''
        @doc: logout
        @description: no need
        @input_params:  no need
        @output_type: bool
        @output_params: Return true if sucessful logout, return if not logged.
    '''   
    def logout(self):   

        if not (self.__connected):
            return False

        self.acessa_olt.write(("cd .\nexit\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        self.acessa_olt.close()
        print("Feito logout na olt")
        return 1
    







    '''
        @doc:  
        @description: mac-address
        @input_params:  onu-mac-address
        @output_type: array
        @output_params: 
    '''  
    def getOnuAuth(self, mac):

        if not (self.__connected):
            return False

        self.acessa_olt.write(("cd onu\nshow onu-authinfo phy-id {}\n". format(mac)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 1.5)

        rtn = re.sub("[^0-9\-]", "", self.acessa_olt.read_very_eager().splitlines()[2].decode('utf-8')).split("-")
            
        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)
        return (rtn[1] == '506' and [0,0,0] or rtn)






    '''
        Get Onu Board, Pon, Uid by MAC
    '''
    def getOnuUnAuth(self, mac):
        if not (self.__connected):
            return False

        self.acessa_olt.write(("cd onu\nshow onu-info by {}\n".format(mac)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        rtn = self.acessa_olt.read_very_eager().decode('utf-8').splitlines(True)

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)
        
        return (len(rtn) == 3 and [0,0] or list(filter(None, re.split(r"[(\s)(\-*)]", str(rtn[3])))) )






    '''
        Get Onu Board  by MAC
    '''
    def getOnuBoard(self, mac):
        return self.getOnuAuth(mac)[0]






    '''
        Get Onu Pon  by MAC
    '''
    def getOnuPon(self, mac):
        return self.getOnuAuth(mac)[1]






    '''
        Get Onu Pon ID  by MAC
    '''
    def getOnuUid(self, mac):
        return self.getOnuAuth(mac)[2]






    '''
        GET SOFTWARE / HARDWARE OF ONU
        Returns: [onumodel, software version, hardware version]
    '''
    def getOnuInfo(self, mac, placa=0, pon=0, onuid=0):
        if not (self.__connected):
                    return False
                    
        if(placa == 0 or pon == 0 or onuid == 0):
            OnuInfo = self.getOnuAuth(mac)

            __Placa = OnuInfo[0]
            __Pon   = OnuInfo[1]
            __OnuID = OnuInfo[2]
        else:
            __Placa = placa
            __Pon   = pon
            __OnuID = onuid

        if(__Placa != 0):
            self.acessa_olt.write(("cd onu\nshow local_onu_ver slot {} pon {}\ncd .\n".format(__Placa, __Pon)).encode('ascii'))
            time.sleep(DEFAULT_TELNET_TIMEOUT + 2.0)
            out = self.acessa_olt.read_very_eager().decode('utf-8')
            
            #
            # self.acessa_olt.write(("cd .\n").encode('ascii'))
            # time.sleep(DEFAULT_TELNET_TIMEOUT)
    
            for line in out.splitlines(True):
                reline = list(filter(None, re.split(r"[\s+]", str(line))))
                if(reline[0] == str(__OnuID)):
                    
                    reline.pop(0) # remove onuid
                    reline.pop(1) # remove cfg_type
                    

                    if(len(reline) > 5):
                        reline.pop()  # remove cfg
                    
                    return reline

        return ['0', '0', '0']

    '''
        Get Onu Model by MAC
    '''
    def getOnuModel(self, mac):
        return self.getOnuInfo(mac)[0]

    '''
        Get Onu Software Version by MAC
    '''
    def getOnuSoftVersion(self, mac):
        return self.getOnuInfo(mac)[1]

    '''
        Get Hardware Version of Onu by MAC
    '''
    def getOnuHardVersion(self, mac):
        return self.getOnuInfo(mac)[2]

    '''
        Get Onu Lan Mac-Address 
        Return: 
    '''
    def getOnuLanMacs(self, mac, port=1, placa=0, pon=0, onuid=0):

        if not (self.__connected):
                    return False
                    
        if(placa == 0 or pon == 0 or onuid == 0):
            OnuInfo = self.getOnuAuth(mac)

            __Placa = OnuInfo[0]
            __Pon   = OnuInfo[1]
            __OnuID = OnuInfo[2]
        else:
            __Placa = placa
            __Pon   = pon
            __OnuID = onuid

        self.acessa_olt.write(("cd onu\nshow mac_list slot {} pon {} onu {} port {}\n".format(__Placa, __Pon,__OnuID, port)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 1.1)

        __rtncmd = str(self.acessa_olt.read_very_eager().decode('utf-8'))
        rtn = re.findall("[A-Za-z0-9\-]{16}[1-9a-zA-Z]", __rtncmd)

        # print("RETN: {}". format(__rtncmd))

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)
        return rtn









    '''
        Get onu Signal by FHTT (mac)
        Return: Signal
    '''
    def getOnuSignal(self, mac, placa=0, pon=0, onuid=0):
        if not (self.__connected):
            return False

        if(placa == 0 or pon == 0 or onuid == 0):
            OnuInfo = self.getOnuAuth(mac)

            __Placa = OnuInfo[0]
            __Pon   = OnuInfo[1]
            __OnuID = OnuInfo[2]
        else:
            __Placa = placa
            __Pon   = pon
            __OnuID = onuid

        self.acessa_olt.write(("cd onu\nshow optic_module slot {} pon {} onu {}\n".format(__Placa, __Pon, __OnuID)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 0.4)

        __rtncmd = str(self.acessa_olt.read_very_eager().splitlines(True)) 

        rtn = re.search('([-][0-9]*[.][0-9]{2})', __rtncmd, re.IGNORECASE)

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        if(__rtncmd.find("-553") != -1):
            return None
                    
        return (rtn is not None and rtn.group(1) or ("-0.0"))







    '''
        @getOnuPortIsolation
        Params: Mac=Fhtt, Placa=Optional, Pon=Optional, Onuid=Optional
        Return True when port isolation is enabled
        Return False when Port isolation is enabled or session telnet ins't not connected
    '''
    def getOnuPortIsolation(self, mac, placa=0, pon=0, onuid=0):

        if not (self.__connected):
            return False

        if(placa == 0 or pon == 0 or onuid == 0):
            OnuInfo = self.getOnuAuth(mac)

            __Placa = OnuInfo[0]
            __Pon   = OnuInfo[1]
            __OnuID = OnuInfo[2]
        else:
            __Placa = placa
            __Pon   = pon
            __OnuID = onuid

        self.acessa_olt.write(("cd onu\nshow port_separate slot {} pon {} onu {}\n".format(__Placa, __Pon, __OnuID)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        if(str(self.acessa_olt.read_very_eager().splitlines(True)).find("enable") != -1):
            return True

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        return False
        






    '''
        @getOnuPortInfo
        Params: Placa, Pon, Onuid
        Return None array if doesn't client active or does not exists
        Return False session telnet ins't not connected

        Normal returns bidirecional array with:
        array[0] = Port Status (Linked or not)
        array[1] = Port Speed (half or full)
        array[2] = Port Negociation 10MB or above
    '''
    def getOnuPortInfo(self, placa, pon, onuid):
        if not (self.__connected):
            return False
    

        self.acessa_olt.write(("cd onu\nshow feport_status slot {} pon {} onu {}\n".format(placa, pon, onuid)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 0.4)

        __cmdreturn = str(self.acessa_olt.read_very_eager())
        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        if(__cmdreturn.find("unactive") != -1):
            return [
                    None,
                    None,
                    None
            ]

        return [
                re.findall(":\s(Linked|Not Linked)", __cmdreturn),
                re.findall(":\s(half|full)", __cmdreturn),
                re.findall("[0-9]{2,4}[M,G]", __cmdreturn)
        ]
    







    '''
        @getOnuPortSpeed
        Params: Placa, Pon, Onuid, port=Optional
        Return None array if doesn't client active or does not exists
        Return False session telnet ins't not connected


        if parameter port is not selected, return all ports.
    '''
    def getOnuPortSpeed(self, placa, pon, onuid, port=0):
        if not (self.__connected):
            return False

        __portSpeed = self.getOnuPortInfo(placa, pon, onuid)[2]

        if(__portSpeed == None):
            return None
        
        return (port == 0 and __portSpeed or __portSpeed[int(port)-1])           






    '''
        @getOnuPortStatus
        Params: Placa, Pon, Onuid, port=Optional
        Return None array if doesn't client active or does not exists
        Return False session telnet ins't not connected
        
        Normal Returns:
        integer 1 if interface is active
        integer 0 if interface does not active

        if parameter port is not selected, return all ports.
    '''
    def getOnuPortStatus(self, placa, pon, onuid, port=0):
        if not (self.__connected):
            return False

        __portStatus = self.getOnuPortInfo(placa, pon, onuid)[0]

        if(__portStatus == None):
            return None

        return (port == 0 and [int(re.sub("^Linked$", "1", re.sub("^Not\sLinked", "0", __port))) for __port in __portStatus] or 
                int(__portStatus[int(port)-1].replace("Linked", "1").replace("Not Linked", "0")))





    '''
        @getOnuPortDuplex
        Params: Placa, Pon, Onuid, port=Optional
        Return None array if doesn't client active or does not exists
        Return False session telnet ins't not connected
        
        Normal Returns port duplex state: half, full

        if parameter port is not selected, return all ports.
    '''
    def getOnuPortDuplex(self, placa, pon, onuid, port=0):
        if not (self.__connected):
            return False
            
        __portDuplex = self.getOnuPortInfo(placa, pon, onuid)[1]
        
        if(__portDuplex == None):
            return None 

        return (port == 0 and __portDuplex or __portDuplex[int(port)-1])   


    def getOnuAuthInfo(self, placa, pon, onuid):
        if not (self.__connected):
            return False    

        self.acessa_olt.write(("cd onu\nshow wan_info slot {} pon {} onu {}\n".format(placa, pon, onuid)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        __cmdreturn = self.acessa_olt.read_very_eager().decode('utf-8')

        if(__cmdreturn.find("-20") != -1):
            return None

        if(__cmdreturn.find("ITEM=0") != -1):
            return -1

        return [re.sub("[:\s]", "", __port) for __port in re.findall(":\s\w*[0-9.]*", __cmdreturn)]







    '''
        @doc: getDeviceUnaunthorizedOnus
        @description: get board, pon, onu-mac pending auth
        @input_params: None
        @output_type: multiarray
        @output_params: [[  
            BOARD-ID,
            PON-ID,
            ONU-MACADDR,
            MANUFACTURER
        ]]
    '''
    def getDeviceUnaunthorizedOnus(self):
        if not (self.__connected):
            return False    

        self.acessa_olt.write(("lll\nshow authalarm\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT * 7)

        
        __cmdreturn = self.acessa_olt.read_very_eager()
        
        self.acessa_olt.write(("exit\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        # check nas no ONU pending 
        if(re.search("FHTT", str(__cmdreturn)) is None):
            return None
        #

        __outreturn = []
        for __gt_lst in __cmdreturn.splitlines():
            g_rtn = list(filter(None, re.split(r"[\s+]", str(__gt_lst.decode('utf-8')))))

            __tmpstr = []
            if(len(g_rtn) == 10 and g_rtn[0][0].isnumeric()):
                __tmpstr.append(g_rtn[0])
                __tmpstr.append(g_rtn[1])
                __tmpstr.append(g_rtn[4])
                __tmpstr.append(g_rtn[5])
                __outreturn.append(__tmpstr)
            
            elif(len(g_rtn) == 11 and g_rtn[0][0].isnumeric()):
                __tmpstr.append(g_rtn[0])
                __tmpstr.append(g_rtn[1])
                __tmpstr.append(g_rtn[4])
                __tmpstr.append(g_rtn[5])
                __outreturn.append(__tmpstr)

            
        return __outreturn





    '''
        @doc: getModelUnaunthorizedOnus
        @description: get mac, model(full), model(simplified), manufacturer, softversion, hardversion
        @input_params: None
        @output_type: multiarray
        @output_params: [[  
            MAC,
            MODELfull,
            ModelSimplified,
            Manufacturer,
            SoftwareVersion
            HardwareVersion
        ]]
    '''
    def getModelUnaunthorizedOnus(self):

        if not (self.__connected):
            return False    

        self.acessa_olt.write(("cd onu\nshow unauth\n").encode('ascii'))
        time.sleep(5)

        
        __cmdreturn = self.acessa_olt.read_very_eager()

        self.acessa_olt.write(("cd .\n").encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        # check nas no ONU pending 
        if(re.search("FHTT", str(__cmdreturn)) is None):
            return None

        __outreturn = []
        for __gt_lst in __cmdreturn.splitlines():
            g_rtn = list(filter(None, re.split(r"[\s+]", str(__gt_lst.decode('utf-8')))))

            __tmprtn = []
            if(len(g_rtn) == 11 and g_rtn[0][0].isnumeric()):
                __tmprtn.append(g_rtn[2]) # mac (fhtt)
                __tmprtn.append(g_rtn[10]) # model-full
                __tmprtn.append(g_rtn[1]) # model (simplified)
                __tmprtn.append(g_rtn[3]) # manufacturer
                __tmprtn.append(g_rtn[7]) # soft-version
                __tmprtn.append(g_rtn[8]) # hard-version
                __outreturn.append(__tmprtn)

            elif(len(g_rtn) == 10 and g_rtn[0][0].isnumeric()):
                __tmprtn.append(g_rtn[2]) # mac (fhtt)
                __tmprtn.append(g_rtn[9]) # model-full
                __tmprtn.append(g_rtn[1]) # model (simplified)
                __tmprtn.append(g_rtn[3]) # manufacturer
                __tmprtn.append(g_rtn[6]) # soft-version
                __tmprtn.append(g_rtn[7]) # hard-version
                __outreturn.append(__tmprtn)

            
        
        return __outreturn








    '''
        @doc: getUnaunthorizedOnus
        @description: get board, pon, fhtt, full-model, simply-model, hardware-version
        @input_params: None
        @output_type: multiarray
        @output_params: [[  
            ID-Board,
            ID-Pon,
            FHTT,
            Model-Full,
            Model-Simplified,
            Hardware-Version,
            Software-Version
        ]]
    '''   
    def getUnaunthorizedOnus(self):
        if not (self.__connected):
            return False


        __get_models_onus = self.getDeviceUnaunthorizedOnus()
        __get_device_onus = self.getModelUnaunthorizedOnus()


        if(__get_models_onus is None):
            return None
            
        __models_lenght = len(__get_models_onus)
        __devics_lenght = len(__get_device_onus)


        __out_arr = []

        if(__models_lenght == __devics_lenght):
            x = 0
            while(x < __models_lenght):
                __tmp_out_arr = []

                __tmp_out_arr.append(__get_models_onus[x][0]) # placa
                __tmp_out_arr.append(__get_models_onus[x][1]) # pon
                __tmp_out_arr.append(__get_models_onus[x][2]) # fhtt
                __tmp_out_arr.append(__get_device_onus[x][1]) # full-model
                __tmp_out_arr.append(__get_device_onus[x][2]) # simply-model
                __tmp_out_arr.append(__get_device_onus[x][5]) # Hardware Version
                __tmp_out_arr.append(__get_device_onus[x][4]) # Software Version

                __out_arr.append(__tmp_out_arr)

                x = x + 1
        else:
            return None

        return __out_arr


    def getUnaunthorizedOnuInfo(self, serial):
        __getOnuProvInfos = self.getUnaunthorizedOnus()
        
        if(__getOnuProvInfos is None):
            return None

        for __onu in __getOnuProvInfos:
            if(__onu[2] == serial):
                return __getOnuProvInfos[0]
        
        return None







    '''
        @doc: getOnuServiceVlans
        @description: Get onu service vlans
        @input_params: Board, Pon, Onuid
        @output_type: multiarray
        @output_params: [[
            port,
            # type,
            mode,
            vid
        ]]
    '''   
    def getOnuServiceVlans(self, board, pon, onuid):
        if not (self.__connected):
            return False

        self.acessa_olt.write(f"cd onu\ncd lan\nshow onufe_service slot {board} pon {pon} onu {onuid}\ncd .\ncd .\n".encode('ascii'))
        time.sleep(5)

        
        __cmdreturn = self.acessa_olt.read_very_eager().splitlines(True)

        __outstr = []
        for __raw_port in __cmdreturn:
            __port = __raw_port.decode('utf-8')

            if(re.search("\/[0-9]{1,16}\s+[1-9]", __port) is not None):
                __onuport = list(filter(None, re.split(r"[\s+]", __port)))

                __tmp_str = []
                __tmp_str.append(__onuport[4]) # PORT
                # __tmp_str.append(__onuport[6]) # type

                if(__onuport[7] == 'tran'):
                    __tmp_str.append("untag") # mode 
                else:
                    __tmp_str.append("tag")

                __tmp_str.append(__onuport[8]) # vid

                __outstr.append(__tmp_str)

        if not (len(__outstr)):
            return None

        return __outstr





    def isOnuBridge(self, placa, pon, onuid):
        
        if not (self.__connected):
            return False

        __getIndex = self.getOnuAuthInfo(placa, pon, onuid)

        if(type(__getIndex) == int 
            and __getIndex == -1):
            return True

        if (len(__getIndex)==0):
            return False

        if(__getIndex is None):
            return -1
        

        if(__getIndex[0].find("ITEM=0") != -1):
            return True

        if(__getIndex[4] == 'static'):
            return True
        
        return False

    def isOnuRouter(self, placa, pon, onuid):
        return not self.isOnuBridge(placa, pon, onuid)

    def getOnuWanIndex(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getIndex = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getIndex[0].find("ITEM=0") != -1):
            return -1

        return (__getIndex is not None and __getIndex[0] or None)

    def getOnuWanVlan(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getVlan = self.getOnuAuthInfo(placa, pon, onuid)
        
        if(__getVlan[0].find("ITEM=0") != -1):
            return -1

        return (__getVlan is not None and __getVlan[2] or None)

    def getOnuWanCos(self, placa, pon, onuid):

        if not (self.__connected):
            return False


        __getCos = self.getOnuAuthInfo(placa, pon, onuid) 

        if(__getCos[0].find("ITEM=0") != -1):
            return -1

        return (__getCos is not None and __getCos[3] or None)
    
    def getOnuWanMode(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getMode = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getMode[0].find("ITEM=0") != -1):
            return -1

        return (__getMode is not None and __getMode[4] or None)
    
    def getOnuWanIpAddr(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getIpaddr = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getIpaddr[0].find("ITEM=0") != -1):
            return -1

        return (__getIpaddr is not None and __getIpaddr[7] or None)
    
    def getOnuWanMask(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getMask = self.getOnuAuthInfo(placa, pon, onuid)
        
        if(__getMask[0].find("ITEM=0") != -1):
            return -1

        return (__getMask is not None and __getMask[8] or None)

    def getOnuWanGateway(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getGateway = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getGateway[0].find("ITEM=0") != -1):
            return -1

        return (__getGateway is not None and __getGateway[9] or None)

    def getOnuWanDns1(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getDNS1 = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getDNS1[0].find("ITEM=0") != -1):
            return -1

        return (__getDNS1 is not None and __getDNS1[10] or None)

    def getOnuWanDns2(self, placa, pon, onuid):

        if not (self.__connected):
            return False

        __getDNS2 = self.getOnuAuthInfo(placa, pon, onuid)

        if(__getDNS2[0].find("ITEM=0") != -1):
            return -1

        return (__getDNS2 is not None and __getDNS2[10] or None)





    '''
        @doc: isFH
        @description: Check if onu is Fiberhome manufacturer
        @input_params: Serial number (only string are allowed)
        @output_type: bool
        @output_params: True if is Fiberhome or False if not
    ''' 
    @staticmethod
    def isFH(sn):
        if not (type(sn) == str):
            return None

        if(re.search("FHTT", sn) is not None):
            return True
        else:
            return False

    def setOnuBridge(self, placa, pon, onuid, port, vlanid,vlantype='T'):
        if not (self.__connected):
            return 0

        self.acessa_olt.write(("cd onu\ncd lan\nset epon slot {} pon {} onu {} port {} service number 1\nset epon slot {} pon {} onu {} port {} service 1 vlan_mode tag 0 33024 {}\napply onu {} {} {} vlan\n".format(placa, pon, onuid, port, placa, pon, onuid, port, vlanid, placa, pon, onuid)).encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT)

        return 1
        
    def setOnuDefaultConfig(self, placa, pon, onuid, defconf=1):
        self.acessa_olt.write(f"cd onu\nreset default_cfg slot {placa} pon {pon} onu {onuid} default_cfg {defconf}\ncd .\n".encode('ascii'))
        self.acessa_olt.read_until(b"OK!", timeout = 2)

            
        time.sleep(25)

        return 1
        
    def setOnuDHCPServer(self, placa, pon, onuid, gateway_addr, netmask, dhcp_start, dhcp_end, dns1, dns2,  enabled="enable", lease=1, type='pc'):
        self.acessa_olt.write(f"cd onu\nset user_dhcp_serv_para_cfg slot {placa} pon {pon} onu {onuid} index 1 lan_ip ipv4 {gateway_addr} mask {netmask} {enabled} dhcp_pool_start ipv4 {dhcp_start} mask {netmask} dhcp_pool_end ipv4 {dhcp_end} mask {netmask} dhcp_pri_dns ipv4 {dns1} mask {netmask} dhcp_sec_dns ipv4 {dns2} mask {netmask} dhcp_gateway ipv4 {gateway_addr} mask {netmask} lease_time {lease} dhcp_pool_type {type}\napply user_dhcp_serv_para_cfg slot {placa} pon {pon} onu {onuid}\ncd .\n".encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 2)

    def setOnuDisableDHCP(self, placa, pon, onuid):
        return self.setOnuDHCPServer(placa, pon, onuid, "192.168.1.1", "24", "192.168.1.100", "192.168.1.254", "177.124.49.30", "167.250.153.222", "disable")
    
    def rebootONU(self, placa, pon, onuid):
        self.acessa_olt.write(f"cd maintenance\nreboot slot {placa} pon {pon} onu {onuid}\n".encode('ascii'))
        time.sleep(DEFAULT_TELNET_TIMEOUT + 1)
        if ('Command executes failed' in str(self.acessa_olt.read_very_eager(), 'utf-8')):
            return False
        else:
            return True

    def ConfigureOnuBridge(self, placa, pon, onuid, port, vlanid, vlantype='T', disabledhcp=True):


        self.acessa_olt.write(f"cd onu\nreset default_cfg slot {placa} pon {pon} onu {onuid} default_cfg 1\n".encode('ascii'))
        time.sleep(30)

        if(disabledhcp):
            self.acessa_olt.write(f"set user_dhcp_serv_para_cfg slot {placa} pon {pon} onu {onuid} index 1 lan_ip ipv4 192.168.1.1 mask 24 disable dhcp_pool_start ipv4 192.168.1.1 mask 24 dhcp_pool_end ipv4 192.168.1.1 mask 24 dhcp_pri_dns ipv4 1.1.1.1 mask 24 dhcp_sec_dns ipv4 8.8.8.8 mask 24 dhcp_gateway ipv4 192.168.1.1 mask 24 lease_time 1 dhcp_pool_type pc\napply user_dhcp_serv_para_cfg slot {placa} pon {pon} onu {onuid}\n".encode('ascii'))
        
        
        self.acessa_olt.write(("cd lan\nset epon slot {} pon {} onu {} port {} service number 1\nset epon slot {} pon {} onu {} port {} service 1 vlan_mode tag 0 33024 {}\napply onu {} {} {} vlan\n".format(placa, pon, onuid, port, placa, pon, onuid, port, vlanid, placa, pon, onuid)).encode('ascii'))
        
        time.sleep(1)
        return 1