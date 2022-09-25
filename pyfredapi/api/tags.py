from .base import FredBase


class FredTags(FredBase):
    def get_tags(self):
        raise NotImplementedError

    def get_related_tags(self):
        raise NotImplementedError

    def get_tag_series(self):
        raise NotImplementedError
