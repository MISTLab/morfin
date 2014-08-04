# -*- coding: utf-8 -*-
#"""
#Created on Wed Jul 16 16:24:58 2014
#
#@author: Vedant@MIST Lab
#"""
import multiprocessing
import spacepy
CPUcount = multiprocessing.cpu_count()
spacepy.config['ncpus'] =1
import spacepy.time as spt
import spacepy.coordinates as spc
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import os,math
import spacepy.irbempy as ir
from ConfigParser import SafeConfigParser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import numpy as np
#import time as T

def cls():
    os.system(['clear','cls'][os.name == 'nt'])


def time_proc(ite):
    
    time = parser.get('mission_parameters', 'Time')
    t=spt.Ticktock(time, 'ISO')
    o_sect=float(parser.get('simulation_preferences','Orbit_Sections'))
    Total_T=float(parser.get('simulation_preferences','Simulation_Duration'))    
    L2 = parser.get('mission_parameters', 'TLE_Line2')
    num_orb_day=float(L2[52:])     
    Ilim= round(Total_T*o_sect*num_orb_day)    
    DelT=round(Total_T*24*60*60/Ilim)
    t=spt.Ticktock((t.TAI+(DelT*ite)),'TAI')
    t=t.convert('ISO')
    time=str(t.UTC[0])
    year=int(time[0:4])
    month=int(time[5:7])
    day=int(time[8:10])
    hour=int(time[11:13])
    minute=int(time[14:16])
    second=int(time[17:19])
    print "Constructing Lookup: "+str(ite)+"/"+str(Ilim)
    if ite<Ilim:
        bol=True
    else:
        bol=False
    return year,month,day,hour,minute,second,time,bol
    
def L_para(T_E):
    
    L1 = parser.get('mission_parameters', 'TLE_Line1')
    L2 = parser.get('mission_parameters', 'TLE_Line2')
    satellite = twoline2rv(L1, L2, wgs72)
    position, velocity = satellite.propagate(T_E[0],T_E[1],T_E[2],T_E[3],T_E[4],T_E[5])    
    Re= [x/6371 for x in position] 
    spaco = spc.Coords(Re, 'GEI', 'car')
    spaco.ticks=spt.Ticktock([T_E[6]], 'ISO')
    q=[90]
    L=ir.get_Lm(spaco.ticks,spaco,q,extMag='T01STORM',intMag='IGRF') 
    return satellite.alta*6371,satellite.altp*6371,math.degrees(satellite.inclo),L.items()[2][1][0][0]
        
def Check_Error():
    
    All=driver.page_source
    if (All.find("We're sorry,but there seems to be an error...")<0):
        print "File created successfully"  
        return True        
    else:
        print "Error in creating current File"
        return False
def login(usr):
   
   key=parser.get('creme96', 'password')
   driver.get(base_url + "/CREME-MC/login_form")
   driver.find_element_by_id("__ac_name").clear()
   driver.find_element_by_id("__ac_name").send_keys(usr)
   driver.find_element_by_id("__ac_password").clear()
   driver.find_element_by_id("__ac_password").send_keys(key)
   driver.find_element_by_name("submit").click()
   data=driver.page_source    
   if(data.find("You are now logged in")<0):
       print"Unsuccessful login, try again!!"
       return False
   else:
       print "Login Successful"
       return True
     
def Work_folder_create(folder_name,usr):
    
    print ('Creating Work Folder:(1/8)')
    driver.get(base_url + "/CREME-MC/Members/"+usr)
    driver.find_element_by_xpath("//li[2]/dl/dt/a").click()
    driver.implicitly_wait(30)
    driver.find_element_by_xpath("//li[4]/a/span").click()
    driver.implicitly_wait(30)
    driver.find_element_by_xpath("//input[@id='title']").clear()
    driver.find_element_by_xpath("//input[@id='title']").send_keys(folder_name)
    driver.find_element_by_xpath("//input[@name='form.button.save']").click()
    if(driver.current_url=="https://creme.isde.vanderbilt.edu/CREME-MC/Members/vedant_fno/"+folder_name.lower()+"/"):   
        print "Done!"
        return True
    else:
        return False

def Work_folder_delete(folder_name,usr):
    
    print ('Deleting Work Folder:(8/8)')    
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/folder_contents") 
    i_d="//input[@id='cb_"+folder_name+"']"
    driver.find_element_by_xpath(i_d).click()
    driver.find_element_by_xpath("//input[@name='folder_delete:method']").click()                       
    print "Done!"

