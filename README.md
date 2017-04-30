TTSlab
======

TTSlab is a toolkit intended for text-to-speech research and prototype
development.

Dependencies:
-------------

Python modules:
 - dateutil
 - numpy
 - scipy
 - sklearn
 - sequitur (G2P)
 - scikits-audiolab (optional)

Other:
 - OpenFST 1.5.0 or higher with Python bindings (optional)

Build tools:
 - cmake
 - cython
 - gcc

Recommended:
 - ipython
 - matplotlib

Quickstart:
-----------

 1. Clone this source repository to location `$TTSLAB_SOURCE_ROOT`.
 2. Build the HTS engine by running `build.sh` from within `$TTSLAB_SOURCE_ROOT/hts_engine`.
 3. Build the RELP synthesizer for unit selection voices if necessary by running `compile_relp.sh` from `$TTSLAB_SOURCE_ROOT/ttslab/synthesizers`
 4. Add `$TTSLAB_SOURCE_ROOT` to the `$PYTHONPATH`
 5. Download a voice (e.g. _Lwazi2 Afrikaans_ from the [NTTS Project](https://github.com/NWU-MuST/ntts))
 6. Load and use the downloaded voice (e.g. "voice.pickle") using IPython as follows:

```python
import ttslab
v = ttslab.fromfile("voice.pickle")
u = v.synthesize(u"Toets, 1, 2, 3.")
#save the waveform:
u["waveform"].write("sample.wav")
#play the waveform (if scikits.audiolab has been installed):
u["waveform"].play()
```
