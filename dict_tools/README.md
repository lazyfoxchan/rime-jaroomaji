# rime-jaroomaji/dict_tools
rime-jaroomaji用の辞書ファイルの生成・変換ツールです

## 動作条件
* python3系
  * PyPy3.9で動作確認済み
* jaconv
  * `pip install jaconv`

## 各ツールの詳細

### CreateUserDict.py
ユーザー辞書を生成します。  
同じディレクトリにあるuser_dict.tsvを読み込みます。tsvの記載例はこのレポジトリにあるuser_dict.tsvをご確認下さい。  
出力ファイル名は`jaroomaji.user.dict.yaml`です。

### ConvertJmDict.py
最新のJMDictの辞書ファイルをrime-jaroomaji用に変換します。  
出力ファイル名は`jaroomaji.jmdict.dict.yaml`です。

### ConvertKanjiDic2.py
最新のKANJIDIC2の辞書ファイルをrime-jaroomaji用に変換します。  
出力ファイル名は`jaroomaji.kanjidic2.dict.yaml`です。

### ConvertMozcDict.py
最新のMozcの辞書ファイルをrime-jaroomaji用に変換します。  
出力ファイル名は`jaroomaji.mozc.dict.yaml`です。

### ConvertMozcEmojiDict.py
最新のMozcの絵文字辞書ファイルをrime-jaroomaji用に変換します。  
出力ファイル名は`jaroomaji.mozcemoji.dict.yaml`です。
