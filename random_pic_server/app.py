from datetime import datetime, timedelta
from glob import glob
import os.path
from random import choice

from filelock import FileLock
from flask import Flask, make_response

from random_pic_server.state import state as s


app = Flask(__name__)
logger = app.logger

# 対象画像の格納ディレクトリ
PICS_DIR = os.environ['PICS_DIR']

# ロックファイル
LOCK_FILE = os.environ.get('LOCK_FILE', '.lock')

# レンスポンスヘッダー定義
RESPONSE_HEADER = {
    'Content-Type': 'image/jpeg',
}

# 画像選択間隔
PIC_SELECT_INTERVAL_SEC = os.environ.get('PIC_SELECT_INTERVAL_SEC', '30')
PIC_SELECT_DELTA = timedelta(seconds=int(PIC_SELECT_INTERVAL_SEC))


@app.route('/')
def hello():
    with FileLock(LOCK_FILE, timeout=1):
        logger.info('Start')

        # 前回の画像選択から一定時間経過していない場合は最後の画像を返却
        now = datetime.now()
        selection_required = (
            now - s.pic_selected_latest_time > PIC_SELECT_DELTA)
        if s.current_picture_data and not selection_required:
            logger.info('End: not updated')
            return make_response(s.current_picture_data, 200, RESPONSE_HEADER)

        # 返却する画像ファイルを選択
        file_list = glob(os.path.join(PICS_DIR, '**', '*.jpg'), recursive=True)
        pic_fname = choice(file_list)

        # 画像ファイルを読み込み
        with open(pic_fname, mode='rb') as f:
            s.current_picture_data = f.read()

        # 時刻を更新
        s.pic_selected_latest_time = now

        # レスポンスを返却
        logger.info('End')
        return make_response(s.current_picture_data, 200, RESPONSE_HEADER)
