from flask import Flask, session
from flask.scaffold import F
from flask import render_template 
from flask import redirect
from flask import request
import sqlite3
import os
from wtforms.compat import with_metaclass
import hashlib
from forms.registropaciente import Registropaciente
from forms.registromedico import Registromedico
from forms.registroadmin import Registroadmin  
from forms.login import Login



app = Flask(__name__)

app.secret_key = os.urandom(20)




#pagina inicio------------------------------------------------------------------

@app.route('/', methods=["Get"])

def home():
    return  render_template ("index.html")


#pagina login-----------------------------------------------------------------------------

@app.route('/login', methods=["Get","POST"])
def login():
    frm = Login()
    if frm.validate_on_submit():
        tipousuario = frm.tipousuario.data
        correo = frm.correo.data
        contrasena = frm.contrasena.data
         # Cifra la contraseña
        encrp = hashlib.sha256(contrasena.encode('utf-8'))
        pass_enc = encrp.hexdigest()
        with sqlite3.connect("clinica.db") as con: 
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM usuario WHERE tipoususario = ? AND correo = ? AND contrasena = ?", [tipousuario, correo, pass_enc])

            if cur.fetchone():

                rows = cur.fetchall()

                for usu in rows:
                    session["id_usuario"] = usu[0]
                    session["tipousuario"] = usu[2]
                    session["nombre"] = usu[4]
                    

                    if  session["tipousuario"] == "Paciente":

                        return redirect("/perfil_usuario_paciente.html", frm=frm)

                    elif session["tipousuario"] == "Medico":
            
                        return redirect("/perfil_usuario_medico.html", frm=frm)    

                    elif session["tipousuario"] == "Administrador":

                        return redirect("/perfil_admin.html", frm=frm)
           
           
           
            else:
                return "Usuario/Password incorrectos"    
    

    return render_template("login.html", frm=frm )
            


# registro Paciente----------------------------------------------------------------------

@app.route('/registropaciente', methods=["GET","POST"])
def registrar():
    frm = Registropaciente()
    if frm.validate_on_submit():
        if frm.enviar:
            
            tipodocumento = frm.tipodocumento.data
            numerodocumento = frm.numerodocumento.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            fechanacimiento = frm.fechanacimiento.data
            genero = frm.genero.data
            direccion = frm.direccion.data
            telefono = frm.telefono.data
            contrasena = frm.contrasena.data
            eps = frm.eps.data
              
            # Cifra la contraseña
            encrp = hashlib.sha256(contrasena.encode('utf-8'))
            pass_enc = encrp.hexdigest()
            # Conecta a la BD
            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                
                cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", ["Paciente", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                           
                # Ejecuta la sentencia SQL

                con.commit()

               

                cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                rows = cur.fetchall()
                id_usuario = 0

                for usu in rows:
                    id_usuario =  usu[0]

                
                #cur = con.cursor()
                cur.execute("INSERT INTO paciente ( id_paciente, eps ) VALUES (?,?)", [
                            id_usuario, eps])

                con.commit()
                return "Guardado con éxito <a href='/'>inicio</a>"

    return render_template("registropaciente.html", frm=frm)

    


# registro medico--------------------------------------------------------------------------------------------------------

@app.route('/registromedico', methods=["GET","POST"])
def registrarmedico():
    frm = Registromedico()
    if frm.validate_on_submit():
        if frm.enviar:
            
            tipodocumento = frm.tipodocumento.data
            numerodocumento = frm.numerodocumento.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            fechanacimiento = frm.fechanacimiento.data
            genero = frm.genero.data
            direccion = frm.direccion.data
            telefono = frm.telefono.data
            contrasena = frm.contrasena.data
            especialidad = frm.especialidad.data
            numeroregistro = frm.numeroregistro.data
              
            # Cifra la contraseña
            encrp = hashlib.sha256(contrasena.encode('utf-8'))
            pass_enc = encrp.hexdigest()
            # Conecta a la BD
            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", [ "Medico", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                           
                # Ejecuta la sentencia SQL


                con.commit()

                cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                rows = cur.fetchall()
                id_usuario = 0

                for usu in rows:
                    id_usuario =  usu[0]

                
                #cur = con.cursor()
                cur.execute("INSERT INTO medico ( id_medico, especialidad, numeroregistro ) VALUES (?,?,?)", [
                            id_usuario, especialidad, numeroregistro])

                con.commit()
                return "Guardado con éxito <a href='/'>inicio</a>"
               

    return render_template("registromedico.html", frm=frm)



