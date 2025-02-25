# Sample Images for Steganography

This directory contains sample images you can use to test the steganography tool. These images serve as "carriers" for your hidden messages.

## Using Sample Images

1. **Select appropriate images**: Choose high-quality, uncompressed images when possible.

2. **Test with different image types**: Try various sizes, color patterns, and compositions to understand how they affect the steganography process.

3. **Important considerations**:
   - PNG format preserves your hidden message better than JPEG
   - Larger images can store longer messages
   - More complex images (with varied colors and patterns) better conceal the presence of steganography

## Recommended Image Characteristics

For the best steganography results, look for images with these qualities:

- **High resolution**: More pixels = more data storage capacity
- **Color variation**: Images with solid colors or gradients may show statistical anomalies after encoding
- **Visual complexity**: Busy patterns help hide the subtle changes from steganography
- **Uncompressed formats**: Always use PNG for the encoded output

## Adding Your Own Images

Feel free to add your own images to this directory. Make sure to note the original source and copyright information for any images you use.

## Testing Process

A good testing workflow includes:

1. Encode a message into a sample image
2. Verify the encoded image looks visually identical to the original
3. Successfully decode the message using the correct password
4. Try decoding with incorrect passwords to verify security

## Note

The original repository should include at least one sample image in this directory. If no images are present, you'll need to add your own before using the tool.