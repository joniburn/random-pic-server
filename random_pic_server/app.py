from glob import glob
import os.path
from random import choice

from flask import Flask, make_response
app = Flask(__name__)


PICS_DIR = os.environ['PICS_DIR']

RESPONSE_HEADER = {
    'Content-Type': 'image/jpeg',
}


@app.route('/')
def hello():
    # 返却する画像ファイルを選択
    file_list = glob(os.path.join(PICS_DIR, '**', '*.jpg'), recursive=True)
    pic_fname = choice(file_list)

    # 画像ファイルを読み込み
    with open(pic_fname, mode='rb') as f:
        pic_data = f.read()

    print(f'Hello World!, PICS_DIR=[{PICS_DIR}], pic_fname={pic_fname}')

    # レスポンスを返却
    return make_response(pic_data, 200, RESPONSE_HEADER)
