import cv2
import os
import numpy as np
import argparse
from getpass import getpass
import hashlib

def encode_message(image_path, message, password, output_path="encoded_image.png"):
    """
    Encodes a secret message into an image using steganography.
    
    Args:
        image_path (str): Path to the original image
        message (str): Secret message to encode
        password (str): Password for encryption
        output_path (str): Path to save the encoded image
    
    Returns:
        bool: True if encoding was successful, False otherwise
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return False
            
        # Get image dimensions
        height, width, channels = img.shape
        
        # Calculate maximum message length that can be encoded
        max_bytes = (height * width * 3) // 8 - 64  # Leave room for the header
        
        # Check if message can fit in the image
        message_length = len(message)
        if message_length > max_bytes:
            print(f"Error: Message too long. Maximum length is {max_bytes} characters.")
            return False
            
        # Create a simple encryption key from the password
        import hashlib
        key = hashlib.sha256(password.encode()).digest()
        
        # Encrypt the message - very basic XOR encryption
        encrypted_message = bytearray()
        for i, char in enumerate(message.encode()):
            encrypted_message.append(char ^ key[i % len(key)])
            
        # Add a fixed header with message length for easier decoding
        # Use "STEGO" as a magic number, followed by the message length as 4 bytes
        header = bytearray(b'STEGO') + len(encrypted_message).to_bytes(4, byteorder='big')
        
        # Combine header and encrypted message
        data_to_hide = header + encrypted_message
        
        # Convert to binary
        binary_data = ''.join(format(byte, '08b') for byte in data_to_hide)
        
        # Embed data in image
        data_index = 0
        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    if data_index < len(binary_data):
                        # Set the least significant bit
                        img[row, col, channel] = (img[row, col, channel] & 0xFE) | int(binary_data[data_index])
                        data_index += 1
                    else:
                        # We're done embedding
                        break
                        
        # Save the encoded image
        cv2.imwrite(output_path, img)
        print(f"Message successfully encoded in {output_path}")
        
        # Try to display the image - but don't worry if it fails
        try:
            if os.name == 'nt':  # Windows
                os.system(f"start {output_path}")
            elif os.name == 'posix':  # Linux or macOS
                # Try different methods to open the image
                if os.system("which xdg-open > /dev/null 2>&1") == 0:
                    os.system(f"xdg-open {output_path} > /dev/null 2>&1")
                elif os.system("which display > /dev/null 2>&1") == 0:  # ImageMagick
                    os.system(f"display {output_path} > /dev/null 2>&1 &")
                elif os.system("which eog > /dev/null 2>&1") == 0:  # Eye of GNOME
                    os.system(f"eog {output_path} > /dev/null 2>&1 &")
                elif os.system("which open > /dev/null 2>&1") == 0:  # macOS
                    os.system(f"open {output_path} > /dev/null 2>&1")
        except:
            # Not being able to open the image doesn't affect the encoding process
            pass
            
        return True
        
    except Exception as e:
        print(f"Error during encoding: {e}")
        return False

def decode_message(image_path, password):
    """
    Decodes a secret message from an image that contains steganography.
    
    Args:
        image_path (str): Path to the encoded image
        password (str): Password used for encryption
    
    Returns:
        str: Decoded message if successful, None otherwise
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return None
            
        # Get image dimensions
        height, width, channels = img.shape
        
        # Extract bits from the image
        extracted_bits = ""
        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    # Get the least significant bit
                    extracted_bits += str(img[row, col, channel] & 1)
                    
                    # Check if we have enough bits for the header (5 bytes for 'STEGO' + 4 bytes for length)
                    if len(extracted_bits) >= 72:  # 9 bytes * 8 bits
                        # Convert first 40 bits (5 bytes) to check for 'STEGO' magic number
                        header_bytes = bytearray()
                        for i in range(0, 40, 8):
                            byte_bits = extracted_bits[i:i+8]
                            header_bytes.append(int(byte_bits, 2))
                            
                        # Check if this is a valid steganography file
                        if header_bytes != b'STEGO':
                            # Just continue collecting bits - might be a false start
                            continue
                            
                        # Extract the message length (next 32 bits / 4 bytes)
                        length_bits = extracted_bits[40:72]
                        message_length_bytes = bytearray()
                        for i in range(0, 32, 8):
                            byte_bits = length_bits[i:i+8]
                            message_length_bytes.append(int(byte_bits, 2))
                            
                        # Convert to integer
                        message_length = int.from_bytes(message_length_bytes, byteorder='big')
                        
                        # Safety check for unreasonable message sizes
                        if message_length <= 0 or message_length > (height * width * channels) // 8:
                            # Just continue collecting bits - might be a false start
                            continue
                            
                        # Calculate how many more bits we need
                        bits_needed = message_length * 8
                        total_bits_needed = 72 + bits_needed  # Header + message
                        
                        # If we don't have enough bits yet, continue extraction
                        if len(extracted_bits) < total_bits_needed:
                            continue
                        
                        # We have all the bits we need, extract the encrypted message
                        message_bits = extracted_bits[72:total_bits_needed]
                        
                        # Convert bits to bytes
                        encrypted_message = bytearray()
                        for i in range(0, len(message_bits), 8):
                            if i + 8 <= len(message_bits):
                                byte_bits = message_bits[i:i+8]
                                encrypted_message.append(int(byte_bits, 2))
                                
                        # Create decryption key from password
                        import hashlib
                        key = hashlib.sha256(password.encode()).digest()
                        
                        # Decrypt the message
                        decrypted_bytes = bytearray()
                        for i, byte in enumerate(encrypted_message):
                            decrypted_bytes.append(byte ^ key[i % len(key)])
                            
                        # Convert to string
                        try:
                            decrypted_message = decrypted_bytes.decode('utf-8', errors='replace')
                            return decrypted_message
                        except UnicodeDecodeError:
                            # If we got here with a valid STEGO header but can't decode,
                            # it's likely an incorrect password
                            print("Failed to decode message. Incorrect password most likely.")
                            return None
        
        # If we get here, we didn't find a valid message
        print("No steganography message detected in this image.")
        return None
                        
    except Exception as e:
        print(f"Error during decoding: {e}")
        return None

