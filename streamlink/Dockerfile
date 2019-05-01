# From python to support recorder script, alpine for resources as, on stream is one container
FROM python:3-alpine 

# Fix for the container timezone adaptation in alpine
RUN apk add tzdata

# devel is required for streamlink setup but can remove after setup
RUN apk add gcc musl-dev linux-headers --no-cache

# linux-headers is required for psutil
RUN apk add linux-headers --no-cache

# install streamlinks and dependencies
RUN pip install --upgrade streamlink google-api-python-client oauth2client

# install psutil to control processes
RUN pip install --upgrade psutil

# cleanup built environment
RUN apk del gcc musl-dev linux-headers --no-cache
RUN rm -Rf /tmp/*

# Add recorder script from local repository to prevent external reference
ADD streamlink-recorder.py /

# Configure entrypoint with environment variables (only user is mandatory)
ENTRYPOINT python ./streamlink-recorder.py -user=${user} -timer=${timer} -quality=${quality} -clientid=${clientid} -slackid=${slackid}