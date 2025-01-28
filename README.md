# SteganoMaster - Advanced Steganography Tool

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

SteganoMaster is a comprehensive steganography solution that enables secure data hiding in digital media files with built-in encryption and detection capabilities.

## Features

- **Multi-Format Support**:
  - 🖼️ Images: PNG, JPG
  - 🔊 Audio: WAV, MP3
  - 🎥 Video: MP4, AVI
- **Advanced Operations**:
  - 🔒 Hide data with AES-256 encryption
  - 🔓 Extract encrypted data
  - 🔍 Detect steganographic anomalies
- **Dual Interfaces**:
  - 🖥️ Graphical User Interface (GUI)
  - 💻 Command Line Interface (CLI)
- **Security**:
  - Military-grade encryption (AES-256-CBC)
  - PBKDF2 key derivation
  - Password protection
- **Detection Methods**:
  - Statistical analysis (LSB anomalies)
  - Phase pattern detection (audio)
  - Frame-by-frame analysis (video)

## Installation

### Requirements
- Python 3.8+
- FFmpeg (for video processing)

```bash
# Install dependencies
pip install Pillow numpy pydub opencv-python-headless cryptography wave tqdm tk

# Install FFmpeg (Ubuntu/Debian)
sudo apt install ffmpeg

# For Windows, download FFmpeg from https://ffmpeg.org/
```
# Usage
# Command Line Interface (CLI)

```bash
# Hide data
python cli.py hide -c cover.jpg -s secret.txt -o output.png -p "strongpassword"

# Extract data
python cli.py extract -i output.png -o secret.txt -p "strongpassword"

# Detect anomalies
python cli.py detect -f suspicious.mp4
```
# Graphical User Interface (GUI)
```bash python gui.py ```

# Hide Tab

- **Select cover file and secret file**
- **Set password and output path**
- **Choose from supported formats**

# Extract Tab

- **Load stego file**
- **Provide decryption password**
- **Specify output location**

# Detect Tab

- **Analyze suspicious files**
- **Get instant detection results**

# Supported Formats

| Media Type | Formats          | Encoding Method               |
|------------|------------------|-------------------------------|
| Images     | PNG, JPG         | LSB Steganography             |
| Audio      | WAV, MP3         | Phase/LSB Encoding            |
| Video      | MP4, AVI         | Frame-based LSB Encoding      |

# Security Implementation

### Data protection features:
- AES-256-CBC encryption
- 100,000 PBKDF2 iterations
- Random salt/IV generation
- PKCS7 padding

# Detection Methods

## Image Analysis:
- LSB distribution analysis
- Chi-square statistical test
- Visual attack detection

## Audio Analysis:
- Phase correlation checks
- LSB distribution analysis
- Spectral anomaly detection

## Video Analysis:
- Frame consistency checks
- Motion vector analysis
- Temporal anomaly detection



# Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/improvement`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/improvement`
5. Create a Pull Request

# License
MIT License - See LICENSE for details
