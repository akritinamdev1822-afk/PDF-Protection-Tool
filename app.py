from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import tempfile
from pdf_handler import encrypt_pdf, decrypt_pdf
from password_utils import check_password_strength, generate_strong_password
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze_password', methods=['POST'])
def analyze_password():
    data = request.json
    pwd = data.get('password', '')
    strength, color = check_password_strength(pwd)
    return jsonify({"strength": strength, "color": color})

@app.route('/api/generate_password', methods=['GET'])
def generate_password():
    pwd = generate_strong_password()
    return jsonify({"password": pwd})

@app.route('/api/process', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    password = request.form.get('password', '')
    action = request.form.get('action', 'encrypt')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_processed_{filename}")
    
    file.save(input_path)
    
    if action == 'encrypt':
        success, message = encrypt_pdf(input_path, output_path, password)
    else:
        success, message = decrypt_pdf(input_path, output_path, password)
        
    if not success:
        return jsonify({"error": message}), 400
        
    return jsonify({"success": True, "download_url": f"/download/{unique_id}_processed_{filename}"})

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    # Open the browser dynamically shortly after server starts
    
    app.run(debug=True, port=5000, use_reloader=False)
