#!/usr/bin/env python3
import filelister, sourcefinder, discordhook, source
from logger import log

import random, logging, json, argparse, datetime
import os, time, sys

def main():
    # Set up commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='specify name of server', type=str)
    parser.add_argument('botsdir', nargs='?', default='bots', help='bot directory other than ./bots', type=str)
    parser.add_argument('filesdir', nargs='?', default='bots/files', help='files directory other than ./bots/files', type=str)
    parser.add_argument('queuedir', nargs='?', default='bots/queue', help='queue directory other than ./bots/queue', type=str)
    args = parser.parse_args()

    config_name = os.path.join(args.botsdir, args.name + '.json')
    filesdir = os.path.join(args.filesdir)
    queuedir = os.path.join(args.queuedir)

    random.seed(time.time())

    # initalize logging
    if not os.path.exists('logs/'):
        print('Making a logs folder')
        os.mkdir('logs/')
    logging.basicConfig(filename='logs/' + str(datetime.date.today()), level=logging.DEBUG)

    if not os.path.exists(config_name):
        print('Configuration file doesn\'t exist for the server you specified! Use filelister.py to create one')
        sys.exit(1)

    with open(config_name, 'r') as config_file:
        config = json.load(config_file)
        hook_id = config['hook_id']
        hook_token = config['hook_token']

    with open(config_name, 'r+') as config_file:
        imgname = filelister.getfile(config_file)

    imgpath = os.path.join(filesdir, imgname)
    with open(imgpath, "rb") as img:
        imgsource = sourcefinder.getsource(imgname)
        text = imgsource.format_discord()
        response = discordhook.post_img(hook_id, hook_token, img, text=text)

    log(text, imgpath, response) # Log the results

if __name__ == '__main__':
    main()
