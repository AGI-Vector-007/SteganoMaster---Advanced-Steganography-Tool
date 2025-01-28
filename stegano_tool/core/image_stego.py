from PIL import Image
import numpy as np
import logging

logger = logging.getLogger(__name__)

def hide_data(cover_path: str, data: bytes, output_path: str) -> None:
    try:
        with Image.open(cover_path) as img:
            img = img.convert('RGB')
            array = np.array(img)
            data_len = len(data).to_bytes(4, 'big')
            bits = ''.join(f"{byte:08b}" for byte in data_len + data)
            bits += '0' * (array.size * 3 - len(bits))
            idx = 0
            for row in array:
                for pixel in row:
                    for i in range(3):
                        if idx < len(bits):
                            pixel[i] = (pixel[i] & 0xFE) | int(bits[idx])
                            idx += 1
            Image.fromarray(array).save(output_path)
            logger.info(f"Data hidden in {output_path}")
    except Exception as e:
        logger.error(f"Image hide error: {e}")
        raise

def extract_data(stego_path: str) -> bytes:
    try:
        with Image.open(stego_path) as img:
            array = np.array(img.convert('RGB'))
            bits = [str(pixel[i] & 1) for row in array for pixel in row for i in range(3)]
            length = int(''.join(bits[:32]), 2)
            data_bits = bits[32:32+length*8]
            return bytes(int(''.join(data_bits[i:i+8]), 2) for i in range(0, len(data_bits), 8))
    except Exception as e:
        logger.error(f"Image extract error: {e}")
        raise

def detect_anomalies(image_path: str) -> bool:
    try:
        with Image.open(image_path) as img:
            array = np.array(img.convert('RGB'))
            lsb = [pixel[i] % 2 for row in array for pixel in row for i in range(3)]
            avg = sum(lsb) / len(lsb)
            return abs(avg - 0.5) > 0.1  # Simple anomaly detection
    except Exception as e:
        logger.error(f"Detection error: {e}")
        raise

def hide_data_without_header(image: Image.Image, data: bytes, output_path: str) -> None:
    array = np.array(image.convert('RGB'))
    bits = ''.join(f"{byte:08b}" for byte in data)
    bits += '0' * (array.size * 3 - len(bits))
    idx = 0
    for row in array:
        for pixel in row:
            for i in range(3):
                if idx < len(bits):
                    pixel[i] = (pixel[i] & 0xFE) | int(bits[idx])
                    idx += 1
    Image.fromarray(array).save(output_path)

def extract_data_without_header(image_path: str, max_bytes: int) -> bytes:
    with Image.open(image_path) as img:
        array = np.array(img.convert('RGB'))
        bits = [str(pixel[i] & 1) for row in array for pixel in row for i in range(3)]
        data_bits = bits[:max_bytes*8]
        return bytes(int(''.join(data_bits[i:i+8]), 2) for i in range(0, len(data_bits), 8))
