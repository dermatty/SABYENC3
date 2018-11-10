#!/home/stephan/.virtualenvs/nntp/bin/python

'''
This is example code how to use 'sabyenc' to decode yencoded articles (used on Usenet)

More info on sabyenc:
https://pypi.python.org/pypi/sabyenc
https://github.com/sabnzbd/sabyenc
'''

import sabyenc	# sudo -H pip install sabyenc --upgrade (after: sudo apt-get install python-dev)
import yenc
import sys
import re
import time

# print("Version of sabyenc on this system:", sabyenc.__version__)

# See if an input file (with yencoded info) was given as argument
try:
	inputfilename = sys.argv[1]
	print("Reading from", inputfilename)
	with open (inputfilename, "r") as myfile:
		data=myfile.readlines()
except:
	# No input, so use a pre-fab yencoded file / string, just like you get the BODY (or ARTICLE) from a newsserver
	# source: http://nzbindex.com/search/?q=verysmallfile+2384928394820394

	data = [b'=ybegin line=128 size=173 name=smallfile.rar\r\n', 
		b'|\x8b\x9cKD1*\xf9\xba\x9d**7*******\xcb\xfb\x9eJ\xaa[*\x8b***\x8b***-MW\xe5\xb8\x8e\x92\x95s>Z;*\xde\xab**\x9e\x8f\x9d\x9eW[ZZ\x8c\xa3\x9e\x8f\x9dX\x93\x97\x91\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x94\r\n', 
		b'4\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x9444\xeeg\xa5*j1*\r\n', 
		b'=yend size=173 crc32=8828b45c\r\n']

print("\nINPUT:")
print("First Line", data[0].rstrip())
print("Last Line", data[-1].rstrip())

bytes0 = bytearray()
for d in data[1:-1]:
        bytes0.extend(d)
t0_yenc = time.time()
for i in range(10000000):
        _, decodedcrc32, decoded = yenc.decode(bytes0)
dt_yenc = time.time() - t0_yenc
print(decoded)

# Find size in laste line of yencoded message:
lastline = data[-1].decode()	# For example: '=yend size=173 crc32=8828b45c\r\n' (and ... assuming it's in the last line)
m = re.search('size=(.\d+?) ', lastline)
if m:
    size = int(m.group(1))
print( "size of decoded info will be", size)

# Now do the yencode-decoding using sabyenc:
t0_sabyenc = time.time()
for i in range(10000000):
        decoded_data, output_filename, crc, crc_yenc, crc_correct = sabyenc.decode_usenet_chunks(data, size)
dt_sabyenc = time.time() - t0_sabyenc

print("\nOUTPUT:")

#print "decoded_data, first 20 bytes (Warning: probably binary stuff!):\n", decoded_data[:20]
print("decoded_data -> length:", len(decoded_data))
print("output_filename:", output_filename)
print("crc:", crc)
print("crc_yenc:", crc_yenc)
print("crc_correct:", crc_correct)

print("\nsabyenc writing to:", output_filename, dt_sabyenc)
file = open(output_filename, "wb")
file.write(decoded_data)
file.close()

output_filename_yenc = "yenc_smallfile.rar"
print("\nyenc writing to:", output_filename_yenc, dt_yenc)
file = open(output_filename_yenc, "wb")
file.write(decoded)
file.close()

print("yenc: " + "-" *20)
print(decoded)

print("sabyenc: " + "-" *20)
print(decoded_data)

print()
print("Diff %: ", 1 - dt_sabyenc/dt_yenc)
print("Done")

