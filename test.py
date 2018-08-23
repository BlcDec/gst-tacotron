from matplotlib import pyplot as plt
import numpy as np


def shownpy(int_dir):
    a=np.load(int_dir)

    print(a.shape)

    plt.imshow(a.T*255)
    plt.show()

if __name__=='__main__':
    shownpy("C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\training\\Imuspeech-tar_cd_mel-00007.npy")
    shownpy("C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\training\\Imuspeech-in_cg_mel_spec-00007.npy")