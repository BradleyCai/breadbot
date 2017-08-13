import requests

discord_api_url = 'https://discordapp.com/api/webhooks'

# Posts an image with an optional caption
def post_img(hook_id, hook_token, img, text=None):
    if text == None:
        return requests.post('{}/{}/{}'.format(discord_api_url, hook_id, hook_token), files={'file': img})
    else:
        return requests.post('{}/{}/{}'.format(discord_api_url, hook_id, hook_token), data={'content': text}, files={'file': img})

# Posts text
def post_text(hook_id, hook_token, text):
    return requests.post('{}/{}/{}'.format(discord_api_url, hook_id, hook_token), data={'content': text})
