import itertools
import random
import re
import sys
import textwrap

from contextlib import closing
from math import log2
from pkg_resources import resource_stream

from autocommand import autocommand


def base_word_set(use_10k):
    '''
    Get the initial set of words to create a password from
    '''
    # These files should have been installed by setup.py
    file = resource_stream(
        'makepass',
        'data/10k.txt' if use_10k else 'data/20k.txt'
    )
    with closing(file):
        for word in file:
            yield word.decode('utf8').strip()


def constrain_word_length(words, min_len, max_len):
    '''
    Filter words from an iterable of words that are outside the inclusive
    length boundaries
    '''
    for word in words:
        if min_len <= len(word) <= max_len:
            yield word


def gen_alpha_password(rand_engine, word_set, word_count):
    '''
    Create a single password out words from the words set. Return an iterable
    of strings
    '''
    yield from rand_engine.sample(word_set, word_count)


def gen_alnum_password(rand_engine, word_set, word_count):
    '''
    Create a password out of words from the word set, and append a random
    numeral. Return an iterable of strings
    '''
    yield from gen_alpha_password(rand_engine, word_set, word_count)
    yield str(rand_engine.randrange(10))


def base_passwords(rand_engine, word_set, word_count, append_numeral):
    '''
    Generate an infinite list of password using either gen_alnum_password or
    gen_alpha_password.
    '''
    if append_numeral:
        gen = gen_alnum_password
    else:
        gen = gen_alpha_password

    return itertools.starmap(gen, itertools.repeat((rand_engine, word_set, word_count)))


# We generate and pass around passwords as strings, for efficiency; this helper
# is provided to break a password back into its constituent parts. It returns
# [parts], (numeral or None)
def password_parts(password):
    # Assumes only ascii, which the current data set does fulfill.
    word_parts = re.findall('[A-Z][a-z]*', password)
    number_part = int(password[-1]) if password[-1].isdigit() else None
    return word_parts, number_part


def count_iterator(it):
    '''
    Count the length of an iterable. This consumes the iterator.
    '''
    try:
        return len(it)
    except TypeError:
        return sum(1 for _ in it)


def wordset_entropy(word_set_size, word_count):
    '''
    Get the entropy for selecting word_count words from a set of word_set_size,
    without replacement
    '''
    return sum(map(log2, range(word_set_size, word_set_size - word_count, -1)))


def numeral_entropy(append_numeral):
    '''
    Get the entropy for appending a numeral (or not)
    '''
    return log2(10) if append_numeral else 0


def sampled_entropy(sample_size, success_size):
    '''
    Estimate the change in entropy given a sample of passwords from a set.

    Rationalle: Assume that we can produce passwords with an entropy of 57.
    However, not all of these passwords are at least 24 characters long. Rather
    than try to calculate the exact change in entropy, we estimate it by
    generating {sample_size} passwords, and seeing that {success_size} meet our
    constraints. We then assume that the ratio of these numbers is proportional
    to the overall ratio of possible_passwords to allowed_passwords. This
    allows us to do the following caluclation:

    original_entropy = log2(permutation_space)
    new_entropy = log2(permutation_space * ratio)
       = log2(permutation_space) + log2(success_size / sample_size)
       = log2(permutation_space) + log2(success_size) - log2(sample_size)
       = original_entropy + log2(success_size) - log2(sample_size)
    '''
    return log2(success_size) - log2(sample_size)


def estimate_entropy(
    word_set_size,
    word_count,
    append_numeral,
    sample_size,
    success_size
):
    '''
    Perform a complete entropy estimate using wordset_entropy, numeral_entropy,
    sampled_entropy
    '''
    return (
        wordset_entropy(word_set_size, word_count) +
        numeral_entropy(append_numeral) +
        sampled_entropy(sample_size, success_size)
    )


def errfmt(fmt, *args, **kwargs):
    '''
    Given a format string, .format() it with the args and kwargs, text wrap it
    to 70 columns, and write it to stdout.
    '''
    return print(textwrap.fill(
        fmt.format(*args, **kwargs)
    ), file=sys.stderr)


