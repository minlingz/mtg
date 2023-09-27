"""Markov Text Generator.

Minling Zhou, 2023

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

from collections import Counter
from typing import Optional, List
import random


def generate_tokens(corpus: List[str], n: int, sentence: list):
    """Generate tokens tuple for n gram"""
    tokens = {}

    # create tokens for 1-gram
    if n == 1:
        tokens = {i: tuple(corpus[i]) for i in range(len(corpus))}
        return tokens
    # create tokens for n-gram (n>1)
    for i in range(len(corpus) - n + 1):
        if tuple(corpus[i : i + n - 1]) == tuple(sentence[-n + 1 :]):
            tokens[i] = tuple(corpus[i : i + n])
    return tokens


def generate_next_word(tokens: dict, n: int, corpus: list, randomize=False):
    """Generate next word"""
    if randomize:
        return random.choice(list(tokens.values()))[-1]
    else:
        w = Counter(tokens.values())
        return w.most_common(1)[0][0][-1]


def finish_sentence(sentence, n, corpus, randomize=False):
    """Generate tokens to unfinished sentence using ngram"""
    working_sentence = sentence.copy()
    future_sentence = sentence.copy()

    while future_sentence[-1] not in {".", "?", "!"} and len(future_sentence) < 10:
        current_tokens = generate_tokens(corpus, n, working_sentence)
        i = n
        while current_tokens == {} and i > 1:
            # run 1 level back in gram
            i = i - 1
            if len(working_sentence) >= i:
                working_sentence.pop()
            current_tokens = generate_tokens(corpus, i, working_sentence)

        if current_tokens:
            next_word = generate_next_word(current_tokens, i, corpus, randomize)
            working_sentence.append(next_word)
            future_sentence.append(next_word)

    return future_sentence


if __name__ == "__main__":
    finish_sentence()
