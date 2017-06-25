# Posts an image with an optional caption
def post_img(url, img, text=None):
    payload = {'content': text}
    files = {'file': img}

    if text == None:
        return requests.post(url, files=files)
    else:
        return requests.post(url, data=payload, files=files)

# Posts text
def post_text(url, text):
    return requests.post(url, data={'content': text})
