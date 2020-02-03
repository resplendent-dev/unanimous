"""Test text plugin."""
from spellingtest.check import PluginTestCase


class TestNonWordFilter(PluginTestCase):
    """Check non-words are allowed."""

    bad_words1 = ["helo", "begn"]

    def setup_fs(self):
        """Setup files."""

        good_words = [
            "yes",
            "word",
            "wyx",
            "hl",
            "wa",
            "ai",
            "x",
            "y",
            "zx",
            "sexualized",
        ]
        exclude_words = ["hujibuki", ""]
        self.bad_words1 = ["helo", "begn"]
        self.mktemp(
            "test1.txt",
            "\n".join(self.bad_words1 + good_words + exclude_words),
            "utf-8",
        )
        self.mktemp("spelling_wordlist.txt", "\n".join(exclude_words), "utf-8")

        config = self.dedent(
            """
            matrix:
            - name: name
              group: group1
              default_encoding: utf-8
              sources:
              - '{temp}/**/test1.txt'
              aspell:
                lang: en
              hunspell:
                d: en_AU
              pipeline:
              - unanimous.filters.nonwords:
                  too_short: 1
              - unanimous.filters.nonwords:
                  too_short: 3
                  wordlist:
                  - '{temp}/spelling_wordlist.txt'
            """
        ).format(temp=self.tempdir)
        self.mktemp(".source.yml", config, "utf-8")

    def test_all(self):
        """Test all."""
        self.assert_spellcheck(".source.yml", self.bad_words1)
