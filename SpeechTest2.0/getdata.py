from scipy.io import wavfile
import numpy as np
def getdatas(in_path,re_path,out_path):
    rate, audio = wavfile.read(in_path)
    time = np.arange(0, len(audio))
    timelist = time.tolist()
    audiolist = audio.tolist()
    datas = []
    for i in range(0, len(timelist)):
        datas.append({'time': timelist[i]/16000, 'value': (audiolist[i]/10000)+5, 'sound': 'in'})
    rate2, audio2 = wavfile.read(re_path)
    time2 = np.arange(0, len(audio2))
    timelist2 = time2.tolist()
    audiolist2 = audio2.tolist()
    for i in range(0, len(timelist2)):
        datas.append({'time': timelist2[i]/16000, 'value': (audiolist2[i]/10000), 'sound': 're'})
    rate3, audio3 = wavfile.read(out_path)
    time3 = np.arange(0, len(audio3))
    timelist3 = time3.tolist()
    audiolist3 = audio3.tolist()
    for i in range(0, len(timelist3)):
        if (timelist3[i]/ 16000 > 7):
            break
        datas.append({'time': timelist3[i]/16000, 'value': (audiolist3[i]/10000)-5, 'sound': 'out'})
    return datas


