FROM python:3-alpine 

RUN apk add gcc musl-dev --no-cache \ 
	&& pip install --upgrade streamlink google-api-python-client oauth2client \ 
	&& apk del gcc musl-dev --no-cache \ 
	&& rm -Rf /tmp/* 

RUN apk add tzdata

ADD streamlink-recorder.py /

ENTRYPOINT python ./streamlink-recorder.py -timer=${timer} -user=${user} -quality=${quality} -clientid=${clientid}