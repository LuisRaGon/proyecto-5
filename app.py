from flask import Flask
from flask.scaffold import F
from flask import render_template 
from flask import redirect
from flask import request

app = Flask(__name__)

#lista de usuarios----------------------

lista_usuarios =["juan","maria"]

#----------------------------------------------------------------------------

#lista de citas---------------------------------------------------

lista_citas={
    1: "Medico carlos",
    2: "Medico julian",
    3: "Medico alex",
    4: "Medico carmen",
}


sesion_iniciada =False



#pagina inicio--------------

@app.route('/', methods=["Get"])

def home():
    return  render_template ("index.html")


# registro--------------

@app.route('/registro', methods=["Get","POST"])
def registro():
    return render_template("/registro.html") 


# <Sesión iniciada---------------------------





#pagina login--------------

@app.route('/login', methods=["Get","POST"])
def login():
    global sesion_iniciada
    if request.method == "GET":
        return render_template("login.html")
    else:
        sesion_iniciada = True
        return render_template("perfil_usuario_paciente.html", sesion_iniciada)    
    

# salida---------------------------------------
@app.route('/salir', methods=["POST"])
def salir():
    global sesion_iniciada
    sesion_iniciada =False
    return redirect ("inicio")    


#perfil usuario paciente-------- 

@app.route('/perfil_usuario_paciente/<id_usuario_paciente>', methods=["Get","POST"])
def usuario_paciente(id_usuario_paciente):
    if id_usuario_paciente in lista_usuarios:
        return render_template ("perfil_usuario_paciente.html")
    else:
         return f"Error el Usuario {id_usuario_paciente} no existe"



# actualizar datos paciente--------------


@app.route('/actualizar_datos_paciente', methods=["Get","POST"])
def actualizar_datos_paciente():
     return render_template("/actualizar_datos_paciente.html")

# solicitar cita medica-------------------------

@app.route('/solicitar_cita_medica/<id_cita>', methods=["Get","POST"])
def solicitar_cita_medica(id_cita):

    try:
        id_cita = int (id_cita)
    except Exception as e:

        id_cita=0
       
    
    
    if id_cita in lista_citas:
        
            return render_template ("solicitar_cita_medica.html")
                
    else: 
                return f"error  {id_cita}"
            
        


#actualizar datos medico-------------- 

@app.route('/actualizar_datos_medico', methods=["Get","POST"])
def actualizar_datos_medico():
    return render_template("/actualizar_datos_medico.html")

# cancelar cita--------------------------

@app.route('/cancelar_cita', methods=["Get"])
def cancelar_cita():
    return render_template("/cancelar_cita.html")

# conozcanos----------------------

@app.route('/conozcanos', methods=["Get"])
def conozcanos():
      return render_template("/conozcanos.html")

# contactenos-------------------------

@app.route('/contactenos', methods=["Get"])
def contactenos():
    return render_template("/contactenos.html")

#Detalle cita--------------------------

@app.route('/detalle_cita', methods=["Get"])
def detalle_cita():
     return render_template("/detalle_cita.html")


# Historial cita pacientes--------------------     

@app.route('/historial_citas_paciente', methods=["Get"])
def historial_paciente():
     return render_template("/historial_citas_paciente.html")

#olvidar contraseña--------------------------

@app.route('/olvidarcontrasena', methods=["Get"])
def olvidarcontrasena():
     return render_template("/olvidarcontrasena.html")

#Perfil del medico--------------------------

@app.route('/perfil_usuario_medico', methods=["Get"])
def perfil_usuario_medico():
     return render_template("/perfil_usuario_medico.html")     

#gestionar citas medico--------------------------

@app.route('/gestionar_citas_medico', methods=["Get"])
def gestionar_citas_medico():
     return render_template("/gestionar_citas_medico.html")  

#Historia Clinica --------------------------

@app.route('/historia_clinica', methods=["Get","POST"])
def historia_clinica():
     return render_template("/historia_clinica.html")  

#Historia Clinica --------------------------

@app.route('/nueva_consulta', methods=["Get","POST"])
def nueva_consulta():
     return render_template("/nueva_consulta.html")   



# Modificar Cronogrma citas -------------------------

@app.route('/cronograma_citas', methods=["Get"])
def cronograma_citas():
     return render_template("/cronograma_citas.html")  




if __name__ == '__main__':
    app.run(debug=True)
