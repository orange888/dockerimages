# From python to support recorder script, alpine for resources as, on stream is one container
FROM python:3.7-alpine as base

FROM base as builder
# devel is required for streamlink setup but can remove after setup
RUN apk add gcc musl-dev --no-cache
RUN mkdir /install
WORKDIR /install
RUN pip install --install-option="--prefix=/install" --upgrade streamlink google-api-python-client oauth2client

FROM base
# Fix for the container timezone adaptation in alpine
RUN apk add tzdata
COPY --from=builder /install /usr/local
# Add recorder script from local repository to prevent external reference
ADD streamlink-recorder.py /

# Configure entrypoint with environment variables (only user is mandatory)
ENTRYPOINT python ./streamlink-recorder.py -user=${user} -timer=${timer} -quality=${quality} -clientid=${clientid} -slackid=${slackid}