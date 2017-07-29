import re

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
