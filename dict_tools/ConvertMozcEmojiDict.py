# License: Apache License 2.0
# Author: lazy fox chan
# Mozcの絵文字辞書ファイルをrime-jaroomaji用に変換する
import urllib.request
import convcommon


EMOJI_SCORE = "30000"
MOZC_EMOJI_DICT_URL = "https://github.com/google/mozc/raw/master/src/data/emoji/emoji_data.tsv"
MOZC_EMOJI_DICT_FILE_NAME = "emoji_data.tsv"
OUTPUT_FILE_NAME = "jaroomaji.mozcemoji.dict.yaml"
OUTPUT_FILE_HEADER = \
"""# Rime dictionary
# encoding: utf-8
#
# This file was converted from the mozc project repository
# See original license:
# https://github.com/google/mozc/blob/master/LICENSE
## Copyright 2010-2018, Google Inc.
## All rights reserved.
## 
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
## 
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above
##     copyright notice, this list of conditions and the following disclaimer
##     in the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Google Inc. nor the names of its
##     contributors may be used to endorse or promote products derived from
##     this software without specific prior written permission.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

---
name: jaroomaji.mozcemoji
version: "1.0"
sort: by_weight
use_preset_vocabulary: false
...

"""


def main():
    mozc_list = []  # 単語、読み、スコア

    # Mozcの辞書データをダウンロード
    print("ダウンロード開始：" + MOZC_EMOJI_DICT_URL)
    urllib.request.urlretrieve(MOZC_EMOJI_DICT_URL, MOZC_EMOJI_DICT_FILE_NAME)
    print("ダウンロード終了：" + MOZC_EMOJI_DICT_FILE_NAME)

    # ダウンロードしたtsvファイルから必要な情報を取り出す
    input_file = open(MOZC_EMOJI_DICT_FILE_NAME, "r", encoding="utf-8")
    for line in input_file:
        line = line.replace("\n", "")
        word = line.split("\t")
        # tsvのコメント行は無視
        if word[0][0] == "#":
            continue
        # 絵文字に対する読みを全て取得する
        for yomi in word[2].split(" "):
            mozc_list.append([word[1], yomi, EMOJI_SCORE])  # 単語、読み、スコア
    input_file.close()
    print("step 1/5 ファイル読み込み ： 完了")

    # 候補が多すぎる絵文字を削除する
    mozc_list = remove_verbose_emoji(mozc_list)
    print("step 2/5 候補が多すぎる絵文字の削除 ： 完了")

    # ひらがなの読みをrime-jaroomaji用のローマ字に変換する。
    mozc_list = convcommon.hiralist2roomalist(mozc_list)
    print("step 3/5 読みをローマ字に変換 ： 完了")

    # 重複している項目を削除する
    mozc_list = convcommon.remove_duplicates(mozc_list)
    print("step 4/5 重複単語の削除 ： 完了")

    # ファイル書き出し
    output_file = open(OUTPUT_FILE_NAME, "w", encoding="utf-8")
    output_file.write(OUTPUT_FILE_HEADER)
    for word in mozc_list:
        output_file.write(word[0] + "\t" + word[1] + "\t" + word[2] + "\n")  # 単語、読み、スコア
    output_file.close()
    print("step 5/5 出力ファイル書き込み ： 完了")


def remove_verbose_emoji(arg_list):
    """リスト内の絵文字の読みが「はた」「こっき」のものを削除する

    Args:
        arg_list (list): [[単語, ひらがなの読み, スコア], [単語, ひらがなの読み, スコア]...]
    Returns:
        list: [[単語, ひらがなの読み, スコア], [単語, ひらがなの読み, スコア]...]
    """
    return_list = []

    # 読みが「はた」「こっき」以外のものはリストに追加する
    for line in arg_list:
        if line[1] != "はた" and line[1] != "こっき":
            return_list.append(line)

    return return_list


if __name__ == "__main__":
    main()
