# Enhanced Steganography Tool

A robust Python-based steganography tool that lets you securely hide text messages within image files. This project demonstrates the implementation of steganography techniques by encoding messages in the least significant bits of image pixels, combined with password-based encryption for added security.

## Features

- **Message Encoding**: Hide text messages securely within image files
- **Password Protection**: Secure your hidden messages with strong SHA-256 based encryption
- **Magic Number Headers**: Reliable message identification with "STEGO" header format
- **Command Line Interface**: User-friendly encode/decode operations
- **Comprehensive Error Handling**: Clear feedback for all operations
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

## How Steganography Works

Steganography is the practice of hiding information within ordinary, non-secret data or a physical object to avoid detection. This tool implements LSB (Least Significant Bit) steganography, where we:

1. Read each pixel's color channel values from the source image
2. Replace the least significant bit of each byte with a bit from our encrypted message
3. Since changing only the least significant bit causes minimal visual change, the modified image looks identical to the human eye
4. The encoded image can be shared normally, with the hidden message only accessible to those with the password

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/mr-tweaker/steganography-enhanced.git
   cd steganography-enhanced
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Encoding a Message

To hide a message in an image:

```bash
python stego_enhanced.py encode -i [input_image_path] -o [output_image_path]
```

Example:
```bash
python stego_enhanced.py encode -i sample_images/original.png -o secret_image.png
```

If you don't specify an output path, it defaults to "encoded_image.png".

You'll be prompted to enter:
- Your secret message
- A password to secure the message

### Decoding a Message

To extract a hidden message from an image:

```bash
python stego_enhanced.py decode -i [image_with_hidden_message]
```

Example:
```bash
python stego_enhanced.py decode -i encoded_image.png
```

You'll need to enter the same password used during encoding.

## Technical Details

This tool uses several techniques to ensure reliability and security:

1. **Message Structure**: 
   - A "STEGO" magic number header identifies valid steganographic images
   - Message length is stored in the header for accurate extraction

2. **Encryption**:
   - Password is hashed using SHA-256
   - Message is encrypted with XOR cipher using the hashed password as the key

3. **Bit Manipulation**:
   - Messages are converted to binary and embedded bit by bit
   - Only the least significant bit of each color channel is modified

## Best Practices

For optimal results:

- Use PNG format for both input and output images (avoid lossy formats like JPEG)
- Larger images can store longer messages
- Keep your password secure - it cannot be recovered if lost
- Images with varied colors and patterns work best for hiding messages

## Sample Images

The `sample_images` directory contains test images you can use to experiment with the tool.

## Limitations

- Works best with lossless image formats (PNG recommended)
- Message length is limited by image dimensions
- Not resistant to image manipulation (cropping, resizing, or compression)

## Future Improvements

- Support for hiding files (not just text)
- Advanced encryption methods
- Steganography detection resistance 
- Graphical user interface

## License

MIT

## Author

Aniket Lamba