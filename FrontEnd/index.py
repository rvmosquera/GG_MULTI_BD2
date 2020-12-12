#Flask levantar pagina
#render_t... para el html
from flask import Flask, render_template

app = Flask(__name__)
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
    app.run(debug=True)