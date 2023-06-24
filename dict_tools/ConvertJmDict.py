# License: Apache License 2.0
# Author: lazy fox chan
# JMdictをrime-jaroomaji用に変換する
import urllib.request
import xml.etree.ElementTree as ET
import jaconv
import convcommon


SCORE_HIGH = "40002"
SCORE_MEDIUM = "40001"
SCORE_LOW = "40000"
JMDICT_URL = "http://ftp.edrdg.org/pub/Nihongo/JMdict_e"
JMDICT_FILE_NAME = "JMdict_e.xml"
OUTPUT_FILE_NAME = "jaroomaji.jmdict.dict.yaml"
OUTPUT_FILE_HEADER = \
"""# Rime dictionary
# encoding: utf-8
#
# This file was converted from JMdict
# See original license(CC BY-SA 4.0):
# https://www.edrdg.org/edrdg/licence.html
# https://creativecommons.org/licenses/by-sa/4.0/
# https://creativecommons.org/licenses/by-sa/4.0/legalcode
#

---
name: jaroomaji.jmdict
version: "VERSION_REPLACE"
sort: by_weight
use_preset_vocabulary: false
...

"""


def main():
    jmdict_list = []  # 単語、読み、スコア
    dict_version = ""

    # JMdictのxmlをダウンロード
    print("ダウンロード開始：" + JMDICT_URL)
    urllib.request.urlretrieve(JMDICT_URL, JMDICT_FILE_NAME)
    print("ダウンロード終了：" + JMDICT_FILE_NAME)

    # xmlからデータを取り出す
    tree = ET.parse(JMDICT_FILE_NAME)
    root = tree.getroot()
    # entryタグが一つの単語のまとまり(複数表記が含まれる場合あり)
    for entry in root.iter("entry"):
        # k_eleタグがなかったら(ひらがなかカタカナのみの単語だったら)
        if entry.find("k_ele") is None:
            # r_eleタグ内の全てのrebタグの内容を取得(全ての単語を取得)
            for r_ele in entry.iter("r_ele"):
                # ただしr_eleタグ内のre_infタグに「search-only kanji form」が格納されていた場合は、そのr_eleタグは無視する(誤用に関するデータも入っているので)
                if r_ele.find("re_inf") is not None and r_ele.find("re_inf").text == "search-only kana form":
                    continue
                # また、r_eleタグ内のre_infタグにre_nokanjiタグが存在した場合は、そのr_eleタグは無視する(誤用に関するデータも入っているので)
                if r_ele.find("re_nokanji") is not None:
                    continue
                tango = r_ele.find("reb").text
                yomi = r_ele.find("reb").text
                priority = ""
                # 取得したrebタグ(単語の内容)に対応するre_pri(単語の一般性情報)があればそれも取得
                if r_ele.find("re_pri") is not None:
                    priority = r_ele.find("re_pri").text
                # 上記があるかに関わらず、読みのカタカナをひらがなに変換してリストに保存
                jmdict_list.append([tango, jaconv.kata2hira(yomi), calc_score(priority)])
        # k_eleタグがあったら(ひらがなかカタカナ以外が含まれている単語だったら)
        elif entry.find("k_ele") is not None:
            # 全てのr_eleタグに対して処理を行う
            for r_ele in entry.iter("r_ele"):
                # ただしr_eleタグ内のre_infタグに「search-only kanji form」が格納されていた場合は、そのr_eleタグは無視する(誤用に関するデータも入っているので)
                if r_ele.find("re_inf") is not None and r_ele.find("re_inf").text == "search-only kana form":
                    continue
                # また、r_eleタグ内のre_infタグにre_nokanjiタグが存在した場合は、そのr_eleタグは無視する(誤用に関するデータも入っているので)
                if r_ele.find("re_nokanji") is not None:
                    continue
                # r_eleタグ内にre_restrタグがなかった場合
                if r_ele.find("re_restr") is None:
                    # k_eleタグ内のkebタグの内容(単語)とr_eleタグ内のrebタグの内容(読み)を取得
                    for k_ele in entry.iter("k_ele"):
                        # ただしk_eleタグ内のke_infタグに「search-only kanji form」があった場合は、そのk_eleタグは無視する(誤用に関するデータも入っているので)
                        if k_ele.find("ke_inf") is not None and k_ele.find("ke_inf").text == "search-only kanji form":
                            continue
                        tango = k_ele.find("keb").text
                        yomi = r_ele.find("reb").text
                        priority = ""
                        # k_eleタグ内ke_priタグの内容(単語の一般性情報)があったら取得する
                        if k_ele.find("ke_pri") is not None:
                            priority = k_ele.find("ke_pri").text
                        # 上記があるかに関わらず、読みのカタカナをひらがなに変換してリストに保存
                        jmdict_list.append([tango, jaconv.kata2hira(yomi), calc_score(priority)])
                # r_eleタグ内にre_restrタグがあった場合
                elif r_ele.find("re_restr") is not None:
                    # r_eleタグ内の全てのre_restrタグに対して
                    for re_restr in r_ele.iter("re_restr"):
                        # 対応するrebタグの内容(読み)を取得し、全てのk_eleタグの内容を見ていく
                        for k_ele in entry.iter("k_ele"):
                            # ただしk_eleタグ内のke_infタグに「search-only kanji form」があった場合は、そのk_eleタグは無視する(誤用に関するデータも入っているので)
                            if k_ele.find("ke_inf") is not None and k_ele.find("ke_inf").text == "search-only kanji form":
                                continue
                            tango = re_restr.text
                            yomi = r_ele.find("reb").text
                            priority= ""
                            # re_restrタグの内容(単語)と一致するk_eleタグだった場合
                            if tango == k_ele.find("keb").text:
                                # k_eleタグ内ke_priタグの内容(単語の一般性情報)があったら取得する
                                if k_ele.find("ke_pri") is not None:
                                    priority = k_ele.find("ke_pri").text
                                # 上記があるかに関わらず、読みのカタカナをひらがなに変換してリストに保存
                                jmdict_list.append([tango, jaconv.kata2hira(yomi), calc_score(priority)])
    # xmlからバージョン情報を取り出す
    input_file = open(JMDICT_FILE_NAME, "r", encoding="utf-8")
    for line in input_file:
        if "JMdict created:" in line:
            dict_version = line.replace("<!-- JMdict created: ", "").replace(" -->\n", "")
            break
    input_file.close()
    print("step 1/6 ファイル読み込み ： 完了")

    # 大文字ラテン文字が含まれている単語は小文字ラテン文字版も追加する
    jmdict_list = convcommon.add_half_with_latin(jmdict_list)
    print("step 2/6 小文字ラテン文字の追加 ： 完了")

    # 変換精度向上のため、読みが「っ」で終わる単語を処理する
    jmdict_list = convcommon.replace_xtu(jmdict_list)
    print("step 3/6 「っ」で終わる単語の置換 ： 完了")

    # ひらがなの読みをローマ字に変換する
    jmdict_list = convcommon.hiralist2roomalist(jmdict_list)
    print("step 4/6 読みをローマ字に変換 ： 完了")

    # 重複している項目を削除する
    jmdict_list = convcommon.remove_duplicates(jmdict_list)
    print("step 5/6 重複単語の削除 ： 完了")

    # ファイル書き出し
    output_file = open(OUTPUT_FILE_NAME, "w", encoding="utf-8")
    output_file.write(OUTPUT_FILE_HEADER.replace("VERSION_REPLACE", dict_version))
    for word in jmdict_list:
        output_file.write(word[0] + "\t" + word[1] + "\t" + word[2] + "\n")
    output_file.close()
    print("step 6/6 出力ファイル書き込み ： 完了")


def calc_score(pri):
    """単語の一般性情報をrime-jaroomaji用のスコアに変換する

    Args:
        pri (str): JMdictのxmlに記載されている単語の一般性情報
    Returns:
        str: スコア
    """
    if pri == "news1" or pri == "ichi1" or pri == "spec1" or pri == "gai1":
        return SCORE_HIGH
    if pri == "news2" or pri == "ichi2" or pri == "spec2" or pri == "gai2":
        return SCORE_MEDIUM
    else:
        return SCORE_LOW


if __name__ == "__main__":
    main()
