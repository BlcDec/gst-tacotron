import os
from time import sleep
import argparse
from time import sleep
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from getdata import getdatas
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
num = True
input_url = ''
re_url = ''
out_url = ''

@app.route('/')
def login():
    return render_template('home.html')

@app.route('/upfile',methods=['GET', 'POST'])
def login_action():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        global num
        global input_url
        global re_url
        if num:
            input_url = os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest2.0\\static\\in', filename)
            num = False
            file.save(input_url)
        else:
            re_url = os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest2.0\\static\\re', filename)
            num = True
            file.save(re_url)

        return render_template('home.html')
    return render_template('home.html')

@app.route('/synthesizer',methods=['GET', 'POST'])
def Synthesizer_action():
    try:
        out_url, out_name = synthesizer.synthesize(input_url, re_url)
        # out_url = os.path.join('..\\static\\out\\', '5-712930-714330-jp.wav')
        # out_name = '5-712930-714330-jp.wav'
        out_name = os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest2.0\\static\\out', out_name)
        datas = getdatas(input_url, re_url, out_name)

        res = {
            'state': True,
            'out': out_url,
            'data': datas
        }
        return json.dumps(res)
    except IndexError:
        res = {
            'state': False
        }
        return json.dumps(res)
@app.route('/datas',methods=['GET', 'POST'])
def updata():
    datas = getdatas(input_url, re_url, input_url)
    print(datas)
    return json.dumps(datas)



synthesizer = Synthesizer()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True, help='')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--hparams', default='',
                        help='Hyperparameter overrides as a comma-separated list of name=value pairs')
    args = parser.parse_args()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    hparams.parse(args.hparams)
    print(hparams_debug_string())
    synthesizer.load(args.checkpoint)
    print('Serving on port %d' % args.port)
    app.run()
else:
    synthesizer.load(os.environ['CHECKPOINT'])
