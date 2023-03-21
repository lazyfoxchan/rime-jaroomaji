# License: Apache License 2.0
# Author: lazy fox chan
# Mozcの辞書ファイルをrime-jaroomaji用に変換する
import urllib.request
import convcommon


MIN_SCORE = 50000
MOZC_DICT_URL_LIST = ["https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary00.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary01.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary02.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary03.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary04.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary05.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary06.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary07.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary08.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/dictionary09.txt",
                      "https://github.com/google/mozc/raw/master/src/data/dictionary_oss/suffix.txt"]
MOZC_DICT_FILE_NAME_LIST = ["dictionary00.txt", "dictionary01.txt", "dictionary02.txt", "dictionary03.txt",
                            "dictionary04.txt", "dictionary05.txt", "dictionary06.txt", "dictionary07.txt",
                            "dictionary08.txt", "dictionary09.txt", "suffix.txt"]
OUTPUT_FILE_NAME = "jaroomaji.mozc.dict.yaml"
OUTPUT_FILE_HEADER = \
"""# Rime dictionary
# encoding: utf-8
#
# This file was converted from the mozc project repository
# See original license:
# https://github.com/google/mozc/tree/master/src/data/dictionary_oss
#

---
name: jaroomaji.mozc
version: "1.0"
sort: by_weight
use_preset_vocabulary: false
...

"""


def main():
    mozc_list = []  # 単語、読み、スコア

    # Mozcの辞書データをダウンロード
    for i, input_file_url in enumerate(MOZC_DICT_URL_LIST):
        print("ダウンロード開始：" + input_file_url)
        urllib.request.urlretrieve(input_file_url, MOZC_DICT_FILE_NAME_LIST[i])
        print("ダウンロード終了：" + MOZC_DICT_FILE_NAME_LIST[i])

    # ダウンロードしたテキストファイルから必要な情報を取り出す
    for input_file_name in MOZC_DICT_FILE_NAME_LIST:
        input_file = open(input_file_name, "r", encoding="utf-8")
        for line in input_file:
            line = line.replace("\n", "")
            word = line.split("\t")
            mozc_list.append([word[4], word[0], word[3]])  # 単語、読み、スコア
        input_file.close()
    print("step 1/7 ファイル読み込み ： 完了")

    # Mozcのスコアをrime-jaroomaji用のスコアに変換する
    mozc_list = calc_score(mozc_list)
    print("step 2/7 スコア反転 ： 完了")

    # 小文字ラテン文字が含まれている単語は大文字ラテン文字版も追加する
    mozc_list = convcommon.add_full_with_latin(mozc_list)
    print("step 3/7 大文字ラテン文字の追加 ： 完了")

    # 変換精度向上のため、読みが「っ」で終わる単語を処理する
    mozc_list = convcommon.replace_xtu(mozc_list)
    print("step 4/7 「っ」で終わる単語の置換 ： 完了")

    # ひらがなの読みをrime-jaroomaji用のローマ字に変換する。
    mozc_list = convcommon.hiralist2roomalist(mozc_list)
    print("step 5/7 読みをローマ字に変換 ： 完了")

    # 重複している項目を削除する
    mozc_list = convcommon.remove_duplicates(mozc_list)
    print("step 6/7 重複単語の削除 ： 完了")

    # ファイル書き出し
    output_file = open(OUTPUT_FILE_NAME, "w", encoding="utf-8")
    output_file.write(OUTPUT_FILE_HEADER)
    for word in mozc_list:
        output_file.write(word[0] + "\t" + word[1] + "\t" + word[2] + "\n")  # 単語、読み、スコア
    output_file.close()
    print("step 7/7 出力ファイル書き込み ： 完了")


def calc_score(arg_list):
    """Mozcのスコアをrime-jaroomaji用のスコアに変換する

    リスト内のスコアを昇順から降順に反転させる
    スコアの最小値はMIN_SCOREを参照する

    Args:
        arg_list (list): [[単語, 読み, スコア], [単語, 読み, スコア]...]
    Returns:
        list: [[単語, 読み, スコア], [単語, 読み, スコア]...]
    """
    return_list = []
    max_score = 0

    # スコアの最大値を取得する
    for line in arg_list:
        if int(line[2]) > max_score:
            max_score = int(line[2])

    # スコアを反転させる
    for line in arg_list:
        rime_score = max_score - int(line[2])
        return_list.append([line[0], line[1], str(rime_score + MIN_SCORE)])  # 単語、読み、スコア(最小は0) + スコア最小値

    return return_list


if __name__ == "__main__":
    main()
