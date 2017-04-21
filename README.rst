MakePass
========

A password generator inspired by https://xkcd.com/936/

Usage
-----

Simply install the package with pip, then run the ``make_pass`` command::

    $ make_pass
    Estimated password entropy: 57.5569 bits
    CorrectHorseBatteryStaple7

The password is written to stdout, from which it can be captured via your pipelined capture mechanism of choice, and additional diagnostic data will be printed to stderr.

Process & Constraints
---------------------

Makepass generates a memorable, readable password by combining **N** unique, random common english words, which are sourced from the `Google Common English Words <https://github.com/first20hours/google-10000-english>`_ repository. By default, the list of 20,000 english words is used. The set of words is constrained to be between **m** and **n** characters long, inclusive, to promote memorability and prevent common words. A random numeral is appended, to satisfy the common requirement that passwords contain a letter and a number. The final password must will be at least **L** characters long; up to **S** passwords are generated internally until a password of sufficient length is found.

All of the above can be configured; run ``make_pass -h`` for a list of the flags that modify its behavior, as well as options for more or less verbose printing
of entropy information

Defaults.
~~~~~~~~~

All of the following parameters can be changed:

- **N** = 4
- **m** = 4
- **n** = 8
- **L** = 24
- **S** = 10,000
- Random numeral **is** appended
- Word set: 20k. Can be repaced with the 10k set.

These default parameters produce passwords with an entropy of approximately 57.561 bits.
