#!/bin/bash
# Audio device setup script

set -e

echo "=== IVRyaa Audio Setup ==="

# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS environment"

    # Check PortAudio installation
    if ! brew list portaudio &>/dev/null; then
        echo "Installing PortAudio..."
        brew install portaudio
    else
        echo "PortAudio is already installed"
    fi

    # Check input devices
    echo ""
    echo "Available audio input devices:"
    system_profiler SPAudioDataType | grep -A2 "Input"

# Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux environment"

    # Check ALSA/PulseAudio
    if command -v arecord &>/dev/null; then
        echo ""
        echo "Available audio input devices:"
        arecord -l
    fi

    # Required packages info
    echo ""
    echo "Required packages (Debian/Ubuntu):"
    echo "  sudo apt-get install portaudio19-dev python3-pyaudio"
fi

echo ""
echo "Setup complete"
