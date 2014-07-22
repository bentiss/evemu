#!/usr/bin/env python
# Parses linux/input.h scanning for #define KEY_FOO 134
# Prints a C header file or a Python file that can be used as
# mapping table
#

# Make sure the print statement is disabled and the function is used.
from __future__ import print_function

import argparse
import re
import sys
import textwrap

SOURCE_FILE = "/usr/include/linux/input.h"

class Bits(object):
	pass

prefixes = [
		"EV_",
		"REL_",
		"ABS_",
		"KEY_",
		"BTN_",
		"LED_",
		"SND_",
		"MSC_",
		"SW_",
		"FF_",
		"SYN_",
		"INPUT_PROP_",
]

blacklist = [
		"EV_VERSION",
		"BTN_MISC",
		"BTN_MOUSE",
		"BTN_JOYSTICK",
		"BTN_GAMEPAD",
		"BTN_DIGI",
		"BTN_WHEEL",
		"BTN_TRIGGER_HAPPY"
]

def p(s):
	print(textwrap.dedent(s))

def print_bits(bits, prefix):
	if  not hasattr(bits, prefix):
		return
	print("static const char * const %s_map[%s_MAX + 1] = {" % (prefix, prefix.upper()))
	print("	[0 ... %s_MAX] = NULL," % prefix.upper())
	for val, name in getattr(bits, prefix).items():
		print("	[%s] = \"%s\"," % (name, name))
	print("};")
	print("")

def print_python_bits(bits, prefix):
	if  not hasattr(bits, prefix):
		return

	print("%s_map = {" % (prefix))
	for val, name in getattr(bits, prefix).items():
		print("	%d : \"%s\", \"%s\" : %d," % (val, name, name, val))
	print("}")
	print("")

def print_map(bits):
	print("static const char * const * const map[EV_MAX + 1] = {")
	print("	[0 ... EV_MAX] = NULL,")

	for prefix in prefixes:
		if prefix == "BTN_" or prefix == "EV_" or prefix == "INPUT_PROP_":
			continue
		print("	[EV_%s] = %s_map," % (prefix[:-1], prefix[:-1].lower()))

	print("};")
	print("")

def print_python_map(bits):
	print("map = {")

	for val, name in getattr(bits, "ev").items():
		name = name[3:]
		if name == "REP" or name == "PWR"  or name == "FF_STATUS"  or name == "MAX":
			continue
		print("	%d : %s_map," % (val, name.lower()))

	print("}")
	print("")

def print_mapping_table(bits):
	p("""
	/* THIS FILE IS GENERATED, DO NOT EDIT */

	#ifndef EVENT_NAMES_H
	#define EVENT_NAMES_H

	#define SYN_MAX 3 /* linux/input.h doesn't define that */

	""")

	for prefix in prefixes:
		if prefix == "BTN_":
			continue
		print_bits(bits, prefix[:-1].lower())

	print_map(bits)

	p("""
	static const char * event_get_type_name(int type) {
		return ev_map[type];
	 }

	static const char * event_get_code_name(int type, int code) {
		return map[type] ? map[type][code] : NULL;
	}

	#endif /* EVENT_NAMES_H */
	""")

def print_python_mapping_table(bits):
	p("""# THIS FILE IS GENERATED, DO NOT EDIT")
	""")

	for prefix in prefixes:
		if prefix == "BTN_":
			continue
		print_python_bits(bits, prefix[:-1].lower())

	print_python_map(bits)

	p("""
	def event_get_type_name(type):
		return ev_map[type]


	def event_get_code_name(type, code):
		try:
			return map[type][code]
		except KeyError:
			return 'UNKNOWN'
	""")

def parse_define(bits, line):
	m = re.match(r"^#define\s+(\w+)\s+(\w+)", line)
	if m == None:
		return

	name = m.group(1)

	if name in blacklist:
		return

	try:
		value = int(m.group(2), 0)
	except ValueError:
		return

	for prefix in prefixes:
		if not name.startswith(prefix):
			continue

		attrname = prefix[:-1].lower()
		if attrname == "btn":
			attrname = "key"

		if not hasattr(bits, attrname):
			setattr(bits, attrname, {})
		b = getattr(bits, attrname)
		b[value] = name

def parse(path):
	fp = open(path)

	bits = Bits()

	lines = fp.readlines()
	for line in lines:
		if not line.startswith("#define"):
			continue
		parse_define(bits, line)

	return bits

if __name__ == "__main__":
	bits = parse(SOURCE_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("--output", default="c")

	args = parser.parse_args(sys.argv[1:])
	if args.output == "python":
		print_python_mapping_table(bits)
	else:
		print_mapping_table(bits)
