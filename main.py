from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']

    # Generate QR Code
    data = f"Full Name: {full_name}\nEmail: {email}\nPhone Number: {phone_number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR Code as PNG
    qr_img_path = 'output.png'
    qr_img.save(qr_img_path)

    # Convert PNG to PDF
    pdf_path = 'output.pdf'
    image = Image.open(qr_img_path)
    image.save(pdf_path, "PDF")

    return send_file(pdf_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
