class Icon:
    type: str = None
    icon: str = None

    def __init__(self, icon: str = None):
        self.type = self.__class__.__name__[:-4].lower()
        self.icon = icon


class EmojiIcon(Icon):
    pass


class LinkIcon(Icon):
    pass
