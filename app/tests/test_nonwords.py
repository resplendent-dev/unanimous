"""Test text plugin."""
from . import util


class TestNonWordFilter(util.PluginTestCase):
    """Check non-words are allowed."""

    def setup_fs(self):
        """Setup files."""

        good_words = ["yes", "word", "zx"]
        self.bad_words1 = ["zxq", "helo", "begn"]
        self.mktemp("test1.txt", "\n".join(self.bad_words1 + good_words), "utf-8")

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
                  too_short: 2
            """
        ).format(temp=self.tempdir)
        self.mktemp(".source.yml", config, "utf-8")

    def test_all(self):
        """Test all."""

        self.assert_spellcheck(".source.yml", self.bad_words1)
