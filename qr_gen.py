
import qrcode
from PIL import Image, ImageDraw
import sys
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer

# Custom drawer for rounded corners on the alignment patterns
class CustomRoundedModuleDrawer(RoundedModuleDrawer):
    def __init__(self):
        super().__init__()
        self.border_width = 2

    def draw_alignment(self, image, center, size):
        """ Draw the alignment pattern with rounded corners """
        color = self.fill_color
        radius = size // 2
        # Draw a rounded rectangle around the corner square
        image.paste(color, [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius])
        return image

# Check if the URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python qr_code_generator.py <website_url> [rounded|square] [image_path] [inverted]")
    sys.exit(1)

# Get the website URL from the command-line argument
data = sys.argv[1]

# Check for the optional style argument
style = sys.argv[2].lower() if len(sys.argv) > 2 else "square"

# Get the image path for the logo (optional)
logo_path = sys.argv[3] if len(sys.argv) > 3 else None

# Check if inverted option is provided
inverted = len(sys.argv) > 4 and sys.argv[4].lower() == 'inverted'

# Determine the module drawer based on the style
module_drawer = CustomRoundedModuleDrawer() if style == "rounded" else SquareModuleDrawer()

# Create the QR code
qr = qrcode.QRCode(
    version=10,  # Larger version for higher resolution
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # Controls the size of each individual box
    border=4,  # Thickness of the border
)

qr.add_data(data)
qr.make(fit=True)

# Set the colors for the QR code
fill_color = "white" if inverted else "black"
back_color = "black" if inverted else "white"

# Create an image of the QR code with the selected style
img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer, fill_color=fill_color, back_color=back_color)

# Add logo in the center with a rounded-edge square background
if logo_path:
    logo = Image.open(logo_path)
    
    # Calculate the size and position for the logo in the center
    qr_width, qr_height = img.size
    max_logo_size = qr_width // 5  # Maximum logo size is 1/5th of the QR code width
    
    # Resize the logo while maintaining its aspect ratio
    logo.thumbnail((max_logo_size, max_logo_size))  # This resizes the logo while keeping its aspect ratio
    
    # Create a white rounded-edge square background for the logo
    bg_size = max_logo_size + 20  # The rounded square size will be logo size + padding
    rounded_square_bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))  # White background
    
    draw = ImageDraw.Draw(rounded_square_bg)
    radius = 15  # Radius for the corners of the square
    # Draw a rounded square (rounded corners)
    draw.rounded_rectangle(
        [(0, 0), (bg_size, bg_size)], 
        radius=radius, 
        fill=(255, 255, 255)  # White fill for the background
    )
    
    # Place the logo inside the rounded-edge square
    logo_position = ((bg_size - logo.size[0]) // 2, (bg_size - logo.size[1]) // 2)  # Center the logo inside the background
    rounded_square_bg.paste(logo, logo_position, logo)  # Paste logo with transparency

    # Get the position to place the rounded-edge square at the center of the QR code
    logo_position_on_qr = ((qr_width - bg_size) // 2, (qr_height - bg_size) // 2)
    
    # Paste the rounded-edge square onto the QR code
    img.paste(rounded_square_bg, logo_position_on_qr, rounded_square_bg)

# Save the image in high resolution
filename = "high_res_qr_code_with_logo_inverted.png" if inverted else "high_res_qr_code_with_logo.png"
img.save(filename, "PNG")

print(f"QR code saved as {filename} with {style} edges and a logo in a rounded-edge square.")
