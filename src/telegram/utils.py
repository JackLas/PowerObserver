import time
import os
import pathlib
import argparse
import sys
import json
import datetime

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    args = parser.parse_args()

    if not args.config:
        sys.exit(-1)

    with open(args.config) as config:
        return json.load(config)

def get_token(path=""):
    if not path:
        path = os.path.join(pathlib.Path(__file__).parent.resolve(), "token.txt")
    
    with open(path) as tokenfile:
        return tokenfile.readline()

def time_now():
    return int(time.time())

def convert_duration(seconds):
    return str(datetime.timedelta(seconds=seconds))

def convert_date(epoch_int):
    return time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(epoch_int))