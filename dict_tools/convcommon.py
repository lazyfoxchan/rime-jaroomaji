# License: Apache License 2.0
# Author: lazy fox chan
import convrules


def add_half_with_latin(arg_list):
    """リスト内の全角ラテン文字が入っている単語を半角ラテン文字も追加する

    ・リスト内の全角ラテン文字が入っている単語を半角ラテン文字にする
    ・リスト内の全角ラテン文字が入っている単語のスコアを-1する

    Args:
        arg_list (list): [[単語, 読み, スコア], [単語, 読み, スコア]...]
    Returns:
        list: [[単語, 読み, スコア], [単語, 読み, スコア]...]
    """
    return_list = []

    for word in arg_list:
        is_exist_uppercase = False
        lower_case_latin = word[0]
        # 単語に全角ラテン文字が含まれていたら、半角ラテン文字に変換した単語を作成する
        for ConvertRule in convrules.LATIN_CONVERT_RULES:
            if ConvertRule[0] in lower_case_latin:
                lower_case_latin = lower_case_latin.replace(ConvertRule[0], ConvertRule[1])
                is_exist_uppercase = True
        # 単語に全角ラテン文字が含まれていたら、半角と全角両方のラテン文字をリストに入れる
        if is_exist_uppercase:
            return_list.append([lower_case_latin, word[1], word[2]])
            return_list.append([word[0], word[1], str(int(word[2]) - 1)])  # 全角のスコアは-1する
        # 単語に全角ラテン文字が含まれていなかったら、そのままにする
        else:
            return_list.append(word)

    return return_list


def add_full_with_latin(arg_list):
    """リスト内の半角ラテン文字が入っている単語を全角ラテン文字も追加する

    ・リスト内の半角ラテン文字が入っている単語を全角ラテン文字にする
    ・リスト内の全角ラテン文字が入っている単語はスコアを-1する

    Args:
        arg_list (list): [[単語, 読み, スコア], [単語, 読み, スコア]...]
    Returns:
        list: [[単語, 読み, スコア], [単語, 読み, スコア]...]
    """
    return_list = []

    for word in arg_list:
        is_exist_lowercase = False
        upper_case_latin = word[0]
        # 単語に半角ラテン文字が含まれていたら、全角ラテン文字に変換した単語を作成する
        for ConvertRule in convrules.LATIN_CONVERT_RULES:
            if ConvertRule[1] in upper_case_latin:
                upper_case_latin = upper_case_latin.replace(ConvertRule[1], ConvertRule[0])
                is_exist_lowercase = True
        # 単語に半角ラテン文字が含まれていたら、半角と全角両方のラテン文字をリストに入れる
        if is_exist_lowercase:
            return_list.append(word)
            return_list.append([upper_case_latin, word[1], str(int(word[2]) - 1)])  # 全角のスコアは-1する
        # 単語に全角ラテン文字が含まれていなかったら、そのままにする
        else:
            return_list.append(word)

    return return_list


def replace_xtu(arg_list):
    """リスト内の読みが「っ」で終わる単語を削除して、「た」「て」「と」が末尾に付いた単語を新たに追加する

    Args:
        arg_list (list): [[単語, ひらがなの読み, スコア], [単語, ひらがなの読み, スコア]...]
    Returns:
        list: [[単語, ひらがなの読み, スコア], [単語, ひらがなの読み, スコア]...]
    """
    return_list = []

    for word in arg_list:
        if word[1][-1] == "っ":
            return_list.append([word[0] + "た", word[1] + "た", word[2]])
            return_list.append([word[0] + "て", word[1] + "て", word[2]])
            return_list.append([word[0] + "と", word[1] + "と", word[2]])
        else:
            return_list.append(word)

    return return_list


