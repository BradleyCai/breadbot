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
