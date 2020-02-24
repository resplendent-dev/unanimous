"""
Exposed utility calls
"""

def is_nonword(word, lowercase_only=True, too_short_check=3):
    """
    Utility call to check a word is a non-word
    """
    if lowercase_only and not word.islower():
        return True
    too_short_result = len(word) <= too_short_check
    if too_short_result:
        return True
    lword = word.lower()
    non_word_check = lword in self.non_words
    if non_word_check:
        return True
    return False


