from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse
import os
import subprocess
import uuid

bp = Blueprint('user', __name__, url_prefix='/user')
Kaldi_path = '/home/nohead/kaldi-trunk/egs/aishell/v1/data'

array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
         "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z",
         "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z"
         ]


def get_short_id():
    id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
    buffer = []
    for i in range(0, 8):
        start = i * 4
        end = i * 4 + 4
        val = int(id[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        sample = args.get('file')
        name = get_short_id()
        utt = name + os.path.splitext(sample.filename)[0]
        temp = name + sample.filename
        SAVE_PATH = os.path.join('/home/nohead/kaldi-trunk/egs/aishell/v1/data/newdata/', temp)
        sample.save(SAVE_PATH)
        os.makedirs(Kaldi_path + '/' + utt)
        f = open(Kaldi_path + '/' + utt + '/wav.scp', 'w+', encoding='utf-8')
        f.write(utt + ' ' + SAVE_PATH)
        f.close()
        f1 = open(Kaldi_path + '/' + utt + '/utt2spk', 'w+', encoding='utf-8')
        f1.write(utt + ' ' + name)
        f1.close()
        os.chdir('/home/nohead/kaldi-trunk/egs/aishell/v1')
        cmd = './run_eval.sh' + ' ' + utt
        subp = subprocess.Popen(cmd, shell=True)  # 执行命令
        subp.wait()  # 等待子进程结束
        p = subp.returncode  # 获取状态码
        if p == 0:
            return redirect("/")
        else:
            return redirect(url_for("user.login"))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        sample = args.get('file')
        name = get_short_id()
        utt = name + os.path.splitext(sample.filename)[0]
        temp = name + sample.filename
        SAVE_PATH = os.path.join('/home/nohead/kaldi-trunk/egs/aishell/v1/data/newdata/', temp)
        sample.save(SAVE_PATH)
        os.makedirs(Kaldi_path + '/' + utt)
        f = open(Kaldi_path + '/' + utt + '/wav.scp', 'w+', encoding='utf-8')
        f.write(utt + ' ' + SAVE_PATH)
        f.close()
        f1 = open(Kaldi_path + '/' + utt + '/utt2spk', 'w+', encoding='utf-8')
        f1.write(utt + ' ' + name)
        f1.close()
        os.chdir('/home/nohead/kaldi-trunk/egs/aishell/v1')
        cmd = './run_enroll.sh' + ' ' + utt
        subp = subprocess.Popen(cmd, shell=True)  # 执行命令
        subp.wait()  # 等待子进程结束
        p = subp.returncode  # 获取状态码
        if p == 0:
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for('user.register'))
