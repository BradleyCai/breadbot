import requests

# Posts an image with an optional caption
def post_img(url, img, text=None):
    if text == None:
        return requests.post(url, files={'file': img})
    else:
        return requests.post(url, data={'content': text}, files={'file': img})

# Posts text
def post_text(url, text):
    return requests.post(url, data={'content': text})
