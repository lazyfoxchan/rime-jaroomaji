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
# https://github.com/google/mozc/blob/master/LICENSE
# https://github.com/google/mozc/tree/master/src/data/dictionary_oss
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
## -------------------------------------------------------------------------------
## IPAdic is licensed as follows:
## 
## Copyright 2000, 2001, 2002, 2003 Nara Institute of Science
## and Technology.  All Rights Reserved.
## 
## Use, reproduction, and distribution of this software is permitted.
## Any copy of this software, whether in its original form or modified,
## must include both the above copyright notice and the following
## paragraphs.
## 
## Nara Institute of Science and Technology (NAIST),
## the copyright holders, disclaims all warranties with regard to this
## software, including all implied warranties of merchantability and
## fitness, in no event shall NAIST be liable for
## any special, indirect or consequential damages or any damages
## whatsoever resulting from loss of use, data or profits, whether in an
## action of contract, negligence or other tortuous action, arising out
## of or in connection with the use or performance of this software.
## 
## A large portion of the dictionary entries
## originate from ICOT Free Software.  The following conditions for ICOT
## Free Software applies to the current dictionary as well.
## 
## Each User may also freely distribute the Program, whether in its
## original form or modified, to any third party or parties, PROVIDED
## that the provisions of Section 3 ("NO WARRANTY") will ALWAYS appear
## on, or be attached to, the Program, which is distributed substantially
## in the same form as set out herein and that such intended
## distribution, if actually made, will neither violate or otherwise
## contravene any of the laws and regulations of the countries having
## jurisdiction over the User or the intended distribution itself.
## 
## NO WARRANTY
## 
## The program was produced on an experimental basis in the course of the
## research and development conducted during the project and is provided
## to users as so produced on an experimental basis.  Accordingly, the
## program is provided without any warranty whatsoever, whether express,
## implied, statutory or otherwise.  The term "warranty" used herein
## includes, but is not limited to, any warranty of the quality,
## performance, merchantability and fitness for a particular purpose of
## the program and the nonexistence of any infringement or violation of
## any right of any third party.
## 
## Each user of the program will agree and understand, and be deemed to
## have agreed and understood, that there is no warranty whatsoever for
## the program and, accordingly, the entire risk arising from or
## otherwise connected with the program is assumed by the user.
## 
## Therefore, neither ICOT, the copyright holder, or any other
## organization that participated in or was otherwise related to the
## development of the program and their respective officials, directors,
## officers and other employees shall be held liable for any and all
## damages, including, without limitation, general, special, incidental
## and consequential damages, arising out of or otherwise in connection
## with the use or inability to use the program or any product, material
## or result produced or otherwise obtained by using the program,
## regardless of whether they have been advised of, or otherwise had
## knowledge of, the possibility of such damages at any time during the
## project or thereafter.  Each user will be deemed to have agreed to the
## foregoing by his or her commencement of use of the program.  The term
## "use" as used herein includes, but is not limited to, the use,
## modification, copying and distribution of the program and the
## production of secondary products from the program.
## 
## In the case where the program, whether in its original form or
## modified, was distributed or delivered to or received by a user from
## any person, organization or entity other than ICOT, unless it makes or
## grants independently of ICOT any specific warranty to the user in
## writing, such person, organization or entity, will also be exempted
## from and not be held liable to the user for any such damages as noted
## above as far as the program is concerned.
## 
## -------------------------------------------------------------------------------
## Okinawa dictionary is licensed as follows
## 
## Public Domain Dataです。使用・変更・配布に関しては一切の制限をつけません。
## 商品などに組み込むことも自由に行なってください。すでにいくつかの辞書には沖縄辞書が採用されています。
## 勝手ながら、沖縄辞書に寄贈された辞書も in the Public Domain' 扱いとさせていただきます。
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
