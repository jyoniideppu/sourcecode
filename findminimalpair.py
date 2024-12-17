import itertools
import jaconv
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
def find_first_char_diff_minimal_pairs(words_with_ro, words_with_bo):
    minimal_pairs = []
    
    for word_ro, kanji_ro, freq_ro in words_with_ro:
        for word_bo, kanji_bo, freq_bo in words_with_bo:
            # 長さが同じで、一文字目だけが違う場合
            if (len(word_ro) == len(word_bo) and 
                word_ro[0] != word_bo[0] and 
                word_ro[1:] == word_bo[1:] and 
                freq_ro > 100 and freq_bo > 100):
                minimal_pairs.append((word_ro, word_bo, kanji_ro, kanji_bo, freq_ro, freq_bo))
    
    return minimal_pairs

# ミニマルペアを頻度順にソート
def sort_minimal_pairs_by_frequency(minimal_pairs):
    return sorted(minimal_pairs, key=lambda pair: (pair[4] + pair[5]), reverse=True)

# 結果を表示する関数
def display_minimal_pairs(minimal_pairs):
    print("頻度順のミニマルペア:")
    for pair in minimal_pairs:
        print(f"{pair[0]} - {pair[1]} ({pair[2]} - {pair[3]}) 頻度: {pair[4]} + {pair[5]}")

    # ひらがなでも表示
    #print("\nひらがなでのミニマルペア:")
    #for pair in minimal_pairs:
      #  hiragana_pair = (jaconv.kata2hira(pair[0]), jaconv.kata2hira(pair[1]))
       # print(f"{hiragana_pair[0]} - {hiragana_pair[1]} ({pair[2]} - {pair[3]}) 頻度: {pair[4]} + {pair[5]}")

# メイン処理
def main():
    corpus_file_path = r'C:/yourapass' 
    if os.path.exists(corpus_file_path):
        corpus = load_corpus(corpus_file_path)
        words_with_ro, words_with_bo = extract_words_with_ro_bo(corpus)
        minimal_pairs = find_first_char_diff_minimal_pairs(words_with_ro, words_with_bo)
        sorted_minimal_pairs = sort_minimal_pairs_by_frequency(minimal_pairs)
        display_minimal_pairs(sorted_minimal_pairs)
    else:
        print("ファイルが存在しません")

if __name__ == "__main__":
    main()
