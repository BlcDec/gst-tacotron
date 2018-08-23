
import csv
import os


def test():
    in_dir = 'C:\\Users\\blcdec\\project\\speech_style_convert\\tacotron_imu\\ImuSpeech-2.0'
    with open(os.path.join(in_dir, 'metadata.csv'), encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            tar_path = os.path.join(in_dir, 'wavs', '%s.wav' % parts[0])

            in_path = os.path.join(in_dir, 'wavs', '%s.wav' % parts[1])
            print(in_path)



def write_csv(in_cd_dir, in_jd_dir,in_cg_dir):
    ''' 获取指定目录下的所有指定后缀的文件名 '''

    f_list_cd = os.listdir(in_cd_dir)
    f_list_jd =os.listdir(in_jd_dir)
    f_list_cg=os.listdir(in_cg_dir)
    # print f_list
    list_cd=[]
    list_jd=[]
    list_cg=[]
    for i in f_list_cd:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.wav':
            list_cd.append(os.path.splitext(i)[0])
    for i in f_list_jd:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.wav':
            list_jd.append(os.path.splitext(i)[0])
    for i in f_list_cg:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.wav':
            list_cg.append(os.path.splitext(i)[0])


    print(list_cd)
    print(list_jd)
    print(list_cg)
    metadata = open('C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\ImuSpeech-2.0\\metadata.csv', 'w', newline='',encoding='utf-8')
    w = csv.writer(metadata)
    for i in range(0,len(list_cd)):
        w.writerow([list_cd[i], list_jd[i],list_cg[i]])
    metadata.close()



if __name__ == '__main__':
    in_cd_dir = 'C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\ImuSpeech-2.0\\wly'#chinese dubbing
    in_jd_dir = 'C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\ImuSpeech-2.0\\gky'#japanese dubbing
    in_cg_dir = 'C:\\Users\\blcdec\\project\\gst-tacotron\\tacotron_imu\\ImuSpeech-2.0\\tts'#tts
    write_csv(in_cd_dir, in_jd_dir,in_cg_dir)
    #test()
