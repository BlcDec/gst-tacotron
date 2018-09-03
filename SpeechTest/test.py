import scipy.io.wavfile as wav

rate,audio=wav.read('out.wav')
print(audio)
print(rate)

