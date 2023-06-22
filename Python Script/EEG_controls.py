import socket
from pylsl import StreamInlet, resolve_stream
import tkinter as tk
import threading

class GUI:

    def __init__(self):
        self.inlet = None
        self.max_strength = 0 
        self.root = tk.Tk()
        
        self.root.geometry("500x300")
        self.root.title("2D EMG Game Acquisition")

        self.label = tk.Label(self.root,text = "Console :")
        self.label.pack(padx=20,pady=10)

        self.console = tk.Text(self.root,height=6)
        self.console.pack(padx=20,pady=10)

        self.buttonFindStream = tk.Button(self.root,text="Find Stream",command=threading.Thread(target=self.open_stream).start)
        self.buttonFindStream.pack(padx=20,pady=10)

        self.buttonTest = tk.Button(self.root, text="Test", command=threading.Thread(target=self.test).start)
        self.buttonTest.pack(padx=20,pady=10)

        self.buttonStart = tk.Button(self.root, text="Start Server", command = threading.Thread(target = self.start_server).start)
        self.buttonStart.pack(padx=20,pady=10)

        self.root.mainloop()

    def recv_data(self):
        sample,timestamp = self.inlet.pull_sample()
        return sample[0:4]

    def traitement_data(self):
        last_sample = self.recv_data()
        return last_sample
    
    def test(self):
        #self.console.delete(1.0,tk.END)
        while True:
            buffer = []
            for i in range(100):
                sample = self.traitement_data()
                if abs(sample[1]) > abs(sample[2])*6:
                    print("Right : ",sample)
                    buffer.append(1)
                elif abs(sample[2]) > abs(sample[1])*8:
                    print("Left : ",sample)
                    buffer.append(-1)
                else:
                    buffer.append(0)

            buffer_sum = 0
            for i in buffer:
                buffer_sum = buffer_sum + buffer[i]
            
            if buffer_sum >= -50 and buffer_sum <= 50:
                #message_console="no val \n"
                message = 0
            if buffer_sum > 50:
                #message_console = "left "+str(sample[1])+"\n"
                message = 1
            if buffer_sum < -50:
                #message_console = "right "+str(sample[2])+" "+str(sample[1])+"\n"
                message = 2

            #self.console.insert(tk.END,message_console)
            #self.console.see(tk.END)

            return message

    def start_server(self):
        self.console.delete(1.0,tk.END)
        # Créer un socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Attacher le socket à une adresse et un port spécifiques
        server_socket.bind(('localhost', 12345))
        
        # Commencer à écouter pour les connexions entrantes
        server_socket.listen(1)
        self.console.insert(tk.END,"Server started and listening on localhost:12345 \n")

        while True:
            # Accepter une connexion entrante
            client_socket, addr = server_socket.accept()
            self.console.insert(tk.END,f"Connection from {addr} has been established! \n")

            while True:

                try:
                    # Envoyer un message au client
                    message = str(self.test())
                    client_socket.send(bytes(message+",", "utf-8"))
                    self.console.insert(tk.END,message+"\n")
                except:
                    self.console.insert(tk.END,"Client has disconnected \n")
                    break  # sortir de la boucle interne si le client est déconnecté

            # Fermer le socket client
            client_socket.close()

    def open_stream(self):
        self.console.delete(1.0,tk.END)
        self.console.insert(tk.END,"Looking for Stream ...")
        os_stream = resolve_stream("type","EEG")
        self.inlet = StreamInlet(os_stream[0])
        self.console.insert(tk.END,"Stream found !")

if __name__ == "__main__":
    GUI()

"""
Version 1: Flow continu 
def test(self):
        self.console.delete(1.0,tk.END)
        while True:
            sample = self.traitement_data()
            message="no val \n"
            #self.console.insert(tk.END,str(abs(sample[1]))+" "+str(abs(sample[2]))+"\n")
            if abs(sample[1]) > abs(sample[2])*6:
                message = "left "+str(sample[1])+"\n"
            if abs(sample[2]) > abs(sample[1])*8:
                message = "right "+str(sample[2])+" "+str(sample[1])+"\n"      
                
            self.console.insert(tk.END,message)
            self.console.see(tk.END)
"""

"""
Version 2: Flow par chunk pour améliorer la précision
def test(self):
        self.console.delete(1.0,tk.END)
        while True:
            buffer = []
            for i in range(100):
                sample = self.traitement_data()
                if abs(sample[1]) > abs(sample[2])*6:
                    buffer.append(1)
                elif abs(sample[2]) > abs(sample[1])*8:
                    buffer.append(-1)
                else:
                    buffer.append(0)

            buffer_sum = 0
            for i in buffer:
                buffer_sum = buffer_sum + buffer[i]
            
            if buffer_sum >= -50 and buffer_sum <= 50:
                message="no val \n"
            if buffer_sum > 50:
                message = "left "+str(sample[1])+"\n"
            if buffer_sum < -40:
                message = "right "+str(sample[2])+" "+str(sample[1])+"\n"
                
            self.console.insert(tk.END,message)
            self.console.see(tk.END)
"""