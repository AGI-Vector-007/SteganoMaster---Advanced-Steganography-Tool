import wave
import numpy as np
from pydub import AudioSegment
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def hide_data_lsb(cover_path: str, data: bytes, output_path: str, password: Optional[str] = None) -> None:
    try:
        if password:
            from .encryption import encrypt_data
            data = encrypt_data(password, data)

        audio = AudioSegment.from_file(cover_path)
        raw_data = bytearray(audio.raw_data)
        
        # Prepend 4-byte data length header
        data_with_header = len(data).to_bytes(4, 'big') + data
        bits = ''.join(f"{byte:08b}" for byte in data_with_header)
        bits += '0' * (len(raw_data) - len(bits))  # Pad with zeros if needed
        
        if len(bits) > len(raw_data):
            raise ValueError("Insufficient audio capacity to hide data")
        
        # Modify LSB of each byte in raw audio data
        for i in range(len(bits)):
            raw_data[i] = (raw_data[i] & 0xFE) | int(bits[i])
        
        modified_audio = audio._spawn(raw_data)
        modified_audio.export(output_path, format=output_path.split('.')[-1])
        logger.info(f"Data hidden in {output_path}")

    except Exception as e:
        logger.error(f"Audio LSB hide error: {e}")
        raise

def extract_data_lsb(stego_path: str, password: Optional[str] = None) -> bytes:
    try:
        audio = AudioSegment.from_file(stego_path)
        raw_data = audio.raw_data
        
        # Extract first 32 bits (4-byte length header)
        length_bits = ''.join(str(byte & 1) for byte in raw_data[:32])
        data_len = int(length_bits, 2)
        
        # Extract total required bits
        total_bits = 32 + data_len * 8
        bits = ''.join(str(byte & 1) for byte in raw_data[:total_bits])
        
        # Convert to bytes
        data_bytes = bytes(int(bits[i:i+8], 2) for i in range(32, len(bits), 8))
        
        if password:
            from .encryption import decrypt_data
            data_bytes = decrypt_data(password, data_bytes)
        
        return data_bytes

    except Exception as e:
        logger.error(f"Audio LSB extract error: {e}")
        raise

def detect_anomalies_lsb(audio_path: str) -> bool:
    try:
        audio = AudioSegment.from_file(audio_path)
        lsb_dist = [byte & 1 for byte in audio.raw_data]
        avg = sum(lsb_dist) / len(lsb_dist)
        return abs(avg - 0.5) > 0.1  # Basic anomaly detection

    except Exception as e:
        logger.error(f"Audio LSB detection error: {e}")
        raise
