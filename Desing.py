
# Importamos las librerías necesarias
from pathlib import Path
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import PIL.Image
from tkinter import Button, Image, Label, PhotoImage, ttk, messagebox
from datetime import datetime
from pygrabber.dshow_graph import FilterGraph
import tkinter as tk
import cv2
import os
import random 

global cameras_list

# Definimos las cámaras a utilizar
camerasName = ["Camara 1", "Camara 2", "Camara 3", "Camara 4", "Camara 5", "Camara 6"]
camerasLevel = [[0, 1], [2, 3], [4, 5]]
config_path = Path('Datos/config.txt')
names_config_path = Path('Datos/cameras.txt')

nivel_actual = 0
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def inicio():
    def cambio():
        for i in range(len(cameras_list)):
            camerasName[i] = names_level[i].get()
        set_cameras_names()
        root.destroy()
        main() 
    root = tk.Tk()
    root.config(bg='white')
    root.overrideredirect(True)
    
    #imagen_fondo = tk.PhotoImage(file=resource_path('xd.png'))
    #imagen_fondo =imagen_fondo.subsample(2)

    imagen_pil = PIL.Image.open("Datos/bg.png")

    # Aplicar un zoom a la inversa a la imagen
    zoom_factor = 0.8  
    imagen_pil_zoomed = imagen_pil.resize((int(imagen_pil.width * zoom_factor), int(imagen_pil.height * zoom_factor)))

    # Convertir la imagen de Pillow a un objeto PhotoImage
    imagen_fondo = Pil_imageTk.PhotoImage(imagen_pil_zoomed)

    # Establecer la imagen de fondo en la ventana
    background_label = tk.Label(root, image=imagen_fondo)
    background_label.place(x=-220, y=0, relwidth=1, relheight=1)
    root.minsize(1000, 600)
    background_label.config(bg='white')
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    wventana = 1000
    hventana = 600
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

    imagen_continuar = tk.PhotoImage(file=resource_path("Datos/Continue.png"))
    imagen_continuar = imagen_continuar.subsample(13)  # 13Submuestrea la imagen por un factor de 15
    imagen_cerrar = tk.PhotoImage(file=resource_path("Datos/Close.png"))
    imagen_cerrar = imagen_cerrar.subsample(17) #17

    # Botón "Cerrar" con imagen
    button_close = tk.Button(root, image=imagen_cerrar, command=root.destroy, bg="white", bd=0)
    button_close.pack(side=tk.LEFT, anchor='ne',padx=20, pady=20)

    # Crear un frame principal
    frame = tk.Frame(root)
    frame.configure(background="white")
    frame.pack(side=tk.RIGHT, padx=20, pady=(130,0), fill=tk.BOTH)

    names_level = []
    NC=len(cameras_list)
    Letrero_lista_camaras= tk.Frame(frame,bg="#FFFFFF")
    Letrero_lista_camaras.pack(side=tk.TOP)
    letrero=tk.Label(Letrero_lista_camaras,text=f"{NC} camaras encontradas",font=("Arial", 24),bg="#FFFFFF")
    letrero.pack(side=tk.TOP)

    for i in range(len(cameras_list)):
            row_frame = tk.Frame(frame,bg="#577BB4")
            row_frame.pack(side=tk.TOP, fill=tk.Y)
            level = tk.Label(row_frame, text=f" {i+1}: ",font=("Arial", 14),bg="#577BB4")
            name = tk.Entry(row_frame, font=("Arial", 14))
            name.insert(0, camerasName[i].split('\n')[0])
            names_level.append(name)
            level.pack(side=tk.LEFT, padx=10, pady=10, ipadx=10)
            name.pack(side=tk.LEFT, padx=10, pady=10, ipadx=20)

    # Botón "Continuar" con imagen redimensionada
    button_continue = tk.Button(frame, image=imagen_continuar, command=cambio, bg="white", bd=0)
    button_continue.pack(side=tk.RIGHT, anchor='se', padx=20, pady=20)

    button_reports2 = tk.Label(frame ,text="        ",bg="#ffffff", font=("Helvetica", 24))
    button_reports2.pack(side=tk.RIGHT, padx=0)
   

    default_index = [0]
    default_texts = ["Nombre por defecto 1", "Nombre por defecto 2"]

    ordenar_button = tk.Button(frame, text=default_texts[default_index[0]], font=("Arial", 12), bg="#577BB4",command=lambda: toggle_names_level(default_index))
    ordenar_button.pack(side=tk.BOTTOM, padx=20, pady=25)

    def toggle_names_level(default_index):
        if default_index[0] == 0:
            ordenar_button.config(text=default_texts[1])
            default_index[0] = 1
            print(default_index[0])
            for i, name in enumerate(names_level):
                name.delete(0, tk.END)
                name.insert(0, str(i + 1))
        else:
            ordenar_button.config(text=default_texts[0])
            default_index[0] = 0
            words = ["1 Izquierda", "3 Derecha", "2 Derecha", "3 Izquierda", "1 Derecha", "2 Izquierda"]
            for i, name in enumerate(names_level):
                name.delete(0, tk.END)
                name.insert(0, words[i % len(words)])

    def delete_files():
        if os.path.exists(names_config_path):
            os.remove(names_config_path)
        if os.path.exists(config_path):
            os.remove(config_path)
        messagebox.showinfo("Files deleted", "Camera and config files have been deleted.")

    delete_button = tk.Button(root, text="Reiniciar", font=("Arial", 12), bg="#577BB4", command=delete_files)
    delete_button.pack(side=tk.LEFT, anchor='s',padx=0,pady=25)
    
    """
    # Add a button for saving the configuration
    cancelar_button = tk.Button(frame, text="Cancelar", command=root.destroy,bg="#2E6EA6", fg="black", font=("Arial", 14))
    cancelar_button.pack(side=tk.LEFT, padx=100, pady=0)
    save_button = tk.Button(frame, text="Guardar", command=root,bg="#2E6EA6", fg="black", font=("Arial", 14))
    save_button.pack(side=tk.LEFT, padx=0, pady=0)
    """
    
    root.mainloop()

  
