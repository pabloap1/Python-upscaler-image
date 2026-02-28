import os
from flask import Flask, render_template, request, send_file, flash, redirect
from PIL import Image

app = Flask(__name__)
app.secret_key = "super_secreto" # Necesario para mostrar mensajes de error
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale_image():
    if 'file' not in request.files:
        flash('No se subió ningún archivo')
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        flash('No seleccionaste ninguna imagen')
        return redirect('/')

    if file:
        # 1. Abrir la imagen subida
        img = Image.open(file.stream)
        
        # 2. Calcular la nueva resolución (ejemplo: 2x más grande)
        factor = 2
        new_width = int(img.width * factor)
        new_height = int(img.height * factor)
        
        # 3. Reescalar usando el filtro LANCZOS (el mejor para interpolación)
        upscaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 4. Guardar temporalmente la imagen procesada
        output_path = os.path.join(UPLOAD_FOLDER, f"upscaled_{file.filename}")
        
        # Convertir a RGB si es necesario (para guardar en JPEG)
        if upscaled_img.mode in ("RGBA", "P"):
            upscaled_img = upscaled_img.convert("RGB")
            
        upscaled_img.save(output_path, quality=95)
        
        # 5. Enviar el archivo al usuario para que lo descargue
        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
