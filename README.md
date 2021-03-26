## Audio file quantisation demonstration!

This python 3 script takes the supplied 16bit 48Ksps audio mono WAV file and creates a further 15 versions, each
with a reduced number of sampled bits from 15 through to 1.

The purpose is to demonstrate how fewer bits affects the audio quality of digitally reproduced sound.

It is fascinating just to see how few bits can be used to sample audio before it is affected by digital noise caused 
by quantisation errors. 
That is, for a sample, a significant movement in value from the original source.

My own anecdotal findings (aka my ears!) note that the audio is easy listening down to 7 or 6 bits when the 
quantisation errors manifest in a form of white noise that sounds uncannily similar to tape hiss!

I've included a sample audio file (16bit signed, mono WAV) for testing.
This includes an excerpt from a piano tune ('Newborn' by Apple Loops) that is 
significantly affected by this 'tape hiss' before the other audio samples get affected as the number
of sampling bits drop.

In the included audio test file 'test_track_mono_signed_16bit.wav' has these sounds, in order:
* Opening few seconds of Nick Lansley's Innovation Lab podcast/video theme tune.
* Nick counting from one to ten.
A short sample of 'Newborn', a piano track from Apple Loops.
* A ticking spound.
* A frequency sweep from 1Hz to 20KHz in 5 seconds at 80% max volume.

Running the script will generate 15 audio files, all of 16bit WAV audio 
but with bit depth reduced in each case. The sample rate of 48Ksps is not changed.
The script id fully commented with each step.

The script uses scipy, matplotlib and numpy.
The matplotlib uses a function plot_waveform() that is not called (yet!) so can be removed
along with that function if needed.

Enjoy!

Best regards
Nick Lansley