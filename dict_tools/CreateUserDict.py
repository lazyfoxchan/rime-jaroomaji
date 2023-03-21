# License: Apache License 2.0
# Author: lazy fox chan
# rime-jaroomaji用のユーザー辞書ファイルを作成する
import convcommon


USER_DICT_FILE_NAME = "user_dict.tsv"
OUTPUT_FILE_NAME = "jaroomaji.user.dict.yaml"
OUTPUT_FILE_HEADER = \
"""# Rime dictionary
# encoding: utf-8
#
# ユーザー辞書ファイル
# CreateUserDict.pyを使用すると簡単にこのファイルを作成できます
#

---
name: jaroomaji.user
version: "1.0"
sort: by_weight
use_preset_vocabulary: false
...

"""


def main():
    userdict_list = []  # 単語、読み、スコア

    # ユーザー辞書のtsvファイルを読み込む
    input_file = open(USER_DICT_FILE_NAME, "r", encoding="utf-8")
    for line in input_file:
        line = line.replace("\n", "")
        word = line.split("\t")
        # tsvのコメント行は無視
        if word[0][0] == "#":
            continue
        userdict_list.append([word[0], word[1], word[2]])  # 単語、読み、スコア
    input_file.close()
    print("step 1/3 tsvファイル読み込み ： 完了")

    # ひらがなの読みをrime-jaroomaji用のローマ字に変換する。
    userdict_list = convcommon.hiralist2roomalist(userdict_list)
    print("step 2/3 読みをローマ字に変換 ： 完了")

    # ファイル書き出し
    output_file = open(OUTPUT_FILE_NAME, "w", encoding="utf-8")
    output_file.write(OUTPUT_FILE_HEADER)
    for word in userdict_list:
        output_file.write(word[0] + "\t" + word[1] + "\t" + word[2] + "\n")  # 単語、読み、スコア
    output_file.close()
    print("step 3/3 出力ファイル書き込み ： 完了")


if __name__ == "__main__":
    main()
