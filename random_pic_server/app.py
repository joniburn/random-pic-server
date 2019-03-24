from datetime import datetime, timedelta
from glob import glob
import os.path
from random import choice

from flask import Flask, make_response
app = Flask(__name__)


# 対象画像の格納ディレクトリ
PICS_DIR = os.environ['PICS_DIR']

# レンスポンスヘッダー定義
RESPONSE_HEADER = {
    'Content-Type': 'image/jpeg',
}

# 画像選択間隔
PIC_SELECT_INTERVAL_SEC = os.environ.get('PIC_SELECT_INTERVAL_SEC', 30)
PIC_SELECT_DELTA = timedelta(seconds=PIC_SELECT_INTERVAL_SEC)

# メモリ上で保持する情報
# flask runで起動するサーバーではリクエストの並列処理を行わないため、
# 排他処理やスレッド/プロセス間同期処理は不要
pic_selected_latest_time = datetime.now()  # 最後に画像が選択された時刻
current_picture_data = None  # 現在選択されている画像のバイナリデータ


@app.route('/')
def hello():
    global pic_selected_latest_time
    global current_picture_data

    # 前回の画像選択から一定時間経過していない場合は最後の画像を返却
    now = datetime.now()
    selection_required = now - pic_selected_latest_time > PIC_SELECT_DELTA
    if current_picture_data and not selection_required:
        return make_response(current_picture_data, 200, RESPONSE_HEADER)

    # 返却する画像ファイルを選択
    file_list = glob(os.path.join(PICS_DIR, '**', '*.jpg'), recursive=True)
    pic_fname = choice(file_list)

    # 画像ファイルを読み込み
    with open(pic_fname, mode='rb') as f:
        current_picture_data = f.read()

    # 時刻を更新
    pic_selected_latest_time = now

    # レスポンスを返却
    return make_response(current_picture_data, 200, RESPONSE_HEADER)
