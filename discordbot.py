import filelister, sourcefinder, discordhook, source
from logger import log

import random, logging, json, argparse, datetime
import os, time, sys

# Creates a suitable message about the image to send to discord
def format_discord(source_url, page, imgname):
    if source_url == None:
        res = '**No source**'
    else:
        res = '**Source: **<' + source_url + '>'

        if page == '?':
            res += '\n**Page: ** Page unknown'
        elif page != '0':
            res += '\n**Page: **' + str(int(page) + 1)

    res += '\n**Original filename: **`' + imgname + '`'

    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='specify name of server', type=str)
    args = parser.parse_args()
    random.seed(time.time())
    config_name = './bots/{}.json'.format(args.name)

    # initalize logging
    if not os.path.isdir('logs/'):
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

    with open('./bots/files/' + imgname, "rb") as img:
        imgsource = sourcefinder.getsource(imgname)
        text = imgsource.format_discord()
        response = discordhook.post_img(hook_id, hook_token, img, text=text)

    log(text, './bots/files/' + imgname, response) # Log the results

if __name__ == '__main__':
    main()
