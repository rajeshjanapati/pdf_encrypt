import base64
from PyPDF2 import PdfReader, PdfWriter
from flask import Flask, request, jsonify

app = Flask(__name__)
application=app

@app.route('/encrypt', methods=['POST'])
def encrypt_pdf():
    # Get the JSON data from the request
    data = request.get_json()
    
    if 'data' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Decode the base64-encoded PDF data
    try:
        pdf_data = base64.b64decode(data['data'])
    except Exception as e:
        return jsonify({'error': 'Invalid base64 data'}), 400
    
    password = data['password']
    
    # Read the PDF from the decoded bytes
    file_pdf = PdfReader(pdf_data)
    out_pdf = PdfWriter()

    for i in range(len(file_pdf.pages)):
        page_details = file_pdf.pages[i]
        out_pdf.add_page(page_details)

    # Encrypt the PDF with the provided password
    out_pdf.encrypt(password)
    
    # Create an output bytes buffer
    output_pdf_bytes = bytearray()
    with open("encryptedtickets.pdf", "wb") as output_file:
        out_pdf.write(output_file)
        output_file.seek(0)
        output_pdf_bytes.extend(output_file.read())

    # Encode the encrypted PDF as base64 to include in the JSON response
    encrypted_pdf_base64 = base64.b64encode(output_pdf_bytes).decode('utf-8')

    return jsonify({'encrypted_file': encrypted_pdf_base64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)