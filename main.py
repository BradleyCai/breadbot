import discordhook as dh

from datetime import datetime, date
import random, re, requests, logging
import os, time, sys

# Returns a random image in unused_path, moves it to used_path, and returns the
# image name
def getimage(unused_path, used_path):
    dirlist = os.listdir(unused_path)

    if len(dirlist) < 0:
        return None

    imgname = random.choice(dirlist)
    os.rename(unused_path + imgname, used_path + imgname)

    return imgname

# Tries to find source of the image
# For now, only supports images saved from pixiv
def getsource(imgname):
    return get_pixiv_source(imgname)

def get_pixiv_source(imgname):
    pixiv_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='

    # Match computer saved links (ex: 28022143_p0.jpg)
    m = re.match(r'(\d{7,9})_?p(\d{1,3})', imgname)
    if m:
        return pixiv_url + m.group(1), m.group(2)

    # Match mobile saved links (ex: illust_51503473_20170620_040102.jpg)
    m = re.match(r'illust_(\d{7,9})_\d{8}_\d{6}', imgname)
    if m:
        return pixiv_url + m.group(1), '?' # page is not saved in link name

    return None, None

# Creates a suitable message about the image to send to discord
def format_source(source_url, page, imgname):
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
    url = 'https://discordapp.com/api/webhooks/326506189796147201/EZbjsoCNCvzRtVbKBXe0-_mQQVos5JXgNxNxlv90h20ADIdJc25SyrXpPvo53mwwDeor'
    unused_path = "./imgs/unused/"
    used_path = "./imgs/used/"

    logging.basicConfig(filename='logs/' + str(date.today()), level=logging.DEBUG)

    random.seed(time.time())
    imgname = getimage(unused_path, used_path)
    if imgname == None:
        logging.warning("Ran out of images")
        sys.exit(1)
    img = open(used_path + imgname, "rb")

    pixiv_url, page = getsource(imgname)
    text = format_source(pixiv_url, page, imgname)

    response = str(dh.post_img(url, img, text=text)) # post image

    logging.info("Time: " + str(datetime.now()))
    logging.info("Text: " + text)
    logging.info("Image name:" + used_path + imgname)
    logging.info("POST response: " + response)
    logging.info("=========================================================================================")

    img.close()

if __name__ == '__main__':
    main()
