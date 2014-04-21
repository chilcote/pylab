#!/usr/bin/env python

"""
pyscreenrez.py

Reference:
https://gist.github.com/gregneagle/5722568
https://github.com/Tonyliu2ca/ScreenResolution/blob/master/screenresolution.m

Apple Docs: 
https://developer.apple.com/library/mac/#documentation/graphicsimaging/reference/Quartz_Services_Ref/Reference/reference.html
https://developer.apple.com/library/mac/#documentation/graphicsimaging/Conceptual/QuartzDisplayServicesConceptual/Introduction/Introduction.html#//apple_ref/doc/uid/TP40004316
"""

import sys, os
import Quartz

mode = ''

def get_screen_resolution():
	mainMonitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
	return (mainMonitor.size.width, mainMonitor.size.height)

def get_main_display():
	return Quartz.CGMainDisplayID()

def get_active_displays():
	max_displays = 2
	(err, active_displays, number_of_active_displays) = Quartz.CGGetActiveDisplayList(max_displays, None, None)
	return active_displays

def get_display_modes(display):
	return Quartz.CGDisplayCopyAllDisplayModes(display, None)

def set_screen_resolution(mode, display):
	(err, config_ref) = Quartz.CGBeginDisplayConfiguration(None)
	if err:
		print >> sys.stderr, "Error with CGBeginDisplayConfiguration: %s" % err
		exit(-1)

	# this is the part I need to figure out
	# Need to pass the correct mode (1024 x 768 @ 60)
	err = Quartz.CGConfigureDisplayWithDisplayMode(config_ref, mode, display, None)
	if err:
		print >> sys.stderr, "Error with CGConfigureDisplayWithDisplayMode: %s" % err
		exit(-1)

	err = Quartz.CGCompleteDisplayConfiguration(config_ref, Quartz.kCGConfigurePermanently)
	if err:
		print >> sys.stderr, ("Error with CGCompleteDisplayConfiguration: %s" % err)
		exit(-1)

def main():
	screensize = get_screen_resolution()
	display = get_main_display()
	active_displays = get_active_displays()
	mode_list = get_display_modes(display)

	print 'Main Display: %s' % display
	print 'Active Displays: %s' % active_displays[0]
	print 'Resolution: %s, %s' % screensize

	# for mode in mode_list:
	# 	print mode

	# set_screen_resolution(mode, display)

if __name__ == '__main__':
    main()