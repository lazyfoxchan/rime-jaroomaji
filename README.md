# rime-jaroomaji
Rime IME用MS-IME風ローマ字入力スキーマ。  
Japanese rōmaji input schema for Rime IME.   
中州韻輸入法引擎日文羅馬輸入方案。  
![デモ](./img4md/demo.gif)

## インストール方法
1. [Rime IME](https://rime.im/download/)が必要です。お使いの環境に合わせてRime IMEをインストールして下さい。  
2. 以下ファイルをRime IMEのユーザーディレクトリにコピーして下さい。  
    * jaroomaji.schema.yaml
    * jaroomaji.dict.yaml
    * jaroomaji.user.dict.yaml
    * jaroomaji.kana_kigou.dict.yaml
    * jaroomaji.mozc.dict.yaml
    * jaroomaji.jmdict.dict.yaml
    * jaroomaji.mozcemoji.dict.yaml
    * jaroomaji.kanjidic2.dict.yaml  
  注: plumが利用出来る場合、このレポジトリを指定してインストールすることも出来ます。  
  `lazyfoxchan/rime-jaroomaji`
3. 各環境に合わせたやり方で、rime-jaroomajiを有効化し、再デプロイ(重新部署)して下さい。  
参考：[Rime IME公式ドキュメント「データファイルの構成と動作」(華文)](https://github.com/rime/home/wiki/RimeWithSchemata#rime-%E4%B8%AD%E7%9A%84%E6%95%B8%E6%93%9A%E6%96%87%E4%BB%B6%E5%88%86%E4%BD%88%E5%8F%8A%E4%BD%9C%E7%94%A8)
  

## 入力方法
* 記号入力などは全てUS配列として動作します
* Shiftキー `=` 日本語モード/英字モードの切り替え
* Shift+ローマ字入力 `=` 強制カタカナ入力
* 入力中にEnter `=` 入力したひらがなを確定
* 入力中にShift+Enter `=` 入力した英字を確定
* 入力中に十字キーの上下 `=` 変換候補選択
* 入力中にSpace `=` 変換候補確定
* Lキー `=` 伸ばし棒(Xキーで小さいひらがなを入力出来ます)

## Tips

### ユーザー辞書に単語を追加したい
`opencc/CreateUserDict.py`でユーザー辞書ファイルを生成することが出来ます。  
生成されるユーザー辞書ファイルは`jaroomaji.user.dict.yaml`です。  
実行方法の詳細は[dict_tools/README.md](dict_tools/README.md)をご確認下さい。

### 最新の単語を辞書に追加したい
[![AutoUpdateJMDict](https://github.com/lazyfoxchan/rime-jaroomaji/actions/workflows/AutoUpdateJMDict.yml/badge.svg)](https://github.com/lazyfoxchan/rime-jaroomaji/actions/workflows/AutoUpdateJMDict.yml)  
このレポジトリの`jaroomaji.jmdict.dict.yaml`は毎週自動更新されます。  
必要に応じて自環境のファイルを更新してください。  

### Weasel(小狼毫)ユーザー向けオススメ設定

#### default.custom.yaml (ユーザーディレクトリに配置)
```yaml
patch:
  menu/page_size: 10  # 変換候補を1ページに10個まで表示する
```

#### weasel.custom.yaml (ユーザーディレクトリに配置)
```yaml
patch:
  style/inline_preedit: true  # 入力途中の文字をアプリケーション側に送信する
  style/font_face: "Meiryo UI"  # 変換候補の表示フォントをメイリオUIにする(中華フォント対策)
```

## ライセンス
以下辞書ファイルは変換元のライセンスに従います。詳細は各辞書ファイルヘッダーのコメント行をご確認下さい。
* jaroomaji.mozc
* jaroomaji.jmdict
* jaroomaji.mozcemoji
* jaroomaji.kanjidic2

その他のファイル: [Apache License 2.0](https://github.com/lazyfoxchan/rime-jaroomaji/blob/master/LICENSE)  
製作者: lazy fox chan
