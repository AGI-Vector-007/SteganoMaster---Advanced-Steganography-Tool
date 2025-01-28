import argparse
from core.encryption import encrypt_data, decrypt_data
from core.image_stego import hide_data, extract_data, detect_anomalies
import logging
import sys

def main():
    parser = argparse.ArgumentParser(description="Steganography CLI Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Hide command
    hide_parser = subparsers.add_parser('hide')
    hide_parser.add_argument('-c', '--cover', required=True)
    hide_parser.add_argument('-s', '--secret', required=True)
    hide_parser.add_argument('-o', '--output', required=True)
    hide_parser.add_argument('-p', '--password', required=True)

    # Extract command
    extract_parser = subparsers.add_parser('extract')
    extract_parser.add_argument('-i', '--input', required=True)
    extract_parser.add_argument('-o', '--output', required=True)
    extract_parser.add_argument('-p', '--password', required=True)

    # Detect command
    detect_parser = subparsers.add_parser('detect')
    detect_parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    try:
        if args.command == 'hide':
            with open(args.secret, 'rb') as f:
                encrypted = encrypt_data(args.password, f.read())
            hide_data(args.cover, encrypted, args.output)
            print("Data hidden successfully")
        
        elif args.command == 'extract':
            data = decrypt_data(args.password, extract_data(args.input))
            with open(args.output, 'wb') as f:
                f.write(data)
            print("Data extracted successfully")
        
        elif args.command == 'detect':
            print(f"Steganography detected: {detect_anomalies(args.file)}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
