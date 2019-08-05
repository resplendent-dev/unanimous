"""
pyspelling filter to eliminate words which are not in a dictionary but are not
a spelling mistake but rather are common invented words like PyPi.
"""
import codecs
import re

from pyspelling import filters


class NonWordFilter(filters.Filter):
    """Remove non-words from source"""

    @staticmethod
    def get_default_config():
        """Get default configuration."""
        return {
            'too_short': 3,
        }

    def filter(self, source_file, encoding):  # noqa A001
        """Parse text file."""

        with codecs.open(source_file, 'r', encoding=encoding) as fobj:
            text = fobj.read()
        return [filters.SourceText(
            self._filter(text), source_file, encoding, 'text'
        )]

    def _is_nonword(self, word):
        """
        Check if a word matches the non-word filter of being either too short
        or a known non-word.
        """
        too_short_config = self.config['too_short']
        return len(word) <= too_short_config

    def _filter(self, text):
        """Filter text"""
        words = re.findall("[\\w']+", text)
        result = []
        for word in words:
            if self._is_nonword(word):
                continue
            result.append(word)
        return '\n'.join(result)

    def sfilter(self, source):
        """Filter."""

        return [filters.SourceText(
            self._filter(source.text), source.context, source.encoding,
            'restructuredtext'
        )]


def get_plugin():
    """Return the filter."""

    return NonWordFilter
