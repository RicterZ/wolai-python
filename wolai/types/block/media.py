from wolai.types.block import Block


class MediaBlock(Block):
    link: str = None
    caption: str = None

    def __init__(self, link: str = None, caption: str = None, **kwargs):
        if self.__class__.__name__ == 'MediaBlock':
            raise Exception('MediaBlock class cannot be used directly')
        self.link = link
        self.caption = caption
        super().__init__(**kwargs)

        # TODO: wolai's response data
        if 'media' in kwargs:
            self.link = kwargs['media'].get('url', None)


class ImageBlock(MediaBlock):
    pass


class AudioBlock(MediaBlock):
    pass


class VideoBlock(MediaBlock):
    pass