def binary_to_string(binary):
    """Convert binary to string of characters."""
    message = ""
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):  # Ensure we have a full byte
            byte = binary[i:i+8]
            message += chr(int(byte, 2))
    return message

def main():
    """Main function to parse arguments and run the program."""
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    
    # Create subparsers for encode and decode commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Encode a message in an image")
    encode_parser.add_argument("-i", "--image", required=True, help="Path to input image")
    encode_parser.add_argument("-m", "--message", help="Message to encode (optional, if not provided will prompt)")
    encode_parser.add_argument("-o", "--output", default="encoded_image.png", help="Output image path")
    
    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("-i", "--image", required=True, help="Path to encoded image")
    
    args = parser.parse_args()
    
    if args.command == "encode":
        # Get message from arguments or prompt user
        message = args.message
        if not message:
            message = input("Enter secret message: ")
        
        # Prompt for password securely
        password = getpass("Enter password for encryption: ")
        
        # Encode the message
        success = encode_message(args.image, message, password, args.output)
        if success:
            print(f"\nEncoding successful! Your message is now hidden in: {args.output}")
            print(f"Use the decode command with the same password to extract it.")
        else:
            print("\nEncoding failed. Please check the error messages above.")
        
    elif args.command == "decode":
        # Prompt for password securely
        password = getpass("Enter password for decryption: ")
        
        # Decode the message
        message = decode_message(args.image, password)
        if message:
            print(f"\nDecryption successful!")
            print(f"Decoded message: {message}")
        else:
            print("\nFailed to decode any message. Possible reasons:")
            print("- Incorrect password")
            print("- The image doesn't contain a hidden message")
            print("- The image format was changed after encoding (e.g., converted from PNG to JPEG)")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()