def TRP_form(folder_name,usr,sat_dat):

    print ('Submiting TRP form:(2/8)')       
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/Trp") 
    driver.find_element_by_xpath("//ol[@id='OrbitalParameters']/li[3]/input").click()
    driver.find_element_by_id("apogee").clear()
    driver.find_element_by_id("apogee").send_keys(str(sat_dat[0]))
    driver.find_element_by_id("perigee").clear()
    driver.find_element_by_id("perigee").send_keys(str(sat_dat[1]))
    driver.find_element_by_id("inclination").clear()
    driver.find_element_by_id("inclination").send_keys(str(sat_dat[2]))
    driver.find_element_by_id("initialLongitude").clear()
    driver.find_element_by_id("initialLongitude").send_keys("0")
    driver.find_element_by_id("initialDisplacement").clear()
    driver.find_element_by_id("initialDisplacement").send_keys("0")
    driver.find_element_by_id("displacementOfPerigee").clear()
    driver.find_element_by_id("displacementOfPerigee").send_keys("0")
    Select(driver.find_element_by_id("numberOfOrbits")).select_by_visible_text("50")
    driver.find_element_by_xpath("//ul[@id='sections_ul']/li[2]/input").click()
    driver.find_element_by_id("lValues").clear()
    driver.find_element_by_id("lValues").send_keys(str(sat_dat[3]))
    driver.find_element_by_id("rootname").clear()
    driver.find_element_by_id("rootname").send_keys("SELTEST")
    driver.find_element_by_xpath("(//input[@name='model_index'])[2]").click()
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source    
    if(data.find("File \"SELTEST\" has been created successfully")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True
    
    
def GTRN_form(folder_name,usr,sat_dat):
    
    print ('Submiting GTRN form:(3/8)')    
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/Gtrn")
    driver.find_element_by_xpath("//ol[@id='OrbitalParameters']/li[3]/input").click()
    driver.find_element_by_id("apogee").clear()
    driver.find_element_by_id("apogee").send_keys(str(sat_dat[0]))
    driver.find_element_by_id("perigee").clear()
    driver.find_element_by_id("perigee").send_keys(str(sat_dat[1]))
    driver.find_element_by_id("inclination").clear()
    driver.find_element_by_id("inclination").send_keys(str(sat_dat[2]))
    driver.find_element_by_id("initialLongitude").clear()
    driver.find_element_by_id("initialLongitude").send_keys("0")
    driver.find_element_by_id("initialDisplacement").clear()
    driver.find_element_by_id("initialDisplacement").send_keys("0")
    driver.find_element_by_id("displacementOfPerigee").clear()
    driver.find_element_by_id("displacementOfPerigee").send_keys("0")
    driver.find_element_by_xpath("//ul[@id='sections_ul']/li[2]/input").click()
    driver.find_element_by_id("lValues").clear()
    driver.find_element_by_id("lValues").send_keys(str(sat_dat[3]))
    driver.find_element_by_id("rootname").clear()
    driver.find_element_by_id("rootname").send_keys("SELTEST")
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source    
    if(data.find("File \"SELTEST\" has been created successfully")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True    
   
def FLUX_form(folder_name,usr):
    print ('Submiting FLUX form:(4/8)')    
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/Flux")
    driver.find_element_by_id("z2").clear()
    driver.find_element_by_id("z2").send_keys("92")
    driver.find_element_by_id("version").click()
    driver.find_element_by_id("model").click()
    driver.find_element_by_xpath("//div[@id='region-content']/div[2]/form/fieldset/ol/li[4]/div/input[2]").click()
    driver.find_element_by_id("gtrnFileId_button").click()
    h=driver.window_handles
    driver.switch_to_window("filebrowser_popup")
    driver.find_element_by_xpath("//tr[1]/td[3]/a").click()
    driver.switch_to_window(h[0])
    driver.find_element_by_id("aveTrpFileId_clear").click()
    driver.find_element_by_id("aveTrpFileId_button").click()
    driver.switch_to_window("filebrowser_popup")
    driver.find_element_by_xpath("//tr[1]/td[3]/a").click()
    driver.switch_to_window(h[0])
    driver.find_element_by_id("rootname").clear()
    driver.find_element_by_id("rootname").send_keys("SELTEST")
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source    
    if(data.find("Flux File Preview")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True    
    
def TRANS_form(folder_name,usr):

    print ('Submiting TRANS form:(5/8)')
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/Trans")
    driver.find_element_by_id("fluxFileId_button").click()
    driver.switch_to_window("filebrowser_popup")
    h=driver.window_handles    
    driver.find_element_by_xpath("//tr[3]/td[3]/a/strong").click()
    driver.switch_to_window(h[0])
    driver.find_element_by_name("thickness").clear()
    driver.find_element_by_name("thickness").send_keys(str(parser.get('FPGA_Parameters', 'shilding_thickness')))
    driver.find_element_by_id("rootname").clear()
    driver.find_element_by_id("rootname").send_keys("SELTEST")
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source    
    if(data.find("Transmitted Flux File Preview")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True 
       
def LETSPEC_form(folder_name,usr):

    print ('Submiting LETSPEC form:(5/8)')    
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/LetSpec")
    driver.find_element_by_id("fluxFileId_button").click()
    driver.switch_to_window("filebrowser_popup")
    h=driver.window_handles
    driver.find_element_by_xpath("//tr[3]/td[3]/a/strong").click()
    driver.switch_to_window(h[0])
    driver.find_element_by_id("z2").clear()
    driver.find_element_by_id("z2").send_keys("92")
    driver.find_element_by_id("rootname").clear()
    driver.find_element_by_id("rootname").send_keys("SELTEST")
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source       
    if(data.find("LET Spectrum file preview")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True 
    
def HUP_form(folder_name,usr):

    print ('Submiting HUP form:(6/8)')
    driver.get(base_url + "/CREME-MC/Members/"+usr+"/"+folder_name+"/Hup")
    driver.find_element_by_id("letFileId_button").click()
    driver.switch_to_window("filebrowser_popup")
    h=driver.window_handles
    driver.find_element_by_xpath("//tr[1]/td[3]/a/strong").click()
    driver.switch_to_window(h[0])
    driver.find_element_by_id("jobName").clear()
    driver.find_element_by_id("jobName").send_keys("SELTEST")
    driver.find_element_by_id("label0").clear()
    driver.find_element_by_id("label0").send_keys("FPGA")
    driver.find_element_by_id("rppx0").clear()
    driver.find_element_by_id("rppx0").send_keys(parser.get('FPGA_Parameters', 'X'))
    driver.find_element_by_id("rppy0").clear()
    driver.find_element_by_id("rppy0").send_keys(parser.get('FPGA_Parameters', 'Y'))
    driver.find_element_by_id("rppz0").clear()
    driver.find_element_by_id("rppz0").send_keys(parser.get('FPGA_Parameters', 'Z'))
    driver.find_element_by_id("onset0").clear()
    driver.find_element_by_id("onset0").send_keys(parser.get('FPGA_Parameters', 'Wiebull_onset'))
    driver.find_element_by_id("width0").clear()
    driver.find_element_by_id("width0").send_keys(parser.get('FPGA_Parameters', 'Wiebull_width'))
    driver.find_element_by_id("exponent0").clear()
    driver.find_element_by_id("exponent0").send_keys(parser.get('FPGA_Parameters', 'Wiebull_exponent'))
    driver.find_element_by_id("limitingXS0").clear()
    driver.find_element_by_id("limitingXS0").send_keys(parser.get('FPGA_Parameters', 'Wiebull_LimitingXS'))
    driver.find_element_by_name("form.button.submit").click()
    data=driver.page_source     
    if(data.find("File \"SELTEST.hup\" has been created sucessfully")<0):
       return False
       print "Unsuccessful...Trying Again!"
    else:
       print "Done!"
       return True

def adding_to_LUT(DAT):
    
    print ('Adding to Look-up File:(7/8)')
    data=driver.page_source
    data=data[data.find("SEE")+78:data.find("SEE")+137]
    Fobj=open("data.txt",'a')
    DAT=" ".join(str(x) for x in DAT)
    Fobj.writelines(DAT+" "+data+"\n")
    print(DAT+" "+data)
    Fobj.close()
    print "Done!"

driver = webdriver.Chrome()
parser = SafeConfigParser()
parser.read('inputs.ini')
base_url = "https://creme.isde.vanderbilt.edu/"
F_name=parser.get('creme96', 'folder_name')
user=parser.get('creme96', 'user')
Condition=True
Iteration_count=0
L_range=[]
while(Condition):
    spacepy.config['ncpus'] =1
    cls()
    Time_elements=time_proc(Iteration_count)
    LUT_data=L_para(Time_elements)
    spacepy.config['ncpus'] = CPUcount
    L_range.append(abs(LUT_data[3]))
    Condition=Time_elements[7]
    Iteration_count+=1 
L_range=np.linspace(min(L_range),max(L_range),5)
Iteration_count=0
spacepy.config['ncpus'] =1
cls()
Time_elements=time_proc(Iteration_count)
LUT_data=list(L_para(Time_elements))
spacepy.config['ncpus'] = CPUcount
login(user)

while Iteration_count<len(L_range):
    LUT_data.pop()
    LUT_data.append(L_range[Iteration_count]) 
    f_res=False
    while not f_res:
        f_res=Work_folder_create(F_name,user)
    F_Name=F_name.lower()
    f_res=False
    while not f_res:
        f_res=TRP_form(F_Name,user,LUT_data)    
    f_res=False
    while not f_res:
        f_res=GTRN_form(F_Name,user,LUT_data)
    f_res=False
    while not f_res:
        f_res=FLUX_form(F_Name,user) 
    f_res=False
    while not f_res:
        f_res=TRANS_form(F_Name,user)    
    f_res=False
    while not f_res:
        f_res=LETSPEC_form(F_Name,user)
    f_res=False
    while not f_res:
        f_res=HUP_form(F_Name,user)
    adding_to_LUT(LUT_data)
    Work_folder_delete(F_Name,user)
    Iteration_count+=1
driver.close()