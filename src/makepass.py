import random
import itertools
from math import log2
import sys
from os.path import join as path_join

from autocommand import autocommand


def base_word_set(use_10k):
    path = path_join(
        sys.prefix, 'share', 'makepass',
        '10k.txt' if use_10k else '20k.txt'
    )
    with open(path) as file:
        for word in file:
            yield word.strip().capitalize()


def sized_word_set(word_set, min_word, max_word):
    for word in word_set:
        if min_word <= len(word) <= max_word:
            yield word


def gen_alpha_password(rand_engine, word_set, word_count):
    return ''.join(rand_engine.sample(word_set, word_count))


def gen_alnum_password(rand_engine, word_set, word_count):
    return (
        gen_alpha_password(rand_engine, word_set, word_count) +
        str(rand_engine.randrange(10))
    )


def base_passwords(rand_engine, word_set, word_count, append_numeral):
    if append_numeral:
        gen = gen_alnum_password
    else:
        gen = gen_alpha_password

    while True:
        yield gen(rand_engine, word_set, word_count)


def filtered_passwords(base_passwords, min_length):
    for password in base_passwords:
        if len(password) >= min_length:
            yield password


def count_iterator(it):
    try:
        return len(it)
    except TypeError:
        return sum(1 for _ in it)


def wordset_entropy(word_set_size, word_count):
    return sum(map(log2, range(word_set_size, word_set_size - word_count, -1)))


def numeral_entropy(append_numeral):
    return log2(10) if append_numeral else 0


def sampled_entropy(sample_size, success_size):
    return log2(success_size) - log2(sample_size)


def estimate_entropy(
    word_set_size,
    word_count,
    append_numeral,
    sample_size,
    success_size
):
    return (
        wordset_entropy(word_set_size, word_count) +
        numeral_entropy(append_numeral) +
        sampled_entropy(sample_size, success_size)
    )


@autocommand(__name__)
def main(
    word_count: 'Number of words in the password' =4,
    min_length: 'Minimum character length in the password' =24,
    no_append_numeral: "Don't a random 0-9 numeral to the password" =False,
    min_word: 'Minimum length of each individual word in the password' =4,
    max_word: 'Maximum length of each individual word in the password' =8,
    no_entropy_estimate: "Don't print an entropy estimate to stderr" =False,
    use_10k: 'Use the 10k most common words, instead of 20k' =False,
    sample_size: "Number of internal passwords to produce. Used for entropy "
        "estimates, and as the number of attempts before giving up" =10000,
    verbose: 'Print verbose entropy calculation details' =False,
):
    '''
    %(prog)s is a password generator
    '''
    if min_word > max_word:
        return "min_word must be less than or equal to max_word"

    rand_engine = random.SystemRandom()

    word_set = list(sized_word_set(
        base_word_set(use_10k),
        min_word, max_word
    ))

    passwords = base_passwords(
        rand_engine=rand_engine,
        word_set=word_set,
        word_count=word_count,
        append_numeral=not no_append_numeral
    )

    passwords = itertools.islice(passwords, sample_size)
    passwords = filtered_passwords(passwords, min_length)

    try:
        password = next(passwords)
    except StopIteration:
        return "Couldn't generate password matching constraints"

    if not no_entropy_estimate:
        word_set_size = len(word_set)
        success_size = count_iterator(passwords) + 1

        entropy = estimate_entropy(
            word_set_size=word_set_size,
            word_count=word_count,
            append_numeral=not no_append_numeral,
            sample_size=sample_size,
            success_size=success_size
        )

        print(
            "Estimated password entropy: {:.2f} bits".format(entropy),
            file=sys.stderr
        )

        if verbose:
            print(
                "Generated a password of {word_count} non-repeating words, "
                "from a set of {word_set_size} common english words of length "
                "{min_word} to {max_word}. {bits:.4f} bits of entropy".format(
                    word_count=word_count,
                    word_set_size=word_set_size,
                    min_word=min_word,
                    max_word=max_word,
                    bits=wordset_entropy(word_set_size, word_count),
                ),
                file=sys.stderr,
            )

            if not no_append_numeral:
                print(
                    "A random numeral in the range 0-9 was appended, for an "
                    "additional {bits:.4f} bits of entropy".format(
                        bits=numeral_entropy(True),
                    ),
                    file=sys.stderr,
                )

            if success_size != sample_size:
                print(
                    "{sample_size} sample passwords were generated, but only "
                    "{success_size} passwords had a length of at least "
                    "{min_length}. The entropy estimate was adjusted "
                    "accordingly by {bits:.4f} bits.".format(
                        sample_size=sample_size,
                        success_size=success_size,
                        min_length=min_length,
                        bits=sampled_entropy(sample_size, success_size),
                    ),
                    file=sys.stderr
                )

    print(password)
