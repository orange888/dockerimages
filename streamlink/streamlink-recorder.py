# This script checks if a user on twitch is currently streaming and then records the stream via streamlink
import json
import subprocess
import datetime
import threading
import argparse
import httplib2
import re

import requests
import json
import os

from urllib.request import urlopen
from urllib.error import URLError
from threading import Timer

from apiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.clientsecrets import InvalidClientSecretsError
from oauth2client.file import Storage

# Init variables with some default values
timer = 30
user = ""
quality = "best"
client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"
slack_id = ""

# Init variables with some default values
def post_to_slack(message):
    if slack_id is None:
        print("slackid is not specified, so disabling slack notification")
        pass

    slack_url = "https://hooks.slack.com/services/" + slack_id
    slack_data = {'text': message}

    response = requests.post(
        slack_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    global info
    url = 'https://api.twitch.tv/kraken/streams/' + user + '?client_id=' + client_id
    try:
        info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
        if info['stream'] is None:
            status = 1
        else:
            status = 0
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status

def loopcheck():
    status = check_user(user)
    if status == 2:
        print("username not found. invalid username?")
    elif status == 3:
        print("unexpected error. maybe try again later")
    elif status == 1:
        print(user, "currently offline, checking again in", timer, "seconds")
    elif status == 0:
        filename = user + " - " + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + " - " + (info['stream']).get("channel").get("status") + ".mp4"
        
        # clean filename from unecessary characters
        filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])
        recorded_filename = os.path.join("/download/", filename)
        
        # start streamlink process
        post_to_slack("recording " + user+" ...")
        print(user, "recording ... ")
        retcode = subprocess.call(["streamlink", "--twitch-disable-hosting", "--retry-max", "5", "--retry-streams", "60", "twitch.tv/" + user, quality, "-o", recorded_filename])
        print("Stream is done. Queuing upload if necessary and going back to checking.. retcode is:", retcode)
        post_to_slack("Stream "+ user +" is done. Queuing upload if necessary and going back to checking..")

    t = Timer(timer, loopcheck)
    t.start()

def main():
    global timer
    global user
    global quality
    global client_id
    global slack_id

    parser = argparse.ArgumentParser()
    parser.add_argument("-timer", help="Stream check interval (less than 15s are not recommended)")
    parser.add_argument("-user", help="Twitch user that we are checking")
    parser.add_argument("-quality", help="Recording quality")
    parser.add_argument("-clientid", help="Your twitch app client id")
    parser.add_argument("-slackid", help="Your slack app client id")
    args = parser.parse_args()

    if args.timer is not None:
        timer = int(args.timer)
    if args.user is not None:
        user = args.user
    if args.quality is not None:
        quality = args.quality
    if args.slackid is not None:
        slack_id = args.slackid

    if args.clientid is not None:
        client_id = args.clientid
    
    if client_id is None:
        print("Please create a twitch app and set the client id with -clientid [YOUR ID] aaa")
        return

    print("Checking for", user, "every", timer, "seconds. Record with", quality, "quality.")
    loopcheck()


if __name__ == "__main__":
    # execute only if run as a script
    main()