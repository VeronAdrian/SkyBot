import tkinter as tk
from botClima import chatbot, fast_answer

def enviar_mensaje():
    message = entry_text.get()
    if message:
        text_chat.config(state=tk.NORMAL)
        text_chat.insert(tk.END, "Usuario: ", 'Usuario')
        text_chat.insert(tk.END, f"{message}\n")
        chatbot(message,text_chat)
        text_chat.config(state=tk.DISABLED)
        entry_text.delete(0, tk.END)
        
def get_text(entry):
    text = fast_answer(entry)
    return text

# Crea la ventana principal y los widgets
windows = tk.Tk()
windows.title("Sky ChatBot")

frame_chat = tk.Frame(windows)
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

entry_text = tk.Entry(windows, width=60)
entry_text.pack()

boton_enviar = tk.Button(windows, text="Enviar", command=enviar_mensaje,border=3,width=26)
boton_enviar.pack()


