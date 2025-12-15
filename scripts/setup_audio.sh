#!/bin/bash
# オーディオデバイス設定スクリプト

set -e

echo "=== IVRyaa オーディオセットアップ ==="

# macOSの場合
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS環境を検出しました"

    # PortAudioのインストール確認
    if ! brew list portaudio &>/dev/null; then
        echo "PortAudioをインストールしています..."
        brew install portaudio
    else
        echo "PortAudioはインストール済みです"
    fi

    # 入力デバイスの確認
    echo ""
    echo "利用可能なオーディオ入力デバイス:"
    system_profiler SPAudioDataType | grep -A2 "Input"

# Linuxの場合
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux環境を検出しました"

    # ALSA/PulseAudioの確認
    if command -v arecord &>/dev/null; then
        echo ""
        echo "利用可能なオーディオ入力デバイス:"
        arecord -l
    fi

    # 必要なパッケージのインストール案内
    echo ""
    echo "必要なパッケージ (Debian/Ubuntu):"
    echo "  sudo apt-get install portaudio19-dev python3-pyaudio"
fi

echo ""
echo "セットアップ完了"
