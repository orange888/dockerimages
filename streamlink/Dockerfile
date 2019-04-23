# From python to support recorder script, alpine for resources as, on stream is one container
FROM python:3-alpine 

# devel is required for streamlink setup but can remove after setup
RUN apk add gcc musl-dev --no-cache \ 
	&& pip install --upgrade streamlink google-api-python-client oauth2client \ 
	&& apk del gcc musl-dev --no-cache \ 
	&& rm -Rf /tmp/* 

# Fix for the container timezone adaptation in alpine
RUN apk add tzdata

# Add recorder script from local repository to prevent external reference
ADD streamlink-recorder.py /

# Configure entrypoint with environment variable
ENTRYPOINT python ./streamlink-recorder.py -timer=${timer} -user=${user} -quality=${quality} -clientid=${clientid} -slackid=${slackid}