def open_config():
    def save_config():
        # Logic to save the selected camera configuration
        print("Configuracion Guardada")
        for i in range(3):
            if(combos_camera_config[i*2].current()==combos_camera_config[i*2+1].current()):
                print("Error: Las cámaras no pueden ser iguales")
                messagebox.showerror(message="Las cámaras de un mismo piso deben ser distintas", title="Error en la selección de cámaras")
                return
        with open(config_path, 'w') as file:
            for i in range(3):
                for j in range(2):
                    camerasLevel[i][j] = combos_camera_config[i*2+j].current()
                    file.write(f"{camerasLevel[i][j]} ")
                file.write("\n")
        config_window.destroy()
        update_cameras(nivel_actual, '', tk.Label())

    config_window = tk.Toplevel(root)
    config_window.title(" ")
    #config_window.overrideredirect(True)
    config_window.resizable(0,0)
    
    config_window.grab_set()
    combos_camera_config = []

    #  Obtenemos el largo y  ancho de la pantalla
    wtotal = config_window.winfo_screenwidth()
    htotal = config_window.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 370
    hventana = 200

    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)

    #  Se lo aplicamos a la geometría de la ventana
    config_window.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    
    LetterSize=13
    BLS=10
    label = tk.Label(config_window, text="Configuracion ", font=("Arial", LetterSize),fg="#004A8C",bg="#F2F2F2")
    label.pack( pady=0)

    # Create a grid layout with 3 rows and 3 columns
    for i in range(3):
        row_frame = tk.Frame(config_window)
        row_frame.pack(fill=tk.X)
        level = tk.Label(row_frame, text=f"Nivel {i+1}",font=("Arial", BLS))
        level.pack(side=tk.LEFT, padx=5, pady=10)
        for j in range(2):
            combos_camera_config.append(ttk.Combobox(row_frame, state="readonly", values=camerasName[0:len(cameras_list)]))
            combos_camera_config[-1].current(camerasLevel[i][j])
            combos_camera_config[-1].pack(side=tk.LEFT, padx=5, pady=10)

    # Add a button for saving the configuration
    cancelar_button = tk.Button(config_window, text="Cancelar", command=config_window.destroy,bg="#577BB4", fg="black", font=("Arial", BLS))
    cancelar_button.pack(side=tk.LEFT, padx=100, pady=0)
    save_button = tk.Button(config_window, text="Guardar", command=save_config,bg="#577BB4", fg="black", font=("Arial", BLS))
    save_button.pack(side=tk.LEFT, padx=0, pady=0)
    #config_window.attributes('-zoomed', 1)
    #config_window.attributes('-fullscreen', 1)
    

