class Cover:
    type: str = None
    url: str = None

    def __init__(self, url: str = None):
        self.type = self.__class__.__name__[:-4].lower()
        self.url = url


class LinkCover(Cover):
    pass

