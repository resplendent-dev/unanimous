"""
Exposed utility calls
"""

from unanimous.store import get_current_non_words


class NonWords:  # pylint: disable=too-few-public-methods
    """
    Cache of non-words
    """

    non_words = set()


def is_nonword(
    word,
    lowercase_only=True,
    too_short_check=3,
    exclude_apostrophe=True,
    extra_non_words=None,
):
    """
    Utility call to check a word is a non-word
    """
    if lowercase_only and not word.islower():
        return True
    if exclude_apostrophe and "'" in word:
        return True
    too_short_result = len(word) <= too_short_check
    if too_short_result:
        return True
    lword = word.lower()
    if not NonWords.non_words:
        NonWords.non_words = set(get_current_non_words())
    non_word_check = lword in NonWords.non_words
    if non_word_check:
        return True
    if extra_non_words is not None:
        non_word_check = lword in extra_non_words
        if non_word_check:
            return True
    return False
