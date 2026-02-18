from qrcode import QRCode
import os

def generate_qr_code(url, output_file):
    qr = QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

if __name__ == "__main__":
    url = input("Enter the URL to generate QR code: ")
    output_file = "output.png"
    
    if os.path.exists(output_file):
        response = input(f"File {output_file} already exists. Do you want to overwrite it? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting program.")
            exit()
    
    generate_qr_code(url, output_file)