#!/usr/bin/env python

'''
This script returns all or specified facts about your Mac.

Requirements
------------
+ OS X 10.9.x
+ python 2.7 

'''

##############################################################################
# Copyright 2014 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at  
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

import os
import re
import sys
import socket
import platform
import sysconfig
import subprocess
from AppKit import NSScreen
from CoreFoundation import CFPreferencesCopyAppValue
from SystemConfiguration import *
import objc

objc.loadBundle('CoreWLAN', 
				bundle_path='/System/Library/Frameworks/CoreWLAN.framework', 
				module_globals=globals()) 

class Facts(object):
	'''
	Facts object
	Import the module into your python script:

	from pyfacts import Facts

	fact = Facts()
	serial = fact.get_serial()
	print serial
	'''

	def __init__(self, all=False):
		self.facts = {}
		self.prefs = SCPreferencesCreate(None, 'foo', None)
		self.network_services = SCNetworkServiceCopyAll(self.prefs)	
		self.network_interfaces = SCNetworkInterfaceCopyAll()	
		self.wifi = CWInterface.interfaceNames()
		self.activenetwork = self.get_activenetwork()		
		for iname in self.wifi:
			self.interface = CWInterface.interfaceWithName_(iname)		
		if all:
			self.get_all()

	def get_all(self):
		'''Returns all facts for interactive mode'''
		self.facts['script'] = self.get_script()
		self.facts['hostname'] = self.get_hostname()
		self.facts['kernelversion'] = self.get_kernelversion()
		self.facts['productversion'] = self.get_productversion()
		self.facts['productversionmajor'] = self.get_productversionmajor()
		self.facts['productversionminor'] = self.get_productversionminor()
		self.facts['pythonversion'] = self.get_pythonversion()
		self.facts['architecture'] = self.get_architecture()
		self.facts['processor'] = self.get_processor()
		self.facts['platform'] = self.get_platform()
		self.facts['id'] = self.get_id()
		self.facts['uname'] = self.get_uname()
		self.facts['sysinfo'] = self.get_sysinfo()
		self.facts['homedir'] = self.get_home()
		self.facts['prompt'] = self.get_prompt()
		self.facts['path'] = self.get_path()
		self.facts['term'] = self.get_term()
		self.facts['term_program'] = self.get_termprogram()
		self.facts['shell'] = self.get_shell()
		self.facts['python_interpreter'] = self.get_pythoninterpreter()
		self.facts['editor'] = self.get_editor()
		self.facts['pwd'] = self.get_pwd()
		self.facts['tmpdir'] = self.get_tmpdir()
		self.facts['cwd'] = self.get_cwd()
		self.facts['euid'] = self.get_euid()
		self.facts['uid'] = self.get_uid()
		self.facts['egid'] = self.get_egid()
		self.facts['gid'] = self.get_gid()
		self.facts['groups'] = self.get_groups()
		self.facts['ip'] = self.get_ip(self.get_hostname())
		self.facts['networkinterfaces'] = self.get_networkinfacelist()
		self.facts['networkservices'] = self.get_networkservicelist()
		self.facts['wifiinterface'] = self.get_wifiinterface()
		self.facts['macaddress'] = self.get_macaddress(self.activenetwork)
		self.facts['model'] = self.get_model()
		self.facts['memory'] = self.get_memory()
		self.facts['build'] = self.get_build()
		self.facts['cpucores'] = self.get_cpucores()
		self.facts['cpus'] = self.get_cpus()
		self.facts['uuid'] = self.get_uuid()
		self.facts['serial'] = self.get_serial()
		self.facts['ssid'] = self.get_ssid()
		self.facts['wifistatus'] = self.get_wifistatus()
		self.facts['wifimacaddress'] = self.get_wifimacaddress()
		self.facts['activenetwork'] = self.get_activenetwork()
		self.facts['activepower'] = self.get_activepower()
		self.facts['batterycycles'] = self.get_batterycycles()
		self.facts['batteryhealth'] = self.get_batteryhealth()
		self.facts['batteryserial'] = self.get_batteryserial()
		self.facts['screenresolution'] = self.get_screenresolution()
		self.facts['sus'] = self.get_sus()
		self.facts['freespace'] = self.get_freespace()
		self.facts['bootcamp'] = self.get_bootcamp()
		self.facts['filevaultstatus'] = self.get_filevault()
		self.facts['gatekeeperstatus'] = self.get_gatekeeper()
		self.facts['javaversion'] = self.get_javaversion()
		self.facts['remotelogin'] = self.get_remotelogin()

	def get_script(self):
		'''Returns the name of this script'''
		return sys.argv[0]
	
	def get_hostname(self):
		'''Returns the hostname of this Mac'''
		hostname = SCDynamicStoreCopyComputerName(None, None)[0]
		#hostname = socket.gethostname()
		if not '.' in hostname:
			return hostname + '.local'
		return hostname

	def get_kernelversion(self):
		'''Returns the darwin version of this Mac
		example: 13.1.0'''
		return platform.release()

	def get_productversion(self):
		'''Returns the os x version of this Mac
		example: 10.9.2'''
		return platform.mac_ver()[0]

	def get_productversionmajor(self):
		'''Returns the major os x version of this Mac'''
		return platform.mac_ver()[0].split('.')[0] + '.' + \
									platform.mac_ver()[0].split('.')[1]

	def get_productversionminor(self):
		'''Returns the minor os x version of this Mac'''
		return platform.mac_ver()[0].split('.')[-1]

	def get_pythonversion(self):
		'''Returns the python version on this Mac'''
		return platform.python_version()

	def get_architecture(self):
		'''Returns the architecture of this Mac
		example: x86_64'''
		return platform.machine()

	def get_platform(self):
		'''Returns the processor type of this Mac
		exxample: darwin'''
		return sys.platform

	def get_id(self):
		'''Returns the current console user on this Mac'''
		return SCDynamicStoreCopyConsoleUser(None, None, None)[0]
		#return os.getlogin() 

	def get_uname(self):
		'''Returns the full uname of this Mac as a tuple'''
		return os.uname()

	def get_sysinfo(self):
		'''Returns the system info of this Mac'''
		return os.uname()[3]

	def get_home(self):
		'''Returns the home directory of the current user'''
		return os.environ['HOME']

	def get_prompt(self):
		'''Returns the prompt env of the current user'''
		try:
			return os.environ['PROMPT_COMMAND']
		except:
			return None

	def get_path(self):
		'''Returns the path env of the current user'''
		return os.environ['PATH']

	def get_term(self):
		'''Returns the term env of the current user'''
		return os.environ['TERM']

	def get_termprogram(self):
		'''Returns the term program env of the current user'''
		try:
			return os.environ['TERM_PROGRAM']
		except:
			return None

	def get_shell(self):
		'''Returns the shell env of the current user'''
		return os.environ['SHELL']

	def get_pythoninterpreter(self):
		'''Returns the python interpreter on this Mac'''
		return os.environ['VERSIONER_PYTHON_VERSION']

	def get_editor(self):
		'''Returns the editor env of the current user'''
		return os.environ['EDITOR']

	def get_pwd(self):
		'''Returns the pwd'''
		try:
			return os.environ['PWD']
		except:
			return None

	def get_tmpdir(self):
		'''Returns the tempdir env of the current user'''
		try:
			return os.environ['TMPDIR']
		except:
			return None

	def get_cwd(self):
		'''Returns the cwd'''
		return os.getcwd()

	def get_euid(self):
		'''Returns the euid of the current user'''
		return os.geteuid()

	def get_uid(self):
		'''Returns the uid of the current user'''
		return SCDynamicStoreCopyConsoleUser(None, None, None)[1]
		#return os.getuid()

	def get_egid(self):
		'''Returns the egid of the current user'''
		return os.getegid()

	def get_gid(self):
		'''Returns the gid of the current user'''
		return SCDynamicStoreCopyConsoleUser(None, None, None)[2]
		#return os.getgid()

	def get_groups(self):
		'''Returns the groups of the current user'''
		return os.getgroups()

	def get_ip(self, hostname):
		'''Returns the IP address of the Mac'''
		return socket.gethostbyname(hostname)

	def get_networkservicelist(self):
		'''Returns a list of all network interface names'''
		d = {}	
		for service in self.network_services:
			d[SCNetworkServiceGetName(service)] = SCNetworkServiceGetEnabled(service)
		return d

	def get_networkinfacelist(self):
		'''Returns a list of all network interface names'''
		d = {}	
		for interface in self.network_interfaces:
			d[SCNetworkInterfaceGetLocalizedDisplayName(interface)] = (
				SCNetworkInterfaceGetBSDName(interface),
				SCNetworkInterfaceGetHardwareAddressString(interface)
				)
		return d

	def get_wifiinterface(self):
		'''Returns the name of the Wi-Fi network interface'''
		interface = self.get_networkinfacelist()
		return interface['Wi-Fi'][0]

	# def get_wifiinterface(self):
	# 	return self.interface.interfaceName()

	def get_wifimacaddress(self):
		'''Returns the MAC address of the Wi-Fi network interface'''
		interface = self.get_networkinfacelist()
		return interface['Wi-Fi'][1]

	# def get_wifimacaddress(self):
	# 	return self.interface.hardwareAddress()

	def get_wifistatus(self):
		'''Returns the wifi status
		Yes or No'''		
		if self.interface.powerOn() == 1:
			return "Yes"
		return "No"

	def get_ssid(self):
		return self.interface.ssid()		

	def get_serial(self):
	    '''Returns the serial number of the Mac'''
	    cmd = "/usr/sbin/ioreg -c \"IOPlatformExpertDevice\" | awk -F '\"' \
	    							'/IOPlatformSerialNumber/ {print $4}'"
	    serial = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, 
	    							stdout=subprocess.PIPE).communicate()[0]
	    return serial.strip()

	def get_activepower(self):
		cmd = "/usr/bin/pmset -g | grep \* | /usr/bin/awk '{$NF=\"\"; print $0}'"
		power = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return power.strip()

	def get_batterycycles(self):
		cmd = "/usr/sbin/ioreg -r -c \"AppleSmartBattery\" | \
									/usr/bin/awk '/\"CycleCount\"/{print $3}'"
		cycles = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return cycles.strip()

	def get_batteryhealth(self):
		cmd = "/usr/sbin/ioreg -r -c \"AppleSmartBattery\" | \
							/usr/bin/awk '/PermanentFailureStatus/{print $3}'"
		health = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		if int(health.strip()) == 0:
			return "Healthy"
		return "Failing"

	def get_batteryserial(self):
		cmd = "/usr/sbin/ioreg -r -c \"AppleSmartBattery\" | /usr/bin/awk '/BatterySerialNumber/{NF;print $3}'"
		serial = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return re.split('[\s"]+',serial.strip())[1]

	def get_freespace(self):
		cmd = "/usr/sbin/diskutil info / | /usr/bin/awk '/Free Space/{print $4}'"
		free = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return free.strip()

	def get_bootcamp(self):
		cmd = "/usr/sbin/diskutil list | grep -c \"Microsoft Basic Data\""
		bootcamp = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		if int(bootcamp.strip()) == 0:
			return 'No'
		return 'Yes'

	def get_filevault(self):
		cmd = ['/usr/bin/fdesetup', 'status']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.strip()

	def get_gatekeeper(self):
		cmd = ['/usr/sbin/spctl', '--status']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.strip()

	def get_activenetwork(self):
		cmd = "netstat -rn | /usr/bin/awk  '/^default/{print $6;exit}'"
		interface = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return interface.strip()

	def get_macaddress(self, interface):
		'''Returns the MAC address of the current active network'''
		cmd = ['/usr/sbin/networksetup', '-getmacaddress', interface]
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(' ')[2]

	def get_model(self):
		'''Returns the hardware model of the Mac'''
		cmd = ['/usr/sbin/sysctl', 'hw.model']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(' ')[1].strip()

	def get_memory(self):
		'''Returns the memory in GBs of the Mac'''
		cmd = ['/usr/sbin/sysctl', 'hw.memsize']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return int(stdout.split(' ')[1].strip())/1024/1024/1024

	def get_processor(self):
		'''Returns the processor model of the Mac'''
		cmd = ['/usr/sbin/sysctl', 'machdep.cpu.brand_string']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(': ')[1].strip()

	def get_build(self):
		'''Returns the os build version of the Mac'''
		cmd = ['/usr/sbin/sysctl', 'kern.osversion']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(': ')[1].strip()
	
	def get_cpucores(self):
		'''Returns how many CPU cores on the Mac'''
		cmd = ['/usr/sbin/sysctl', 'hw.ncpu']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(': ')[1].strip()

	def get_cpus(self):
		'''Returns how many CPUs on the Mac'''
		cmd = ['/usr/sbin/sysctl', 'hw.physicalcpu']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(': ')[1].strip()		

	def get_uuid(self):
		'''Returns the UUID of the Mac'''
		cmd = ['/usr/sbin/sysctl', 'kern.uuid']
		(stdout, stderr, rc) = self.run_cmd(cmd)
		return stdout.split(': ')[1].strip()

	def get_screenresolution(self):
		width = NSScreen.mainScreen().frame().size.width
		height = NSScreen.mainScreen().frame().size.height
		return [width, height]

	def get_sus(self):
		sus = CFPreferencesCopyAppValue('CatalogURL', '/Library/Preferences/com.apple.SoftwareUpdate.plist')
		if not sus:
			return None
		return sus

	def get_javaversion(self):
		cmd = "java -version 2>&1 | /usr/bin/awk '/version/{print $3}'"
		serial = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
									stdout=subprocess.PIPE).communicate()[0]
		return re.split('[\s"]+',serial.strip())[1]

	def get_remotelogin(self):
		if os.geteuid() == 0:
			cmd = "/usr/sbin/systemsetup -getremotelogin | /usr/bin/awk '{print $3}'"
			remotelogin = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
										stdout=subprocess.PIPE).communicate()[0]
			return remotelogin.strip()
		return "run as root to check this setting"

	def get(self, key):
		'''Returns a single fact for interactive mode'''
		try:
			return self.facts[key]
		except KeyError:
			print 'Error: key not found'
			sys.exit(1)

	def show_all(self):
		'''Returns all facts for interactive mode'''
		try:
			for k, v in sorted(self.facts.items()):
				print "%s: %s" % (k, v)
		except KeyError:
			print "Error: %s" % KeyError			

	def list_all(self):
		'''Lists all fact categories for interactive mode'''
		try:
			for k, v in sorted(self.facts.items()):
				print "%s" % k
		except KeyError:
			print "Error: %s" % KeyError		

	def run_cmd(self, cmd):
		"""Runs a command and returns a tuple of stdout, stderr, returncode."""
		task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE)
		(stdout, stderr) = task.communicate()
		return stdout, stderr, task.returncode

def usage():
	print 'Usage: ./pyfacts.py <key>'

def main():
	'''Runs in interactive mode'''
	if len(sys.argv) > 2:
		usage()
		sys.exit(0)
	facts = Facts(all=True)
	if len(sys.argv) == 1:
		facts.show_all()
	elif len(sys.argv) == 2:
		if sys.argv[1] == '-h' or sys.argv[1] == 'help':
			usage()
			print '\nCategories:\n----------'
			facts.list_all()
			sys.exit(0)
		print facts.get(sys.argv[1])

if __name__ == "__main__":
	main()