def update_cameras(index, button_text,label):
    """Actualiza los frames de video con las nuevas cámaras."""
    global camera1, camera2, camera_frame1, camera_frame2, nivel_actual

    nivel_actual=index
    camera1.release()
    camera2.release()

    #camera1 = cv2.VideoCapture(cameras_list[index])
    #camera2 = cv2.VideoCapture(cameras_list[(index+1) % len(cameras_list)])

    camera1 = cv2.VideoCapture(cameras_list[camerasLevel[index][0]])
    camera2 = cv2.VideoCapture(cameras_list[camerasLevel[index][1]])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)
    
    label.config(text=f"Nivel {index+1}")

    # Actualizar el frame principal
    root.update()

def update_video(cap, canvas):
    # Continuar leyendo frames mientras la ventana esté abierta
    if root.winfo_exists():
        ret, frame = cap.read()
        if ret:
            # Cambiar tamaño del frame para que encaje en el canvas
            width, height = canvas.winfo_width(), canvas.winfo_height()
            frame = cv2.resize(frame, (width, height))

            # Convertir el frame a RGB y crear un PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = Pil_imageTk.PhotoImage(Pil_image.fromarray(frame))

            # Actualizar el canvas con la nueva imagen
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo  

        # Programar la próxima actualización después de un corto retraso
        root.after(50, update_video, cap, canvas)

def report():
    print("Presionaste el boton de reportes")
    videoCams = [camera1, camera2]
    folderName = datetime.now().strftime("%d-%m-%Y %H.%M")
    reportFolder = "Reporte webcams"
    folderPath = Path(f"{reportFolder}/{folderName} Nivel {nivel_actual+1}")
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    for i in range(2):
        take_pic(videoCams[i], f"{folderPath}/screenShotCamera{i}.png")

def take_pic(camera, path):
    ret, frame = camera.read()
    rgb_frame = frame[:, :, ::-1]
    img = Pil_image.fromarray(rgb_frame)
    img.save(path)
    print("Photo captured successfully.")



