#!/usr/bin/python

import os
import shutil
import time
import sys
import argparse
import os.path
import subprocess
import threading
import ConfigParser


class CinderErrors(object):
	'''
	Inject cinder configuration error
	'''
	cinder_config = "/etc/cinder/cinder.conf"
  

	def stop_cinder_service(self):
            output= os.popen("sudo service cinder-volume stop").read()
	    if 'cinder-volume stop/waiting' not in output:
	        print ('Something Went Wrong, Could not able to stop Cinder-Volume:', output)
	    

	def start_cinder_service(self):
           output= os.popen("sudo service cinder-volume start").read()
	   if 'cinder-volume start/running' not in output:
	       print ('Something Went Wrong, Could not able to start Cinder-Volume:', output)
	   
	
        def restart_cinder_service(self):
            output= os.popen("sudo service cinder-volume restart").read()
	    if 'cinder-volume start/running' not in output:
	        print ('Something Went Wrong, Could not able to Restart Cinder-Volume:', output)
	
        def is_cinder_service_running(self):

		return true;
  
  
        def bad_3par_credential(self, badUserName, badPassword):
            #print "Injecting bad 3par credential"
            badCredential={'hp3par_username' : badUserName, 'hp3par_password' : badPassword}
            self.inject_error_in_cinder_configuration(badCredential,"3PAR-THEVERSE-FC")
        
        
        def bad_3par_iscsi_ips(self, badIscsiIps):
            #print "Injecting bad 3par credential"
            hp3parbadIscsiIps={'hp3par_iscsi_ips' : badIscsiIps}
            self.inject_error_in_cinder_configuration(hp3parbadIscsiIps,"3PAR-THEVERSE")    
            

        def bad_3par_cpg(self, badCpg):
            #print "Injecting bad 3par cpg"
            badCpg={'hp3par_cpg' : badCpg}
            self.inject_error_in_cinder_configuration(badCpg,"3PAR-THEVERSE-FC")
            
        def bad_3par_ws_url(self, badWsUrl):
            #print "Injecting bad 3par cpg"
            
             try :  
                cmnd = "yes | sudo -H pip  uninstall hp3parclient"
                os.popen(cmnd)
                time.sleep(5)
                self.restart_cinder_service();
                time.sleep(15)
                
            
            
             finally: # catch *all* exceptions
                os.popen("git clone https://github.com/hp-storage/python-3parclient.git")
                os.popen("sudo mv python-3parclient/hp3parclient/ /usr/local/lib/python2.7/dist-packages/")
                badWsUrlDic={'hp3par_api_url' : badWsUrl}
                self.inject_error_in_cinder_configuration(badWsUrlDic,"3PAR-THEVERSE-FC")
            
          
            
        def missing_package_3parclient(self):
            self.inject_cinder_missing_package_error('hp3parclient')
        
        def missing_package_sg3utils(self):
            try :  
                cmnd = "sudo apt-get --assume-yes remove sg3-utils" 
                os.popen(cmnd)
                  
            finally: # catch *all* exceptions
                time.sleep(20) 
                #self.restart_cinder_service();
        
        def available_package_sg3utils(self):
            try :  
                cmnd = "sudo apt-get --assume-yes install sg3-utils" 
                os.popen(cmnd)
                  
            finally: # catch *all* exceptions
                time.sleep(15)   
        def missing_package_sysfsutils(self):
            try :  
                cmnd = "sudo apt-get --assume-yes remove sysfsutils" 
                os.popen(cmnd)
                  
            finally: # catch *all* exceptions
                time.sleep(20) 
                #self.restart_cinder_service();
        
        def available_package_sysfsutils(self):
            try :  
                cmnd = "sudo apt-get --assume-yes install sysfsutils" 
                os.popen(cmnd)
                  
            finally: # catch *all* exceptions
                time.sleep(15)          
        
       
       
