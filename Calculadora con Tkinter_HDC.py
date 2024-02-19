import time  # Bibliotecas.
import tkinter as tk  
# Biblioteca para hacer uso de hilos en el programa.
from threading import Thread, Event  

# Guillén García Juan Andrés
# Calculadora basica la cual hace uso de hilos, demonios y concurrencia.

class Calculadora_B(tk.Tk):  
    def __init__(self):  # Método inicializador de la clase
        super().__init__()  
        self.title("Calculadora")  # Titulo del programa.
        self.geometry("225x290")  # Ajuste del tamaño de la ventana del programa.
        self.configure(bg="black") # Fondo negro.

        # Configuración de la entrada de texto y botones.
        self.entry = tk.Entry(self, width=34, bg="white", fg="black", bd=5)  # Cuadro de texto con fondo blanco y letras negras.
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5) 
        button_bg = "gray"  # Color de boton.
        button_fg = "white"  # Color del texto de los botones.

        buttons = [ 
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3), # Acomodo de los botones 
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), # de la calculadora.
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0, 4)  
        ]

        for button in buttons:
            if button[0] == "C": # Este apartado es unicamente para el boton "Clean".
                text, row, col, colspan = button
                btn = tk.Button(self, text=text, width=20, height=2, bg=button_bg, fg=button_fg, command=lambda t=text: self.Detector_B(t))
                btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5)
            else: # Todos los demas botones.
                text, row, col = button
                btn = tk.Button(self, text=text, width=5, height=2, bg=button_bg, fg=button_fg, command=lambda t=text: self.Detector_B(t))
                btn.grid(row=row, column=col, padx=5, pady=5)

        self.running = False  
        self.result = None  
        # Hilo para realizar el cálculo en segundo plano y evento que lo detiene.
        self.thread = None  
        self.stop_event = Event() 

    def Detector_B(self, text):  
        current_text = self.entry.get()  # Captura los valores.
        if text == '=':  
            if not self.running:  # Si no se está ejecutando ningún cálculo actualmente.
                self.thread = Thread(target=self.Resultado, args=(current_text,))  # Hace uso de un hilo para obtener el resultado.
                self.thread.daemon = True  # Convertimos el hilo a demonio.
                self.thread.start()  # Inicia el hilo.
        elif text == 'C':  
            self.entry.delete(0, tk.END)  # Borra todo en la pantalla.
        else:  
            self.entry.insert(tk.END, text)  # Se agrega el texto que indique el boton.

    def Resultado(self, text):
        self.running = True  
        time.sleep(5) # Aparenta que se tarda en ejecutar la operacion.
        try: # Validacion para que el programa no tenga fallas.
            result = eval(text)  # Evalúa la expresión matemática ingresada
            self.result = result  # Guarda el resultado.
        except Exception as e:
            self.result = "No se pudo realizar la operacion" # Muestra mensaje de error.
        self.running = False  
        self.A_Pantalla()  

    def A_Pantalla(self):  # Muestra el resultado en el cuadro de texto.
        if self.result is not None:  # Cuando el resultado es posible.
            self.entry.delete(0, tk.END)  # Borra todo el texto.
            self.entry.insert(tk.END, str(self.result))  # Inserta el resultado.

    def Cerrar_P(self):  # Método que se ejecuta cuando se cierra la ventana.
        self.stop_event.set()  # Evento que detiene el hilo.
        self.destroy()  # Destruye la ventana.

if __name__ == "__main__":  
    app = Calculadora_B()  # Inicia la ejecucucion del programa.
    app.protocol("WM_DELETE_WINDOW", app.Cerrar_P)
    app.mainloop() # Inicia un bucle en la interfaz.