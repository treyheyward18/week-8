from collections import defaultdict

import numpy as np


class MarkovText(object):
    """Generate text from a corpus using a first-order Markov chain."""

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None  # built by get_term_dict()

    def get_term_dict(self):
        """
        Build a transition dictionary from the corpus.

        Each key is a unique token, and each value is a list of every
        token that follows that key in the corpus. Duplicates are kept on
        purpose: a word that follows the key more often appears more
        often in the list, so random sampling from the list naturally
        reproduces the corpus's transition probabilities.
        """
        tokens = self.corpus.split()
        term_dict = defaultdict(list)

        for current, following in zip(tokens[:-1], tokens[1:]):
            term_dict[current].append(following)

        self.term_dict = dict(term_dict)

        return self.term_dict

    def generate(self, seed_term=None, term_count=15):
        """
        Generate `term_count` tokens using the Markov property.

        If `seed_term` is given, it must be a token in the corpus,
        otherwise a ValueError is raised. If no seed is given, a random
        token is used. If the generator reaches a terminal word (one
        that never has a successor, such as the last token of the
        corpus), it restarts from a random token instead of failing.
        """
        if self.term_dict is None:
            self.get_term_dict()

        tokens = list(self.term_dict.keys())

        if seed_term is not None:
            if seed_term not in self.corpus.split():
                raise ValueError(
                    f"Seed term '{seed_term}' is not in the corpus."
                )
            current = seed_term
        else:
            current = str(np.random.choice(tokens))

        words = [current]

        while len(words) < term_count:
            successors = self.term_dict.get(current)

            if successors:
                current = str(np.random.choice(successors))
            else:
                # terminal word: no observed successors, so restart
                current = str(np.random.choice(tokens))

            words.append(current)

        return " ".join(words)