#...................................Common Functions........................................................................       
       
        def inject_cinder_missing_package_error(self, package_name) :
            try :  
                cmnd = "yes | sudo -H pip  uninstall " + package_name
                os.popen(cmnd)
                time.sleep(5)
                self.restart_cinder_service();
                time.sleep(15)
            
            except: # catch *all* exceptions
                          print sys.exc_info()[0]    
            finally :
                # Install package again
                cmnd = "yes | sudo -H pip install " + package_name
                os.popen(cmnd)
                time.sleep(5)
                self.restart_cinder_service();
        
        def inject_nova_missing_package_error(self, package_name) :
            try :  
                cmnd = "yes | sudo -H pip  uninstall " + package_name
                os.popen(cmnd)
                time.sleep(5)
                self.restart_cinder_service();
                time.sleep(15)
            
            except: # catch *all* exceptions
                          print sys.exc_info()[0]    
            finally :
                # Install package again
                cmnd = "yes | sudo -H pip install " + package_name
                os.popen(cmnd)
                time.sleep(5)
                self.restart_cinder_service();

   
        def inject_error_in_cinder_configuration(self , dict, section) :

	   if os.path.isfile(self.cinder_config):
	
                backup_cinder_config= self.cinder_config +".origin"
		os.rename(self.cinder_config , backup_cinder_config)
                try :
                  
                   config = ConfigParser.RawConfigParser(allow_no_value=True)
                   config.read(backup_cinder_config)
                   if config.has_section(section):
                      for key in dict.keys():
                          config.set(section,key,dict.get(key))
                   else :
                      print "Cinder conf does not cotanin the 3PAR configuration "
                   # Writing our configuration file to 'cinder.conf'
                   with open(self.cinder_config, 'w') as configfile:
                        config.write(configfile)
                   self.restart_cinder_service();
                   time.sleep(15)
                except: # catch *all* exceptions
                          print sys.exc_info()[0]
                 
                finally :
                    
                    if os.path.isfile(self.cinder_config):
                       os.remove(self.cinder_config) 
  	               os.rename(backup_cinder_config , self.cinder_config)    
  	            if os.path.isfile(backup_cinder_config):
                       os.rename(backup_cinder_config , self.cinder_config) 
                    self.restart_cinder_service();
           else :
                 print "No file present : " + self.cinder_config





#...........................................................Log Capture.............................................................................................................

