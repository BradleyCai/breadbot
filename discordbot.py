import discordhook as discord
import sourcefinder as source
import filelister
from logger import log

import random, logging, json
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
    bot_name = sys.argv[1]
    logging.basicConfig(filename='logs/' + str(date.today()), level=logging.DEBUG)
    random.seed(time.time())

    with open('./bots/test.json', 'r') as config_file:
        config = json.load(config_file)
        hook_id = config['hook_id']
        hook_token = config['hook_token']

    with open('./bots/test.json', 'r+') as config_file:
        imgname = filelister.getfile(config_file)

    if imgname == None:
        logging.warning('Ran out of images')
        sys.exit(1)

    with open('./bots/files/' + imgname, "rb") as img:
        pixiv_url, page = source.getsource(imgname)
        text = format_discord(pixiv_url, page, imgname)
        response = discord.post_img(hook_id, hook_token, img, text=text)

    log(text, './bots/files' + imgname, response) # Log the results

if __name__ == '__main__':
    main()