def hiralist2roomalist(arg_list):
    """リスト内のひらがなの読みをrime-jaroomaji用のローマ字に変換する。

    適応する変換規則：
      ・読みにひらがな以外が含まれていた場合 → その単語は無視する
      ・読みが伸ばし棒1個のみ → その単語は無視する
      ・「りゅ」のような拗音が含まれている かつ カタカナのみの単語 → パターン1～4全て
      ・カタカナのみの単語 → パターン1とパターン3
      ・「りゅ」のような拗音が含まれている → パターン1とパターン2
      ・それ以外 → パターン1

    Args:
        arg_list (list): [[単語, ひらがなの読み, スコア], [単語, ひらがなの読み, スコア]...]
    Returns:
        list: [[単語, ローマ字の読み, スコア], [単語, ローマ字の読み, スコア]...]
    """
    def hira2rooma(yomi, convert_rules):
        for convert_rule in convert_rules:
            yomi = yomi.replace(convert_rule[0], convert_rule[1])
        return yomi[:-1]  # 最後の空白は不要なので消す

    return_list = []

    for input_list_line in arg_list:
        is_exist_youon = False
        is_only_katakana = False
        # 読みにひらがな以外が読みに含まれている場合、無視する
        tmp_str = input_list_line[1]
        for hiragana in convrules.HIRAGANA_LIST:
            tmp_str = tmp_str.replace(hiragana, "")
        if tmp_str:
            continue
        # 読みが伸ばし棒1個のみである場合、無視する
        if input_list_line[1] == "ー":
            continue
        # 拗音が含まれているか判定
        for youon in convrules.YOUON_LIST:
            if youon in input_list_line[1]:
                is_exist_youon = True
                break
        # カタカナのみの単語か判定
        tmp_str = input_list_line[0]
        for katakana in convrules.KATAKANA_LIST:
            tmp_str = tmp_str.replace(katakana, "")
        if not tmp_str:
            is_only_katakana = True
        # 読みをローマ字に変換して新しいリストに保存
        if is_exist_youon and is_only_katakana:
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_1), input_list_line[2]])
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_2), input_list_line[2]])
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_3), input_list_line[2]])
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_4), input_list_line[2]])
        if not is_exist_youon and is_only_katakana:
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_1), input_list_line[2]])
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_3), input_list_line[2]])
        if is_exist_youon and not is_only_katakana:
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_1), input_list_line[2]])
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_2), input_list_line[2]])
        if not is_exist_youon and not is_only_katakana:
            return_list.append([input_list_line[0], hira2rooma(input_list_line[1], convrules.CONVERT_PATTERN_1), input_list_line[2]])

    return return_list


def remove_duplicates(arg_list):
    """リスト内の重複している単語を削除する

    読みと単語が両方一致しているものを重複項目とする
    重複項目は最初に出てきた箇所に最大スコアを入れたものを1つだけ保持する
    2つ回め以降の重複項目は削除する

    Args:
        arg_list (list): [[単語, 読み, スコア], [単語, 読み, スコア]...]
    Returns:
        list: [[単語, 読み, スコア], [単語, 読み, スコア]...]
    """
    return_list = []
    tmp_dict = {}  # 単語と読みを一つにしてkeyにする。valueは最大スコア

    # スコア最大値を格納する辞書変数作成
    for input_list_line in arg_list:
        key = input_list_line[0] + "|" + input_list_line[1]
        # まだ登録されていないキーならとりあえず登録する
        if key not in tmp_dict.keys():
            tmp_dict[key] = input_list_line[2]
            continue
        # 登録されている既存のキーよりスコアが大きかったら更新する
        if tmp_dict[key] < input_list_line[2]:
            tmp_dict[key] = input_list_line[2]

    # 引数のリストと同じ順序のリスト作成
    for input_list_line in arg_list:
        key = input_list_line[0] + "|" + input_list_line[1]
        # 重複2回目以降はリストに追加しない
        if key not in tmp_dict.keys():  # 下で削除されてる
            continue
        # リストに単語、読み、辞書変数に入っているスコア最大値を入れる
        return_list.append([input_list_line[0], input_list_line[1], tmp_dict[key]])
        # 一度リストに入れたら以降は重複なので辞書から消す
        del tmp_dict[key]

    return return_list