cinder_log_path = '/var/log/cinder/temp.log'
# To verify the string we just keeping log in temprary file and checking if error message is logged or not 
class LogCapture(threading.Thread):
        

        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                log_write_cmd = 'tail -f /var/log/cinder/cinder-volume.log >> /var/log/cinder/temp.log'
                global proc
                proc = subprocess.Popen(log_write_cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        def terminate_thread(self):
                try:
                        proc.terminate()
                except:
                        raise
        def cleanup(self):
            if os.path.isfile(cinder_log_path):
                os.remove(cinder_log_path)

#...........................................................Log Verify.............................................................................................................

class LogVerify:
        

        def __init__(self, log):
                self.log = log

        def check_log_for_bad_3par_credential(self):
                cmd = "grep 'Forbidden (HTTP 403) 5 - invalid username or password' " +cinder_log_path
                proc = subprocess.Popen (cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
                line = proc.stdout.readlines()
                isInjected = False
                for error in line:
                        if 'Forbidden (HTTP 403) 5 - invalid username or password' in error:
                                print "Error bad_3par_credential Injected Successfully "
                                print  line
                                isInjected = True
                                break
                if not isInjected :
                  print "Error bad_3par_credential Injected UnSuccessfully "
                    
        def check_log_for_bad_3par_cpg(self):

                cmd1 = '''grep "Invalid input received: CPG (badcpg) doesn't exist on array" ''' +cinder_log_path
                proc = subprocess.Popen (cmd1, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
                line = proc.stdout.readlines()
                isInjected = False
                for error in line:
                        if "Invalid input received: CPG (badcpg) doesn't exist on array" in error:
                                print "Error bad_3par_cpg Injected Successfully "
                                print  line
                                isInjected = True
                                break
                if not isInjected :
                  print "Error bad_3par_cpg Injected UnSuccessfully "              

        def check_log_for_missing_package_3parclient(self):
            cmnd = '''grep "You must install hp3parclient before using 3PAR drivers" ''' + cinder_log_path
            proc = subprocess.Popen(cmnd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            lines = proc.stdout.readlines()
            isInjected = False
            for errLine in lines:
                if "You must install hp3parclient before using 3PAR drivers" in errLine:
                    print "Error missing_package_3parclient Injected Successfully "
                    print errLine
                    isInjected = True
                    break
            if not isInjected :
                print "Error missing_package_3parclient Injected UnSuccessfully "
        
        def check_log_for_bad_3par_iscsi_ips(self):
            cmnd = '''grep "Invalid input received: At least one valid iSCSI IP address must be set" ''' + cinder_log_path
            proc = subprocess.Popen(cmnd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            lines = proc.stdout.readlines()
            isInjected = False
            for errLine in lines:
                if "Invalid input received: At least one valid iSCSI IP address must be set" in errLine:
                    print "Error bad_3par_iscsi_ips Injected Successfully "
                    print errLine
                    isInjected = True
                    break
            if not isInjected :
                print "Error bad_3par_iscsi_ips Injected UnSuccessfully "
                 



#....................................Command Line argument......................................................................
parser = argparse.ArgumentParser(usage="./ErrorInjection.py [options]...\nExecute'\n")
parser.add_argument("--debug", dest="debug", action="store_true", help="List out given params")
# Errors
parser.add_argument("--bad_3par_credential", dest="bad_3par_credential", action="store_true", help="inject 3par bad credential")
parser.add_argument("--bad_3par_cpg", dest="bad_3par_cpg", action="store_true", help="inject 3par bad cpg")
parser.add_argument("--missing_package_3parclient", dest="missing_package_3parclient", action="store_true",
                        help="inject missing package 3parclient")
parser.add_argument("--bad_3par_iscsi_ips", dest="bad_3par_iscsi_ips", action="store_true",
                        help="Inject error 3par bad iscsi ips") 
parser.add_argument("--bad_3par_ws_url", dest="bad_3par_ws_url", action="store_true",
                        help="Inject error bad 3par ws url")   
parser.add_argument("--missing_package_sg3utils", dest="missing_package_sg3utils", action="store_true",
                        help="Inject error missing package sg3utils")  
parser.add_argument("--available_package_sg3utils", dest="available_package_sg3utils", action="store_true",
                        help="Install missing package sg3utils")                      
parser.add_argument("--missing_package_sysfsutils", dest="missing_package_sysfsutils", action="store_true",
                        help="Inject error missing package sysfsutils")  
parser.add_argument("--available_package_sysfsutils", dest="available_package_sysfsutils", action="store_true",
                        help="Install missing package sysfsutils")  
#................................................ Start Injection..................................................................
log = LogCapture()
log.start()
log_verify = LogVerify(1)
cinder = CinderErrors()
args = parser.parse_args()

if len(sys.argv) > 1:
#  error = sys.argv[1]
  if args.bad_3par_credential :
     cinder.bad_3par_credential("bad3paradm","bad3pardata")
     log_verify.check_log_for_bad_3par_credential()

  elif args.bad_3par_cpg :
     cinder.bad_3par_cpg("badcpg")
     log_verify.check_log_for_bad_3par_cpg()
  
  elif args.missing_package_3parclient :
     cinder.missing_package_3parclient()
     log_verify.check_log_for_missing_package_3parclient()   
  
  elif args.bad_3par_iscsi_ips :
     cinder.bad_3par_iscsi_ips("10.250.100.220555555555:3260")
     log_verify.check_log_for_bad_3par_iscsi_ips()
  
  elif args.bad_3par_ws_url :
     cinder.bad_3par_ws_url("https://theverse.cxo.sdsdsadhp.com:8080/api/v1")
  
  elif args.missing_package_sg3utils :
     cinder.missing_package_sg3utils()  
  
  elif args.available_package_sg3utils :
     cinder.available_package_sg3utils()   
  
  elif args.missing_package_sysfsutils :
     cinder.missing_package_sysfsutils()  
  
  elif args.available_package_sysfsutils :
     cinder.available_package_sysfsutils()        
  else : 
    print ' Error Injection does not support : ' + sys.argv[1]
cinder.restart_cinder_service()
log.terminate_thread()
log.cleanup()
#................................................ End Injection..................................................................
