FROM python

RUN pip install --upgrade streamlink progressbar33 google-api-python-client oauth2client
ADD streamlink-recorder.py /

ENTRYPOINT python ./streamlink-recorder.py -timer=${timer} -user=${user} -quality=${quality} -clientid=${clientid}