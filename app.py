from flask import Flask, request, send_file
import io
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

def encrypt_pdf(file_contents, password):
    input_pdf = io.BytesIO(file_contents)
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        page_details = reader.pages[i]
        writer.add_page(page_details)

    writer.encrypt(password)

    output_pdf = io.BytesIO()
    writer.write(output_pdf)

    return output_pdf.getvalue()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    password = request.form.get('password', 'rajesh')
    file_contents = file.read()

    encrypted_file_contents = encrypt_pdf(file_contents, password)
    
    return send_file(
        io.BytesIO(encrypted_file_contents),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='encryptedtickets.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
