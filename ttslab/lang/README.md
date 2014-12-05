README
======

This directory is meant to contain information to implement the text
processing stages of TTS for different languages. For example *phone
sets* and *valid orthographies* etc.

Each language may have an associated `.py` file containing important
fields and implementations. There is also a `default.py` file which
may serve as template or be used directly by language-specific files
by importanting reusable fields or implementations.

In general Voice classes will implement only the *front-end* or
*text-processing* as well as hooks for the *back-end* or
*synthesizer*. Processes required to further transform the utterance
to conform to synthesizer-specific requirements should be done as a
subprocess of the synthesizer *utterance processor* implementation
(e.g. splitting phones into diphone specifications or model labels for
HTS HMM-based synthesis).

The voice implementation in `sotho.py` is the basis for other
Sotho-Tswana languages.

The voice implementation in `zulu.py` is the basis for other Nguni
languages.
