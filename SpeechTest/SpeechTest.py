import os
import argparse
from time import sleep
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer

from flask import Flask, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_in = request.files['file_in']
        file_re = request.files['file_re']
        if file_in and allowed_file(file_in.filename):
            filename_in = secure_filename(file_in.filename)
            file_in.save(os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest\\static\\in', filename_in))
            filename_re = secure_filename(file_re.filename)
            file_re.save(os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest\\static\\re', filename_re))
            in_path = os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest\\static\\in', filename_in)
            re_path = os.path.join('C:\\Users\\blcdec\\project\\gst-tacotron\\SpeechTest\\static\\re', filename_re)
            print(filename_in)
            print(filename_re)
            data = synthesizer.synthesize(in_path, re_path)
            return render_template('test.html', file_url_out=data, file_url_in='static/in/'+ filename_in, file_url_re='static/re/'+ filename_re)
    return render_template('test.html')



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
