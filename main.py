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

# Has two returns. If a pixiv source is found, returns the pixiv url and the page
# If no source is found, returns None and None
def getsource(imgname):
    pixiv_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='

    m = re.match(r'(\d{7,9})_?p(\d{1,3})', imgname)

    if m:
        return pixiv_url + m.group(1), m.group(2)
    else:
        m = re.match(r'illust_(\d{7,9})_\d{8}_\d{6}', imgname)

        if m:
            return pixiv_url + m.group(1), "0"

    return None, None

# Formats the source name for discord
def format_source(source_url, page):
    if source_url == None:
        return "**No source**"

    res = "**Source: **<" + source_url + ">"

    if page != "0":
        res += "\n**Page: **" + str(int(page) + 1)

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
    text += "\n**Original filename: **" + imgname

    logging.info("Time: " + str(datetime.now()))
    logging.info("Text: " + text)
    logging.info("Image name:" + used_path + imgname)
    logging.info("POST response: " + str(dh.post_img(url, img, text=text)))
    logging.info("=========================================================================================")

    img.close()

if __name__ == '__main__':
    main()