def lengthfmt(min_length, max_length):
    '''
    Create a human-readable length string suitible for use in
    "length of {len} characters"
    '''
    if min_length == max_length:
        return "exactly {}".format(min_length)
    elif min_length == 1:
        if max_length == float('inf'):
            return "any number"
        else:
            return "up to {}".format(max_length)
    else:
        if max_length == float('inf'):
            return "at least {}".format(min_length)
        else:
            return "between {} and {}".format(min_length, max_length)


@autocommand(__name__)
def main(
    word_count: 'Number of words in the password' =4,
    min_length: 'Minimum character length in the password' =24,
    max_length: ('Maximum character length in the password', int) =float('inf'),
    no_append_numeral: "Don't append random 0-9 numeral to the password" =False,
    min_word: 'Minimum length of each individual word in the password' =4,
    max_word: 'Maximum length of each individual word in the password' =8,
    entropy_estimate: "Print an entropy estimate to stderr" =False,
    verbose: 'Print verbose entropy calculation details' =False,
    use_10k: 'Use the 10k most common words, instead of 20k' =False,
    sample_size: "Number of internal passwords to produce. Used for entropy "
        "estimates, and as the number of attempts before giving up" =10000,
):
    '''
    %(prog)s is a password generator inspired by https://xkcd.com/936/. It
    generates simple, memorable, secure passwords by combining common english
    words. All parameters are optional; under the default settings it generates
    a password with an entropy of roughly 57.5 bits and an average length of
    27 characters.
    '''
    if min_word > max_word:
        return "min_word must be less than or equal to max_word"

    if min_length > max_length:
        return "min_length must be less than or equal to max_length"

    min_length = max(1, min_length)
    min_word = max(1, min_word)

    rand_engine = random.SystemRandom()

    word_set = tuple(constrain_word_length(
        base_word_set(use_10k),
        min_word, max_word
    ))

    word_set_size = len(word_set)

    if log2(word_set_size) > min_word * log2(26):
        errfmt(
            "Warning: the entropy of brute forcing a short word is less than "
            "that of selecting one from the random set; the password may be "
            "less secure than the entropy estimate indicates, especially if "
            "using a small max_word")

    passwords = base_passwords(
        rand_engine=rand_engine,
        word_set=word_set,
        word_count=word_count,
        append_numeral=not no_append_numeral
    )

    passwords = map(''.join, passwords)
    passwords = itertools.islice(passwords, sample_size)
    passwords = constrain_word_length(passwords, min_length, max_length)

    try:
        password = next(passwords)
    except StopIteration:
        return "Couldn't generate password matching constraints"

    if entropy_estimate or verbose:
        success_size = count_iterator(passwords) + 1

        entropy = estimate_entropy(
            word_set_size=word_set_size,
            word_count=word_count,
            append_numeral=not no_append_numeral,
            sample_size=sample_size,
            success_size=success_size
        )

        errfmt("Estimated password entropy: {:.2f} bits", entropy)

        if verbose:
            errfmt(
                "Generated a password of {word_count} non-repeating words, "
                "from a set of {word_set_size} common english words of "
                "{lenfmt} letters: {bits:.4f} bits of entropy.",

                word_count=word_count,
                word_set_size=word_set_size,
                lenfmt=lengthfmt(min_word, max_word),
                bits=wordset_entropy(word_set_size, word_count),
            )

            if not no_append_numeral:
                errfmt(
                    "A random numeral in the range 0-9 was appended, for an "
                    "additional {bits:.4f} bits of entropy.",
                    bits=numeral_entropy(True),
                )

            if success_size != sample_size:
                errfmt(
                    "{sample_size} sample passwords were generated, but only "
                    "{success_size} passwords had a length of {lenfmt} "
                    "letters. The entropy estimate was adjusted "
                    "accordingly by {bits:.4f} bits.",

                    sample_size=sample_size,
                    success_size=success_size,
                    min_length=min_length,
                    lenfmt=lengthfmt(min_length, max_length),
                    bits=sampled_entropy(sample_size, success_size),
                )

    print(password)
