"""test_features.py pins each detector in features.py to one sentence it must flag and one it must
not. Positives come from Table 2 of Clark, Martin & Mahowald 2026 where the default rule catches
the paper's own example; the negative is the same sentence with the construction removed, so a
detector that keys on something else fails one side of its pair.
"""

import unittest

import spacy

from hardread import features


class FeatureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlp = spacy.load("en_core_web_trf")

    def test_orc_no_relativizer(self):
        f = self.flag(features.ORCNoRelativizer,
                      "I am writing to share my thoughts on the cell phone policy you are considering.")
        self.assertEqual(f.span, "policy you are considering")
        self.clear(features.ORCNoRelativizer,
                   "I am writing to share my thoughts on the cell phone policy that you are considering.")

    def test_denominal_verb_seed(self):
        f = self.flag(features.DenominalVerb, "We should calendar the review for Friday.")
        self.assertEqual(f.span, "calendar")
        self.clear(features.DenominalVerb, "We should schedule the review for Friday.")

    def test_denominal_verb_brown(self):
        f = self.flag(features.DenominalVerb, "Let me architect the system before lunch.")
        self.assertIn("a noun 30 times and a verb 0 times in Brown", f.note)
        self.clear(features.DenominalVerb, "Let me design the system before lunch.")

    def test_denominal_verb_rare_verbs(self):
        for text, word in (("We should calendar it for Friday.", "calendar"),
                           ("Please footnote it before you send the draft.", "footnote"),
                           ("Let's whiteboard the plan after lunch.", "whiteboard")):
            with self.subTest(word=word):
                self.assertEqual(self.flag(features.DenominalVerb, text).span, word)

    def test_denominal_verb_common_verbs(self):
        # "mirrors" is the paper's Table 2 sentence: an ordinary verb, so not a hit.
        for text in ("The program exits when the input ends.",
                     "The linter flags unused imports.",
                     "We listed the files in the report.",
                     "This process mirrors real-world challenges much more closely than a packet of "
                     "predefined questions.",
                     "We run the tests every night.", "We work on the parser every night.",
                     "We use the parser every night."):
            with self.subTest(text=text):
                self.clear(features.DenominalVerb, text)

    def test_inanimate_subject(self):
        f = self.flag(features.InanimateSubject,
                      "A song doesn't ask you to turn melancholy into a calendar item.")
        self.assertEqual(f.span, "song doesn't ask")
        self.clear(features.InanimateSubject,
                   "My sister doesn't ask you to turn melancholy into a calendar item.")

    def test_inanimate_subject_code_placeholder(self):
        self.flag(features.InanimateSubject, "The docstring promises they are skipped.")
        self.flag(features.InanimateSubject, f"{features.PLACEHOLDER} expects a list.")
        self.clear(features.InanimateSubject, "The engineer who knows the code expects a list.")

    def test_stacked_nouns(self):
        f = self.flag(features.StackedNouns,
                      "Summer park district classes are a whole thing in Chicago and people actually do them.")
        self.assertEqual(f.span, "Summer park district classes")
        self.clear(features.StackedNouns,
                   "Summer classes are a whole thing in Chicago and people actually do them.")

    def test_stacked_nouns_hyphen_is_one_noun(self):
        self.clear(features.StackedNouns,
                   "The paper also uses two word-pair measures, unattested word pairs and trigram surprisal.")

    def test_dependency_length(self):
        # The paper's example averages 3.44 words per arc: flagged at 3.0, under the 3.5 default.
        s = "Has the building had water, mold, structural, or insurance claims?"
        f = features.DependencyLength(self.sent(s), threshold=3.0)
        self.assertIsNotNone(f, f"DependencyLength missed {s!r} at threshold 3.0")
        self.assertIn("sentence 10 words", f.note)
        self.clear(features.DependencyLength, "The cat sat on the mat.")

    def test_dependency_length_max_words(self):
        long = ("We ran the tests on the parser and the linter every night for a week, and then we "
                "read the logs, wrote the notes, and sent them to the team before the next release.")
        f = self.flag(features.DependencyLength, long)
        self.assertIn(f"words > {features.MAX_WORDS}", f.note)
        self.assertIsNone(features.DependencyLength(self.sent(long), max_words=100))

    def test_dependency_length_threshold(self):
        s = "Has the building had water, mold, structural, or insurance claims?"
        self.assertIsNone(features.DependencyLength(self.sent(s), threshold=10.0))

    def sent(self, text):
        sents = list(self.nlp(text).sents)
        self.assertEqual(len(sents), 1, f"fixture splits into {len(sents)} sentences: {text!r}")
        return sents[0]

    def flag(self, detector, text):
        f = detector(self.sent(text))
        self.assertIsNotNone(f, f"{detector.__name__} missed {text!r}")
        self.assertEqual(f.feature, detector.__name__)
        return f

    def clear(self, detector, text):
        f = detector(self.sent(text))
        self.assertIsNone(f, f"{detector.__name__} flagged {text!r}: {f}")


if __name__ == "__main__":
    unittest.main()
