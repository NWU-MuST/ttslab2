Installation quickstart
=======================

This guide briefly describes how to install the toolkit in an _Ubuntu Linux_ environment (tested on Ubuntu 16.04). For other environments refer to `./README.md` for links to software dependencies.

## 1. Install dependencies

#### Required dependencies:
From Ubuntu repositories:
```bash
sudo apt-get install build-essential cmake cython python-setuptools swig wget python-numpy #build environment
sudo apt-get install python-cffi python-dateutil python-scipy python-sklearn python-pyicu #python modules
```
Download [Sequitur G2P][1], make, build and install as follows:
```bash
wget https://www-i6.informatik.rwth-aachen.de/web/Software/g2p-r1668-r3.tar.gz
tar -xzvf g2p-r1668-r3.tar.gz
cd g2p
sudo python setup.py install
```

#### Optional dependencies:

Download, build and install [scikits-audiolab][2] (including dependencies):
```bash
sudo apt-get install libasound2-dev libsndfile1-dev
wget https://pypi.python.org/packages/b0/d8/d9babf3e4fa3ac8094e1783415bf60015a696779f4da4c70ae6141aa5e3a/scikits.audiolab-0.11.0.tar.gz#md5=f93f17211c7763d8631e0d10f37471b0
tar -xzvf scikits.audiolab-0.11.0.tar.gz
cd scikits.audiolab-0.11.0
sudo python setup.py install
```

Download, build and install [OpenFST 1.5.0][3]:
```bash
wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.0.tar.gz
tar -xzvf openfst-1.5.0.tar.gz
cd openfst-1.5.0
./configure --enable-bin --enable-compact-fsts --enable-compress --enable-const-fsts --enable-far --enable-linear-fsts --enable-lookahead-fsts --enable-mpdt --enable-ngram-fsts --enable-pdt --enable-python
make
sudo make install
```

## 2. Install TTSLab toolkit

Clone or download this repository to a location (`$TTSLAB_SOURCE`) e.g.:

```bash
git clone https://github.com/demitasse/ttslab2.git
```

Build the synthesis back-end components as follows:

```bash
cd $TTSLAB_SOURCE/hts_engine
bash build.sh
cd $TTSLAB_SOURCE/ttslab/synthesizers
bash compile_relp.sh
```

Add `$TTSLAB_SOURCE` to the `$PYTHONPATH` (preferably in `~/.bashrc` or similar bash startup script):

```bash
export $PYTHONPATH=$TTSLAB_SOURCE:$PYTHONPATH
```

## 3. Build or download a voice and test

A complete set of scripts for building an HMM-based Afrikaans voice is [available here][4]. A voice file (e.g. `afr_lwazi2.voice.pickle`) can be loaded and used from Python as follows:

```python
import ttslab
v = ttslab.fromfile("afr_lwazi2.voice.pickle")
u = v.synthesize(u"Toets: 1 2 3.")
#save the waveform:
u["waveform"].write("test.wav")
#play the waveform (if scikits.audiolab has been installed):
u["waveform"].play()
```

------------------------------------------------------------
[1]: https://www-i6.informatik.rwth-aachen.de/web/Software/g2p-r1668-r3.tar.gz
[2]: https://pypi.python.org/pypi/scikits.audiolab/0.11.0
[3]: http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.5.0.tar.gz
[4]: https://github.com/demitasse/ttslab2_afr_lwazi2_build