def main():
    global root, camera1, camera2, camera_frame1, camera_frame2
    
    root = tk.Tk()
    #root.overrideredirect(True)
    #root.resizable(False,False)
    root.minsize(1000, 600)
    bg_photo=PhotoImage(file=resource_path('Datos/bg.png'))
   
    root.geometry('1000x600')
    root.title("Webcam viewer")
    icono_chico = tk.PhotoImage(file="Datos/16.png")
    icono_grande = tk.PhotoImage(file="Datos/32.png")
    root.iconphoto(False, icono_grande, icono_chico)    

    root.iconphoto(True, icono_chico)
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    wventana = 1000#1000
    hventana = 600#600
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    icono = tk.PhotoImage(file=resource_path("Datos/icono.png"))
    root.config(bg='white')
    #root.iconphoto(True,icono)

    def on_window_config(event: tk.Event) -> None:
        """Actualizar tamaño de los frames de video y botones al cambiar el tamaño de la ventana."""
        width, height = root.winfo_width()-60, root.winfo_height()-60
        video_width, video_height = width // 2, height*7 // 9
        camera_frame1.config(width=video_width, height=video_height)
        camera_frame2.config(width=video_width, height=video_height)
        """
        level_buttons_frame_width = tk.PhotoImage(width=1, height=1)
        level_buttons_frame_height = height // 3
        level_buttons_frame.config(width=level_buttons_frame_width.width(), height=level_buttons_frame_height)

        button_width = video_width // 3
        button_height = level_buttons_frame_height // 3
        for i, button in enumerate(level_buttons_frame.winfo_children()[:3]):
            button.place(x=i*button_width + 10*i, y=0, width=button_width, height=button_height)

        print(width, video_width, button_width)
        config_button.place(x=button_width*5+20, width=button_width, height=button_height)
       """
        
        LS1=root.winfo_width()*root.winfo_height()//25000#24
        LS2=root.winfo_width()*root.winfo_height()//42857#14
        TS=min(60,LS1)
        BS=min(35,LS2)

        label.config(font=("Arial",TS ))
        
        button_config.config(font=("Arial",BS ))
        button_reports.config(font=("Arial",BS ))

        for button in niveles_botones:    
            button.config(font=("Arial",BS ))

        
       
        #print(LS1,LS2,TS,BS)
        
    root.bind("<Configure>", on_window_config)

    # Crear un frame principal
    frame = tk.Frame(root)
    frame.configure(background="#FFFFFF")
    frame.pack(padx=20, pady=20)

    # Agregar un label al frame
    label = tk.Label(frame, text="Nivel "+ str(nivel_actual+1), font=("Arial",24 ),fg="#2E6EA6",bg="#FFFFFF")
    label.pack( pady=0)

    # Definir acciones para cada botón
    
    button_actions = [lambda index=i, text=f"Nivel {i+1}": update_cameras(index, text, label) for i in range(3)]
    niveles_botones=[]

    # Agregar botones al frame
    buttons_frame = tk.Frame(root)
    buttons_frame.configure(background="#ffffff")
    buttons_frame.pack(side=tk.TOP, pady=0)

    button_reports = tk.Button(buttons_frame, text="Módulo de Reportes", command=report, bg="#577BB4", fg="black", font=("Arial", 14))
    button_reports.pack(side=tk.LEFT, padx=20)

    button_reports2 = tk.Label(buttons_frame ,text="         ",bg="#ffffff", font=("Helvetica", 24))
    button_reports2.pack(side=tk.LEFT, padx=0)

    for i, action in enumerate(button_actions):
        button = tk.Button(buttons_frame, text=f"Nivel {i+1}", command=action, bg="#577BB4", fg="black", font=("Arial", 14))
        niveles_botones.append(button)
        button.pack(side=tk.LEFT, padx=20)

    # Crear botones adicionales
    button_config = tk.Button(buttons_frame, text="Configuración", command=open_config, bg="#2E6EA6", fg="black", font=("Helvetica", 14))
    button_config.pack(side=tk.RIGHT, padx=20)
    button_reports2 = tk.Label(buttons_frame ,text="          ",bg="#ffffff", font=("Helvetica", 24))
    button_reports2.pack(side=tk.RIGHT, padx=20)

    # Crear frames internos para los videos
    camera_frame1 = tk.Canvas(frame, width=300, height=300, bg="white")
    camera_frame1.pack(side=tk.LEFT, padx=(0, 10), pady=13)

    camera_frame2 = tk.Canvas(frame, width=300, height=300, bg="white")
    camera_frame2.pack(side=tk.LEFT, padx=(10, 0), pady=13)

    camera1 = cv2.VideoCapture(cameras_list[camerasLevel[0][0]])
    camera2 = cv2.VideoCapture(cameras_list[camerasLevel[0][1]])

    update_video(camera1, camera_frame1)
    update_video(camera2, camera_frame2)

    root.mainloop()


def list_cameras():
    devices = FilterGraph().get_input_devices()
    print(devices)
    name = 0
    cameras = []
    for i in range(cv2.CAP_DSHOW, cv2.CAP_DSHOW + 10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(devices[name])
            camerasName[name], name = devices[name], name + 1
            cameras.append(i)
            cap.release()
    return cameras

def set_cameras_names():
    if not names_config_path.is_file(): return
    with open(names_config_path, 'w') as file:
        for i in range(6):
            temp = camerasName[i].split('\n')[0]
            file.write(f"{temp}")
            file.write("\n")

def load_cameras_names():
    if not names_config_path.is_file():
        with open(names_config_path, 'w') as file:
            for i in range(6):
                file.write(f"{camerasName[i]}")
                file.write("\n")
    with open(names_config_path, 'r') as file:
        for i in range(6):
            camerasName[i] = file.readline()

def load_cameras_config():
    if not config_path.is_file(): return
    with open(config_path, 'r') as file:
        for i in range(3):
            level_config = file.readline().split(' ')
            if int(level_config[0]) == int(level_config[1]):
                messagebox.showwarning(message="Hubo un error en la carga de la configuración", title="Error cargando ")
                return
            camerasLevel[i] = [int(level_config[0]), int(level_config[1])]


cameras_list = list_cameras()
maxCameras = 0
for i in range(3):
    camerasLevel[i][0] = maxCameras % len(cameras_list)
    camerasLevel[i][1] = (maxCameras + 1) % len(cameras_list)
    maxCameras += 2

if not cameras_list:
    print("No se encontraron cámaras.")
load_cameras_config()
load_cameras_names()
inicio()
