from flask import Flask, request, render_template, send_file
import whisper
import os

app = Flask(__name__)


modelo = whisper.load_model('base')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        
        audio_path = os.path.join('uploads', file.filename)
        file.save(audio_path)
        
     
        resposta = modelo.transcribe(audio_path)
        texto = resposta['text']
        
        
        output_file = 'transcricao.txt'
        with open(output_file, 'w') as f:
            f.write(texto)
        
   
        os.remove(audio_path)
        
      
        return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
