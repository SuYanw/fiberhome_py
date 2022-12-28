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