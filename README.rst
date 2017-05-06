MakePass
========

A password generator inspired by https://xkcd.com/936/

Usage
-----

Simply install the package with ``pip install makepass``, then run the ``make_pass`` command::

    $ make_pass
    CorrectHorseBatteryStaple7

The password is written to stdout, from which it can be captured via your pipelined capture mechanism of choice.

Process & Constraints
---------------------

Makepass generates a memorable, readable password by combining **N** unique, random common english words, which are sourced from the `Google Common English Words <https://github.com/first20hours/google-10000-english>`_ repository. By default, the list of 20,000 english words is used. The set of words is constrained to words between **m** and **n** characters long, inclusive, to promote memorability and prevent common words. A random numeral is appended, to satisfy the common requirement that passwords contain a letter and a number. The final password will be between **L** and **M** characters long; up to **S** passwords are generated internally until a password of appropriate length is found.

All of the above can be configured; run ``make_pass -h`` for a list of the flags that modify its behavior, as well as options for display of entropy information

Defaults
~~~~~~~~

All of the following parameters can be changed:

- **N** = 4
- **m** = 4
- **n** = 8
- **L** = 24
- **M** = ∞
- **S** = 10,000
- Random numeral **is** appended
- Word set: 20k. Can be repaced with the 10k set.

These default parameters produce passwords with an entropy of approximately 57.561 bits.

Security Disclaimer
-------------------

While I am confident in its basic soundness, ``makepass`` has not undergone any kind of security review or audit, and I am not an expert in the field of password security. Use at your own risk.

``makepass`` is built around use of `random.SystemRandom <https://docs.python.org/3/library/random.html#random.SystemRandom>`_, which in turn is based on `os.urandom <https://docs.python.org/3/library/os.html#os.urandom>`_. ``os.urandom`` is described by the Python documentation as "suitable for cryptographic use." For more information about the use of ``os.urandom`` and ``/dev/urandom`` in secure contexts, see `this article <https://www.2uo.de/myths-about-urandom/>`_.

The most obvious security hole I'm currently aware of in ``makepass`` is that it writes to your terminal, which may be logged or cached to disk. Make sure to pipe it into a secure destintion when creating a password you actually intend to use; I'm personally partial to the ``say`` command on OSX, which speaks the password out loud through your speakers.
