QR Code Generator with Custom Styling and Logo Overlay

This Python script generates a high-resolution QR code with optional styling, a logo overlay, and an inverted color scheme.

Features

Generate a QR code from a given URL.

Choose between rounded or square QR code modules.

Optionally, add a logo at the centre with a rounded-edge background.

Support for inverted colours (black-on-white or white-on-black).

Saves the QR code as a high-resolution PNG file.

Usage

Run the script from the command line:

python qr_code_generator.py <website_url> [rounded|square] [image_path] [inverted]

Arguments

<website_url>: The URL or text to encode in the QR code.

[rounded|square] (optional): Choose rounded or square QR code styles. The default is square.

[image_path] (optional): Path to a logo image to embed in the centre.

[inverted] (optional): Use inverted to generate a white-on-black QR code.

Example Commands

Generate a basic QR code:

python qr_code_generator.py "https://example.com"

Generate a QR code with rounded modules:

python qr_code_generator.py "https://example.com" rounded

Generate a QR code with a logo:

python qr_code_generator.py "https://example.com" square logo.png

Generate an inverted QR code with a logo and rounded modules:

python qr_code_generator.py "https://example.com" rounded logo.png inverted

