import tkinter as tk
from botClima import chatbot

def enviar_mensaje():
    mensaje = entry_mensaje.get()
    if mensaje:
        text_chat.config(state=tk.NORMAL)
        text_chat.insert(tk.END, "Usuario: ", 'Usuario')
        text_chat.insert(tk.END, f"{mensaje}\n")
        chatbot(mensaje,text_chat)
        text_chat.config(state=tk.DISABLED)
        entry_mensaje.delete(0, tk.END)

# Crea la ventana principal y los widgets
ventana = tk.Tk()
ventana.title("Sky ChatBot")

frame_chat = tk.Frame(ventana)
frame_chat.pack()

text_chat = tk.Text(frame_chat, width=100, height=35, wrap="word")
text_chat.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(frame_chat, command=text_chat.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
text_chat.config(yscrollcommand=scrollbar.set)

text_chat.tag_config('Usuario', foreground='#3D9DDF')#,background='#DCF8C6'
text_chat.tag_config('Sky')#, background='#C2DFFF'

text_chat.config(state=tk.NORMAL)
text_chat.insert(tk.END, "Sky: ¡Hola! Soy tu asistente de clima. ¿En qué ciudad quieres saber el clima?:\n")
text_chat.config(state=tk.DISABLED)

entry_mensaje = tk.Entry(ventana, width=50)
entry_mensaje.pack()

boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack()


