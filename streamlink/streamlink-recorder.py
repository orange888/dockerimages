#!/usr/bin/python

from subprocess import call
import sys
import time

streamURL = str(sys.argv[1])
streamQuality = str(sys.argv[2])
streamName = str(sys.argv[3])
streamOptions = str(sys.argv[4])

streamOptions = streamOptions.split()

streamBuilder = []
streamBuilder.append("streamlink")
for x in (0, len(streamOptions)-1):
	streamBuilder.append(str(streamOptions[x]))
streamBuilder.append(streamURL)
streamBuilder.append(streamQuality)
streamBuilder.append("-o")
streamBuilder.append("/download/"+streamName+"-"+time.strftime("%Y%m%d%H%M%S")+".mkv")

while True:
	call(streamBuilder)
	time.sleep(60)