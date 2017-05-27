"""
Base class of all sources.
"""

from abc import ABCMeta, abstractmethod

class Source(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def fetch_new(self):
        """
        Fetch new resources.
        """

    def fetch_all(self):
        """
        Fetch a ton of resources to initialize the databse.
        If this function is not implementated, well, just fetch new ones.
        """
        fetch_new()
