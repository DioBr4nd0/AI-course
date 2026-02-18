import qrcode
from PIL import Image

def generate_qr_code(url, output_filename):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the URL to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(output_filename)

def main():
    url = input("Enter a URL: ")
    output_filename = "output.png"
    generate_qr_code(url, output_filename)
    print(f"QR code saved as {output_filename}")

if __name__ == "__main__":
    main()