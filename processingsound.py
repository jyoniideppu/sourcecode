import numpy as np
import soundfile as sf
from scipy.fft import fft, ifft

def remove_frequency_range_from_wav(input_wav, output_wav, min_freq, max_freq):
    # WAVファイルを読み込む
    data, sample_rate = sf.read(input_wav)
    
    # データを-1から1の範囲に正規化
    data = data / np.max(np.abs(data))
    
    # Fourier変換（周波数領域へ変換）
    freq_data = fft(data)
    
    # 周波数のインデックスを計算
    freqs = np.fft.fftfreq(len(data), d=1/sample_rate)
    
    # 正の周波数と負の周波数の両方をマスク
    # 複素共役の対称性を保持するため、絶対値を使用
    mask = (np.abs(freqs) >= min_freq) & (np.abs(freqs) <= max_freq)
    
    # 指定した周波数帯の振幅を0に設定
    freq_data[mask] = 0
    
    # 逆Fourier変換（時間領域に戻す）
    cleaned_data = np.real(ifft(freq_data))
    
    # データを正規化して16ビットの整数範囲に変換
    normalized_data = cleaned_data / np.max(np.abs(cleaned_data))
    cleaned_data_int16 = np.int16(normalized_data * 32767)
    
    # 処理後のデータをWAVファイルとして保存
    sf.write(output_wav, cleaned_data_int16, sample_rate)

# 使用例
input_wav = 'C:/yourpass/tetubou_1328.wav'
output_wav = 'teibouraw.wav'
min_freq = 0000
max_freq = 0000

remove_frequency_range_from_wav(input_wav, output_wav, min_freq, max_freq)
