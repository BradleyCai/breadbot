class source:
    def __init__(self, name, url=None, artist=None, img_id=None, img_name=None, page=None):
        self.name = name
        self.url = url
        self.artist = artist
        self.img_id = img_id
        self.img_name = img_name
        self.page = page

    def format_discord(self):
        if self.name == 'pixiv':
            return self.pixiv_format()
        elif self.name == 'twitter':
            return self.twitter_format()
        elif self.name == 'danbooru':
            return self.danbooru_format()
        elif self.name == 'other':
            return self.other_format()
        else:
            return '**No source found.**\n**Original filename: **`{}`'.format(self.img_name)

    def pixiv_format(self):
        res = '**Source: **<{}>'.format(self.url)

        if self.page == None:
            res += '\n**Page: ** Page unknown'
        elif self.page != '0':
            res += '\n**Page: **' + str(int(self.page) + 1)

        return res

    def twitter_format(self):
        res = '**Source: **<{}>'.format(self.url)
        res += '\n**Artist: **@' + self.artist

        return res

    def danbooru_format(self):
        res = '**Source: **<{}>'.format(self.url)
        if self.artist != None:
            res += '\n**Artist: **' + self.artist

        return res

    def other_format(self):
        res = '**Source website: **{}'.format(self.url)
        if self.artist != None:
            res += '\n**Artist: **' + self.artist
        if self.img_name != None:
            res += '\n**Original filename: **`{}`'.format(self.img_name)

        return res
