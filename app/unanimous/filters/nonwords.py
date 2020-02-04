"""
pyspelling filter to eliminate words which are not in a dictionary but are not
a spelling mistake but rather are common invented words like PyPi.
"""
import codecs
import re

from pyspelling import filters
from wcmatch import glob

from unanimous.custom_nonwords import get_custom_wordlist
from unanimous.store import get_current_non_words


class NonWordFilter(filters.Filter):
    """Remove non-words from source"""

    def __init__(self, options, **kwargs):
        super().__init__(options, **kwargs)
        self.non_words = get_current_non_words()
        for target in self.config.get("wordlist", []):
            for match in glob.iglob(
                target, flags=glob.N | glob.B | glob.G | glob.S | glob.O
            ):
                self.non_words.update(get_custom_wordlist(match))

    @staticmethod
    def get_default_config():
        """Get default configuration."""
        return {"too_short": 3, "wordlist": []}

    def filter(self, source_file, encoding):  # noqa A001
        """Parse text file."""

        with codecs.open(source_file, "r", encoding=encoding) as fobj:
            text = fobj.read()
        return [filters.SourceText(self._filter(text), source_file, encoding, "text")]

    def _is_nonword(self, word):
        """
        Check if a word matches the non-word filter of being either too short
        or a known non-word.
        """
        too_short_config = self.config["too_short"]
        too_short_check = len(word) <= too_short_config
        if too_short_check:
            return True
        lword = word.lower()
        non_word_check = lword in self.non_words
        if non_word_check:
            return True
        return False

    def _filter(self, text):
        """Filter text"""
        words = re.findall("[A-Za-z']+", text)
        result = []
        for word in words:
            if self._is_nonword(word):
                continue
            result.append(word)
        return "\n".join(result)

    def sfilter(self, source):
        """Filter."""

        return [
            filters.SourceText(
                self._filter(source.text), source.context, source.encoding, "text"
            )
        ]


def get_plugin():
    """Return the filter."""

    return NonWordFilter
