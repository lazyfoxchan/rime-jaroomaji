# License: Apache License 2.0
# Author: lazy fox chan
# KANJIDIC2をrime-jaroomaji用に変換する
import urllib.request
import xml.etree.ElementTree as ET
import jaconv
import convcommon


KUNYOMI_SCORE = "8888"
ONYOMI_SCORE = "8000"
KANJIDIC2_URL = "http://ftp.edrdg.org/pub/Nihongo/kanjidic2.xml"
KANJIDIC2_FILE_NAME = "kanjidic2.xml"
OUTPUT_FILE_NAME = "jaroomaji.kanjidic2.dict.yaml"
OUTPUT_FILE_HEADER = \
"""# Rime dictionary
# encoding: utf-8
#
# This file was converted from KANJIDIC2
# See original license(CC BY-SA 4.0):
# https://www.edrdg.org/edrdg/licence.html
# https://creativecommons.org/licenses/by-sa/4.0/
# https://creativecommons.org/licenses/by-sa/4.0/legalcode
#

---
name: jaroomaji.kanjidic2
version: "1.0"
sort: by_weight
use_preset_vocabulary: false
...

"""


def main():
    kanji_list = []  # 漢字、読み、スコア

    # KANJIDIC2のxmlをダウンロード
    print("ダウンロード開始：" + KANJIDIC2_URL)
    urllib.request.urlretrieve(KANJIDIC2_URL, KANJIDIC2_FILE_NAME)
    print("ダウンロード終了：" + KANJIDIC2_FILE_NAME)

    # xmlからデータを取り出す
    # 音読みの振り仮名はカタカナからひらがなに変換する
    tree = ET.parse(KANJIDIC2_FILE_NAME)
    root = tree.getroot()
    for character in root.iter("character"):
        for reading in character.iter("reading"):
            if reading.attrib["r_type"] == "ja_on":
                kanji_list.append([character.find("literal").text, jaconv.kata2hira(reading.text), calc_score(False)])
            if reading.attrib["r_type"] == "ja_kun":
                kanji_list.append([character.find("literal").text, reading.text, calc_score(True)])
    # 訓読みの特殊なデータをIMEで使える形にする
    for kanji in kanji_list:
        # 訓読みの送り仮名を漢字側に入れる
        if "." in kanji[1]:
            kanji[0] = kanji[0] + kanji[1].split(".")[1]
            kanji[1] = kanji[1].replace(".", "")
        # 訓読みの「-」を消す
        if "-" in kanji[1]:
            kanji[1] = kanji[1].replace("-", "")
    print("step 1/4 ファイル読み込み ： 完了")

    # ひらがなの読みをrime-jaroomaji用のローマ字に変換する。
    kanji_list = convcommon.hiralist2roomalist(kanji_list)
    print("step 2/4 読みをローマ字に変換 ： 完了")

    # 重複している項目を削除する
    kanji_list = convcommon.remove_duplicates(kanji_list)
    print("step 3/4 重複単語の削除 ： 完了")

    # ファイル書き出し
    output_file = open(OUTPUT_FILE_NAME, "w", encoding="utf-8")
    output_file.write(OUTPUT_FILE_HEADER)
    for word in kanji_list:
        output_file.write(word[0] + "\t" + word[1] + "\t" + word[2] + "\n")  # 単語、読み、スコア
    output_file.close()
    print("step 4/4 出力ファイル書き込み ： 完了")


def calc_score(is_kunyomi):
    """訓読み、音読みのスコアを返す

    Args:
        is_kunyomi (list): 訓読みはTrue、音読みはFalse
    Returns:
        str: スコア
    """
    if is_kunyomi:
        return KUNYOMI_SCORE
    else:
        return ONYOMI_SCORE


if __name__ == "__main__":
    main()
