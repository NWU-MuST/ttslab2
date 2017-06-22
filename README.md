TTSLab toolkit
==============

TTSLab is a toolkit intended for text-to-speech (TTS) research and prototype development. __For a installation instructions refer to `./INSTALL.md`.__

Software dependencies:
----------------------

Most non-optional dependencies can be installed directly from the standard repositories on Ubuntu Linux. See `./INSTALL.md` on how to install dependencies on Ubuntu Linux.

Python modules/bindings:
 - [dateutil][1]
 - [numpy][2]
 - [scipy][3]
 - [cffi][4]
 - [sklearn][5] (version 0.17)
 - [Sequitur G2P][6] 
 - [pyicu][7]
 - [scikits-audiolab][8] (optional)
 - [OpenFST 1.5.0][9] or higher with Python bindings (optional)

Build tools:
 - [cmake][10]
 - [cython][11]
 - [gcc][12]

Recommended:
 - [ipython][13]
 - [matplotlib][14]


Bundled software by third parties:
----------------------------------

 - A modified version of the [HTS engine][15] version 1.09 (see `hts_engine/README`, `hts_engine/COPYING` and individual source files for more information)
 - POS tagging module (see copyright and authorship information in `ttslab/postagger.py` and `ttslab/postagger_perceptron.py`)


------------------------------------------------------------
[1]: https://pypi.python.org/pypi/python-dateutil
[2]: https://pypi.python.org/pypi/numpy/1.13.0
[3]: https://pypi.python.org/pypi/scipy/0.19.0
[4]: https://pypi.python.org/pypi/cffi/1.10.0
[5]: https://pypi.python.org/pypi/scikit-learn/0.17
[6]: https://www-i6.informatik.rwth-aachen.de/web/Software/g2p-r1668-r3.tar.gz
[7]: https://pypi.python.org/pypi/PyICU/1.9.7
[8]: https://pypi.python.org/pypi/scikits.audiolab/0.11.0
[9]: http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.0.tar.gz
[10]: https://cmake.org/
[11]: http://cython.org/
[12]: https://gcc.gnu.org/
[13]: https://pypi.python.org/pypi/ipython/6.1.0
[14]: https://pypi.python.org/pypi/matplotlib/2.0.2
[15]: http://hts-engine.sourceforge.net/
