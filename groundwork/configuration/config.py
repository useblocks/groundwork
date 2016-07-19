import logging


class Config:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def get(self, name, default=None):
        return getattr(self, name, default)

    def set(self, name, value, overwrite=False):
        if hasattr(self, name):
            if overwrite:
                setattr(self, name, value)
            else:
                self.log.warning("Configuration parameter %s exists and overwrite not allowed" % name)
        else:
            setattr(self, name, value)
        return getattr(self, name)

