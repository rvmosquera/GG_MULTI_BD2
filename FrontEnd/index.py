#Flask levantar pagina
#render_t... para el html
import face_recognition
from flask import Flask, render_template, jsonify, request, redirect,send_from_directory
import face_recognition as fr
from lectura import KNN_Seq
from lectura import KNN_rtree
import json

dirFotos="../BackEnd/Project3/Data/tmp/lfw/"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Ruta para la pagina principal
@app.route('/')
def home():
    #return 'Home Page'
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    # Check if a valid image file was uploaded

    path = '/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/Test_1'
    datapath = '/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/tmp/lfw/'
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        KNN = request.form['KNN']
        kvalue = request.form['kvalue']
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if KNN == 'Sequential':
            if file and allowed_file(file.filename):
            
                img = fr.load_image_file(path + '/' + file.filename)
                query =  fr.face_encodings(img)[0]

                data = KNN_Seq(int(kvalue),query,100, datapath)
                              
                return render_template("result2.html",result = data)
        if KNN == 'RTree':
            if file and allowed_file(file.filename):
                data = []
                #img = face_recognition.load_image_file(file)
                img = fr.load_image_file(path + '/' + file.filename)
                query2 =  fr.face_encodings(img)[0]

                #query2 = face_recognition.face_encodings(img)[0]
                
                data = KNN_rtree(int(kvalue),query2,10)

                return render_template("result.html",result = data)
    # NO imagen
    return render_template('home.html')


#Ruta para la pagina Resultado
#@app.route('/result')
#def result():
    #return 'About Page'
#    return render_template('result.html')

@app.route('/integrantes')
def integrantes():  
    return render_template('integrantes.html')

@app.route("/image/<directorio>/<filename>") 
def show_image(filename,directorio): 
    directory = dirFotos+directorio
    return send_from_directory(directory, filename)



@app.route('/capture')
def capture():  
    return render_template('capture.html')
#Validacion de archivo principal
if __name__ == '__main__':
    #app.run()
    #Entrar modo de prueba y no estar corriendo la pagina
    app.run(host='0.0.0.0', port=5001, debug=True)

