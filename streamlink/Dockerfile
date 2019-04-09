FROM python

RUN pip install --upgrade --user streamlink
RUN pip install ffmpeg
	
ADD streamlink-recorder.py /

CMD python ./streamlink-recorder.py ${streamLink} ${streamQuality} ${streamName} ${streamOptions}