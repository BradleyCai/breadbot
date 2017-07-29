import discordhook as dh
import sourcefinder as source
from formatter import format_discord

from datetime import datetime, date
import random, requests, logging, json
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

# Logs the results of the POST. If fails
def log(text, imgname, response):
    logging.info("Time: " + str(datetime.now()))
    logging.info("Text: " + text)
    logging.info("Image name: " + imgname)
    logging.info("HTTP response code: " + str(response.status_code))
    if response.status_code != requests.codes.ok:
        logging.error("POST didn't go through successfully")
        try:
            logging.info("JSON response: \n" + json.dumps(response.json(), indent=4))
        except(ValueError):
            logging.info("Json response: None")
    logging.info("=========================================================================================")

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

    pixiv_url, page = source.getsource(imgname)
    text = format_discord(pixiv_url, page, imgname)

    response = dh.post_img(url, img, text=text) # post image

    log(text, used_path + imgname, response) # Log the results

    img.close()

if __name__ == '__main__':
    main()
