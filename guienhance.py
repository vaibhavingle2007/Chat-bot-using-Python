from tkinter import *
from tkinter import ttk
import os
from hugchat import hugchat
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
# Get available voices
voices = engine.getProperty('voices')

# Change to Voice 1 (typically female, but may vary based on your system)
engine.setProperty('voice', voices[1].id)

# Adjust speech rate (default ~200, lower is slower, higher is faster)
engine.setProperty('rate', 160)

# Adjust volume (range: 0.0 to 1.0)
engine.setProperty('volume', 1.0)


# Initialize ChatBot once
chatbot = hugchat.ChatBot(cookie_path=r"cookies.json")
chatbot_id = chatbot.new_conversation()
chatbot.change_conversation(chatbot_id)

def chatBot(query):
    if not query.strip():
        return
    
    textarea.insert(END, "\nYou: " + query + "\n", "user")
    
    try:
        response = chatbot.chat(query.lower())
        textarea.insert(END, "\nBot: " + response + "\n", "bot")
        engine.say(response)
        engine.runAndWait()
    except Exception as e:
        response = "Sorry, I am having trouble responding."
        textarea.insert(END, "\nBot: " + response + "\n", "bot")
    
    questionField.delete(0, END)
    textarea.yview_moveto(1)  # Auto-scroll to the bottom
    return response

# GUI Setup
root = Tk()
root.geometry('500x600+100+30')
root.title('ChatBot - AI Assistant')
root.config(bg='#121212')

# Styling
FONT = ('Helvetica', 14)
BG_COLOR = "#1E1E1E"
TEXT_COLOR = "#EAEAEA"
BOT_COLOR = "#72d93f"
USER_COLOR = "#0A84FF"

# Logo
logoPic = PhotoImage(file='pic.png')
Label(root, image=logoPic, bg='#121212').pack(pady=5)

# Chat Frame
centerFrame = Frame(root, bg=BG_COLOR)
centerFrame.pack(padx=10, pady=5, fill=BOTH, expand=True)

scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(centerFrame, font=FONT, height=15, wrap='word', fg=TEXT_COLOR, bg=BG_COLOR,
                yscrollcommand=scrollbar.set, padx=10, pady=10, bd=0, relief=FLAT)
textarea.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=textarea.yview)

# Tagging Styles
textarea.tag_configure("user", foreground=USER_COLOR, font=("Helvetica", 14, "bold"))
textarea.tag_configure("bot", foreground=BOT_COLOR, font=("Helvetica", 14, "italic"))

# Input Field
questionField = Entry(root, font=FONT, bg="#2C2C2C", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                      bd=0, relief=FLAT, highlightthickness=2, highlightbackground="#555")
questionField.pack(pady=10, padx=20, fill=X, ipady=8)

# Ask Button
askPic = PhotoImage(file='ask.png')
askButton = Button(root, image=askPic, bg="#0078D4", activebackground="#005EA2",
                   relief=FLAT, bd=0, cursor="hand2", command=lambda: chatBot(questionField.get()))
askButton.pack(pady=5)

# Bind Enter Key
root.bind('<Return>', lambda event: askButton.invoke())

root.mainloop()
