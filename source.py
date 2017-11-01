class source:
    def __init__(self, name, url=None, artist=None, img_id=None, img_name=None, page=None):
        self.name = name
        self.url = url
        self.artist = artist if artist != 'none' else None
        self.img_id = img_id
        self.img_name = img_name
        self.page = page if page != None else '?'

    # Source formatting function for discord
    def format_discord(self):
        res = ''

        if self.name == None:
            return '**No source found.**\n**Original filename: **`{}`'.format(self.img_name)

        # Source link or website
        if self.name == 'other':
            res += '**Source website: **{}'.format(self.url)
        else:
            res += '**Source: **<{}>'.format(self.url)

        # Pixiv page number or artist name
        if self.name == 'pixiv':
            if self.page == '?':
                res += '\n**Page: ** Page unknown'
            elif self.page != '0':
                res += '\n**Page: **' + str(int(self.page) + 1)
        else:
            if self.artist != None:
                # Include an @ if source is from twitter
                twitAt = '@' if self.name == 'twitter' else ''
                res += '\n**Artist: **' + twitAt + self.artist

        # Filename if source is from 'other'
        if self.name == 'other':
            res += '\n**Original filename: **`{}`'.format(self.img_name)

        return res
