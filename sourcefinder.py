from source import source
import re

def getsource(imgname):
    pixiv_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    twitter_url = 'https://www.twitter.com'
    danbooru_url = 'https://danbooru.donmai.us/posts'

    # Try for a Pixiv match (ex: 28022143_p0.jpg)
    m = re.match(r'(\d{7,9})_?p(\d{1,3})', imgname)
    if m:
        img_id = m.group(1)
        url = pixiv_url + img_id
        page = m.group(2)

        return source(
            'pixiv', url=url, img_id=img_id, img_name=imgname, page=page)

    # Try for a mobile Pixiv match  (ex: illust_51503473_20170620_040102.jpg)
    m = re.match(r'illust_(\d{7,9})_\d{8}_\d{6}', imgname)
    if m:
        img_id = m.group(1)
        url = pixiv_url + img_id

        return source(
            'pixiv', url=url, img_id=img_id, img_name=imgname, page='?')

    # Try for a Twitter match (ex. twitter-HitenKei-885477467594530816)
    m = re.match(r'twitter-(\w+)-(\d+)', imgname)
    if m:
        artist = m.group(1)
        img_id = m.group(2)
        url = '{}/{}/status/{}'.format(twitter_url, artist, img_id)

        return source(
            'twitter', url=url, artist=artist, img_id=img_id, img_name=imgname)

    # Try for a Danbooru match (ex. danbooru-none-2789021)
    m = re.match(r'danbooru-(\w+)-(\w+)', imgname)
    if m:
        artist = m.group(1)
        img_id = m.group(2)
        url = '{}/{}'.format(danbooru_url, img_id)

        return source(
            'danbooru', url=url, artist=artist, img_id=img_id, img_name=imgname)

    # Try for an 'other' match (ex. other-website-artist-111111)
    m = re.match(r'other-(\w+)-(\w+)-(\w+)', imgname)
    if m:
        return source('other', \
            url=m.group(1), \
            artist=m.group(2), \
            img_id=m.group(3), \
            img_name=imgname)

    # if there is no match, then the file doesn't have a recorded source
    return source('none', img_name=imgname)