# registro admin---------------------------------------------------------------------------------------------------------------

@app.route('/registroadmin', methods=["GET","POST"])
def registraradmin():
    frm = Registroadmin()
    if frm.validate_on_submit():
        if frm.enviar:
            tipodocumento = frm.tipodocumento.data
            numerodocumento = frm.numerodocumento.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            fechanacimiento = frm.fechanacimiento.data
            genero = frm.genero.data
            direccion = frm.direccion.data
            telefono = frm.telefono.data
            contrasena = frm.contrasena.data
            cargo = frm.cargo.data
            
              
            # Cifra la contraseña
            encrp = hashlib.sha256(contrasena.encode('utf-8'))
            pass_enc = encrp.hexdigest()
            # Conecta a la BD
            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", [ "Administrador", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                           
                # Ejecuta la sentencia SQL


                con.commit()

                cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                rows = cur.fetchall()
                id_usuario = 0

                for usu in rows:
                    id_usuario =  usu[0]

                
                #cur = con.cursor()
                cur.execute("INSERT INTO administrador ( id_administrador, cargo ) VALUES (?,?)", [
                            id_usuario, cargo])

                con.commit()
                return "Guardado con éxito <a href='/'>inicio</a>"

    return render_template("registroadmin.html", frm=frm)







#perfil usuario paciente-------- 

@app.route('/perfil_usuario_paciente', methods=["Get","POST"])
def usuario_paciente():
    
        return render_template ("perfil_usuario_paciente.html")
   



# actualizar datos paciente--------------


@app.route('/actualizar_datos_paciente', methods=["Get","POST"])
def actualizar_datos_paciente():
     return render_template("/actualizar_datos_paciente.html")

# solicitar cita medica-------------------------

@app.route('/solicitar_cita_medica', methods=["Get","POST"])
def solicitar_cita_medica():

        return render_template ("solicitar_cita_medica.html")
                
  
            
        


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



# actualizar Cronogrma citas -------------------------

@app.route('/Actualizar_cronograma_citas', methods=["Get"])
def Actualizar_cronograma_citas():
     return render_template("/Actualizar_cronograma_citas.html")       



# Pacientes Atendidos-------------------------
@app.route('/pacientes_atendidos', methods=["Get"])
def pacientes_atendidos():
     return render_template("/pacientes_atendidos.html")       

# Editar Comentario-------------------------
@app.route('/editar_comentario', methods=["Get"])
def editar_comentario():
     return render_template("/editar_comentario.html")       


# Calificar Atenciono-------------------------
@app.route('/calificar_atencion', methods=["Get"])
def calificar_atencion():
     return render_template("/calificar_atencion.html")  



# Perfil administrador------------------------------

@app.route("/perfil_admin")
def perfil_admin():
    return render_template("/perfil_admin.html")

# Perfil administrador----------------------------------

@app.route("/gestionar_usuarios_admin")
def gestionar_usuarios_admin():
    return render_template("/gestionar_usuarios_admin.html")

# Perfil administrador-----------------------------------------

@app.route("/gestionar_citas_admin")
def gestionar_citas_admin():
    return render_template("/gestionar_citas_admin.html")

# Perfil administrador----------------------------------------

@app.route("/gestionar_historia_clinica_admin")
def gestionar_historia_clinica_admin():
    return render_template("/gestionar_historia_clinica_admin.html")

# Perfil administrador--------------------------------------------------

@app.route("/editar_historia_clinica_admin")
def editar_historia_clinica_admin():
    return render_template("/editar_historia_clinica_admin.htlm")           




if __name__ == '__main__':
    app.run(debug=True)
