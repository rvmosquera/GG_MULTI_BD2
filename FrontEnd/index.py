#Flask levantar pagina
#render_t... para el html
import face_recognition
from flask import Flask, render_template, jsonify, request, redirect
import face_recognition as fr
from lectura import KNN_Seq
from lectura import knnRtree
import json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded

    path = '/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/Test_1'
    datapath = '/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/Collection/lfw'
    datapath2 = '/home/raiko/GG_MULTI_BD2/BackEnd'
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
                
                results = '''
                    <!doctype html>
                    <title>Buscador</title>
                    <h1>Buscador-seq</h1>
                    <label for="cars">Busqueda KNN:</label>
                    <select name="KNN" id="KNN" form="form">
                      <option value="RTree">RTree</option>
                      <option value="Sequential">Sequential</option>
                    </select>
                    <form method="POST" enctype="multipart/form-data" id="form">
                      <input type="number" name="kvalue">
                      <input type="file" name="file">
                      <input type="submit" value="Cargar">
                    </form>
                    '''
                
                for i in range(len(data)):
                    results += '''<img src=" '''+data[i][1]+ '''" class="img-fluid">
                                
                                <label>'''+data[i][1]+'''</label>
                                '''
                return results
        if KNN == 'RTree':
            if file and allowed_file(file.filename):
                data = []
                img = face_recognition.load_image_file(file)
                query2 = face_recognition.face_encodings(img)[0]
            
                data = knnRtree(int(kvalue),query2,10, datapath2)
                results = '''
                    <!doctype html>
                    <title>Buscador</title>
                    <h1>Buscador-RTree</h1>
                    <label for="cars">Busqueda KNN:</label>
                    <select name="KNN" id="KNN" form="form">
                      <option value="RTree">RTree</option>
                      <option value="Sequential">Sequential</option>
                    </select>
                    <form method="POST" enctype="multipart/form-data" id="form">
                      <input type="number" name="kvalue">
                      <input type="file" name="file">
                      <input type="submit" value="Cargar">
                    </form>
                    '''
                for i in range(len(data)):
                    results += '''<img src=" '''+data[i][1]+ '''" class="img-fluid">
                                
                                <label>'''+data[i][1]+'''</label>
                                '''
                return results

    # NO imagen
    return '''
        <!doctype html>
        <title>Buscador</title>
        <h1>Buscador-1</h1>
        <label for="cars">Busqueda KNN:</label>
        <select name="KNN" id="KNN" form="form">
        <option value="RTree">RTree</option>
        <option value="Sequential">Sequential</option>
        </select>
        <form method="POST" enctype="multipart/form-data" id="form">
        <input type="number" name="kvalue">
        <input type="file" name="file">
        <input type="submit" value="Cargar">
        </form>
        '''



def detect_faces_in_image(file_stream):

    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    picture_of_vizcarra = face_recognition.load_image_file("/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/Test_2/vizcarra.png")    
    known_face_encoding = face_recognition.face_encodings(picture_of_vizcarra)[0]
    

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    
    face_found = False
    is_vizcarra = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        for i in range(len(unknown_face_encodings)):
            match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[i])
        # Your can use the distance to return a ranking of faces <face, dist>. 
        # face_recognition.face_distance([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_vizcarra = True

    # Return the result as json
    result = {
        "rostro_encontrado_en_imagen": face_found,
        "es_foto_de_vizcarra": is_vizcarra
    }
    return jsonify(result)




#Ruta para la pagina principal
@app.route('/')
def home():
    #return 'Home Page'
    return render_template('home.html')

#Ruta para la pagina Resultado
@app.route('/result')
def result():
    #return 'About Page'
    return render_template('result.html')

@app.route('/integrantes')
def integrantes():  
    return render_template('integrantes.html')

@app.route('/capture')
def capture():  
    return render_template('capture.html')
#Validacion de archivo principal
if __name__ == '__main__':
    #app.run()
    #Entrar modo de prueba y no estar corriendo la pagina
    app.run(host='0.0.0.0', port=5001, debug=True)

