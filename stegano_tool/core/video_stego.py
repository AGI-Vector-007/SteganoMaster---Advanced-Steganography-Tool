import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import logging
from typing import Optional
from .image_stego import hide_data_without_header, extract_data_without_header

logger = logging.getLogger(__name__)

def hide_data_frames(cover_path: str, data: bytes, output_path: str, password: Optional[str] = None) -> None:
    try:
        if password:
            from .encryption import encrypt_data
            data = encrypt_data(password, data)

        cap = cv2.VideoCapture(cover_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Calculate max data per frame (3 bits per pixel)
        max_bits_per_frame = frame_width * frame_height * 3
        max_bytes_per_frame = max_bits_per_frame // 8
        
        # Prepend 4-byte data length header
        data_with_header = len(data).to_bytes(4, 'big') + data
        chunks = [data_with_header[i:i+max_bytes_per_frame] 
                 for i in range(0, len(data_with_header), max_bytes_per_frame)]
        
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        chunk_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            if chunk_idx < len(chunks):
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    temp_path = tmp.name
                
                # Hide chunk in frame
                hide_data_without_header(pil_img, chunks[chunk_idx], temp_path)
                mod_frame = cv2.cvtColor(cv2.imread(temp_path), cv2.COLOR_BGR2RGB)
                os.unlink(temp_path)
                
                out.write(mod_frame)
                chunk_idx += 1
            else:
                out.write(frame)
        
        cap.release()
        out.release()
        logger.info(f"Data hidden in {output_path}")

    except Exception as e:
        logger.error(f"Video frame hide error: {e}")
        raise

def extract_data_frames(stego_path: str, password: Optional[str] = None) -> bytes:
    try:
        cap = cv2.VideoCapture(stego_path)
        extracted = bytearray()
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        max_bytes_per_frame = (frame_width * frame_height * 3) // 8
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                temp_path = tmp.name
            pil_img.save(temp_path)
            
            chunk = extract_data_without_header(temp_path, max_bytes_per_frame)
            extracted.extend(chunk)
            os.unlink(temp_path)
        
        cap.release()
        
        # Parse header and decrypt
        data_len = int.from_bytes(extracted[:4], 'big')
        result = bytes(extracted[4:4+data_len])
        
        if password:
            from .encryption import decrypt_data
            result = decrypt_data(password, result)
        
        return result

    except Exception as e:
        logger.error(f"Video frame extract error: {e}")
        raise

def detect_anomalies_video(video_path: str) -> bool:
    try:
        cap = cv2.VideoCapture(video_path)
        anomaly = False
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                temp_path = tmp.name
            pil_img.save(temp_path)
            
            if detect_anomalies(temp_path):
                anomaly = True
                break
            os.unlink(temp_path)
        
        cap.release()
        return anomaly

    except Exception as e:
        logger.error(f"Video detection error: {e}")
        raise
