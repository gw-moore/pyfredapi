from .base import FredBase


class FredSources(FredBase):
    def get_sources(self):
        raise NotImplementedError

    def get_source(self):
        raise NotImplementedError

    def get_source_release(self):
        raise NotImplementedError
