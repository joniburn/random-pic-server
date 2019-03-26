# オンメモリの状態を保持するモジュール
# flask runで起動するサーバーではリクエストの並列処理を行わないため、
# 排他処理やスレッド/プロセス間同期処理は不要

from datetime import datetime


class _State:
    """メモリ上に保持する状態"""

    # 最後に画像が選択された時刻
    pic_selected_latest_time: datetime

    # 現在選択されている画像のバイナリデータ
    current_picture_data: bytes


state = _State()
state.pic_selected_latest_time = datetime.now()
state.current_picture_data = None
