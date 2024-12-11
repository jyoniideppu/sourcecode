import os

# コーパスを読み込む関数（頻度も含めて保存）
def load_corpus(file_path):
    words = []
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # 最初の行をスキップ
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) > 6:  # 7列目に頻度があることを確認
                try:
                    frequency = float(parts[6])  # 頻度を取得
                    words.append((parts[1], parts[2], frequency))  # カタカナ、漢字、頻度のタプルを保存
                except ValueError:
                    print(f"行をスキップしました: {line}")  # エラーが発生した行をスキップ
    return words

# 「ロ」と「ド」を含む単語のリストを作成
def extract_words_with_ro_bo(corpus):
    words_with_ro = []
    words_with_bo = []

    for word, kanji, frequency in corpus:
        if 'ボ' in word:
            words_with_ro.append((word, kanji, frequency))
        if 'ド' in word:
            words_with_bo.append((word, kanji, frequency))
    
    return words_with_ro, words_with_bo

# ミニマルペアを探す関数（頻度を保存）
def find_one_char_diff_minimal_pairs(words_with_ro, words_with_bo):
    minimal_pairs = []
    for word_ro, kanji_ro, freq_ro in words_with_ro:
        for word_bo, kanji_bo, freq_bo in words_with_bo:
            # 長さが同じで、最初の文字が同じ、かつ二文字目以降で一文字だけ違う場合
            if (len(word_ro) == len(word_bo) and 
                word_ro[0] == word_bo[0]):
                # 二文字目以降で違う文字の数をカウント
                diff_chars = sum(c1 != c2 for c1, c2 in zip(word_ro[1:], word_bo[1:]))
                
                # 違う文字が1文字だけの場合
                if diff_chars == 1 and freq_ro > 0 and freq_bo > 0:
                    minimal_pairs.append((word_ro, word_bo, kanji_ro, kanji_bo, freq_ro, freq_bo))
    
    return minimal_pairs

# ミニマルペアを頻度順にソート
def sort_minimal_pairs_by_frequency(minimal_pairs):
    return sorted(minimal_pairs, key=lambda pair: (pair[4] + pair[5]), reverse=True)

# 結果を表示する関数
def display_minimal_pairs(minimal_pairs, category):
    print(f"\nカテゴリー: {category} の頻度順ミニマルペア:")
    for pair in minimal_pairs:
        print(f"{pair[0]} - {pair[1]} ({pair[2]} - {pair[3]}) 頻度: {pair[4]} + {pair[5]}")

# カテゴリーをファイル名から抽出する関数
def extract_category_from_path(file_path):
    if "書き言葉" in file_path:
        return "書き言葉"
    elif "話し言葉" in file_path:
        return "話し言葉"
    elif "日常会話" in file_path:
        return "日常会話"
    else:
        return "不明なカテゴリー"

# メイン処理
def main():
    corpus_files = [
        r'C:/yourpass/BCCWJ_frequencylist_suw_ver1_0/書き言葉_BCCWJ_frequencylist_suw_ver1_0.tsv',
        r'C:/yourpass/CSJ_frequencylist_suw_ver201803/話し言葉CSJ_frequencylist_suw_ver201803.tsv',
        r'C:/yourpass/CEJC短単位語彙表_語彙素のみ_語形別_ver202209/CEJC語彙表_語彙素のみ_語形別_ver202209/日常会話_2_cejc_frequencylist_suw_token.tsv'
    ]
    
    for file_path in corpus_files:
        if os.path.exists(file_path):
            category = extract_category_from_path(file_path)  # ファイル名からカテゴリーを抽出
            print(f"\nファイルを処理中: {file_path} （カテゴリー: {category}）")
            corpus = load_corpus(file_path)
            words_with_ro, words_with_bo = extract_words_with_ro_bo(corpus)
            minimal_pairs = find_one_char_diff_minimal_pairs(words_with_ro, words_with_bo)
            sorted_minimal_pairs = sort_minimal_pairs_by_frequency(minimal_pairs)
            display_minimal_pairs(sorted_minimal_pairs, category)
        else:
            print(f"ファイルが存在しません: {file_path}")

if __name__ == "__main__":
    main()
