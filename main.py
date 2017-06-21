import requests
import os, time, random, re, sys

# Returns the path and image name as an array
def getimage():
    unused_path = "./imgs/unused/"
    used_path = "./imgs/used/"

    dirlist = os.listdir(unused_path)

    if (len(dirlist) > 0):
        imgname = random.choice(dirlist)
    else:
        print("Ran out of images")
        sys.exit()

    os.rename(unused_path + imgname, used_path + imgname)

    return [used_path, imgname]

# Has two returns. If a pixiv source is found, returns the pixiv url and the page
# If no source is found, returns None and None
def getsource(imgname):
    pixiv_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='

    m = re.match(r'.*(\d{7,9})_?p(\d{1,3})', imgname)

    if m:
        return pixiv_url + m.group(1), m.group(2)
    else:
        return None, None

def format_source(pixiv_url, page):
    if (pixiv_url == None):
        return "**No source**"

    res = "**Source: **" + pixiv_url

    if (page != "0"):
        res += "\n**Page: **" + page

    return res

# Posts an image with an optional caption
def post_img(url, img, text=None):
    payload = {'content': text}
    files = {'file': img}

    if text == None:
        requests.post(url, files=files)
    else:
        requests.post(url, data=payload, files=files)

# Posts text
def post_text(url, text):
    requests.post(url, data={'content': text})

def main():
    random.seed(time.time())
    url = 'https://discordapp.com/api/webhooks/326506189796147201/ezbjsocncvzrtvbkbxe0-_mqqvos5jxgnxnxlv90h20adidjc25syrxppvo53mwwdeor'

    imgname = getimage()
    img = open(imgname[0] + imgname[1], "rb")

    pixiv_url, page = getsource(imgname[1])
    text = format_source(pixiv_url, page)
    text += "\n**Original file name: **" + imgname[1]

    print(text, imgname)
    post(text, img)

    img.close()

if __name__ == '__main__':
    main()
