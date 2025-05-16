import random
import docker
import tkinter as tk
import threading

class ContainerManager:
    def __init__(self, port):
        self.port = port
        self.gui_manager = None
        self.client = docker.from_env()

        self.container_list = []
        self.started_containers = 0

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager
    
    """Crea un container detached che espone la porta 80 internamente"""
    def create_container(self, name, port):
        return self.client.containers.run(
            'nginx:latest',
            name=name,
            ports={'80/tcp': port},
            detach=True, # per fare ritornare il container
        )

    """Aggiunge il container alla lista containers"""
    def append_container(self, container):
        self.container_list.append(container)

    def stop_container(self, container):
        container.stop()

    def delete_container(self, container):
        container.stop()
        container.remove()

    """Avvia amount container e li aggiunge all'array dei container"""
    def start_containers(self, label, amount):
        try:
            amount = int(amount)
        except ValueError:
            label.config(text = "Invalid input, insert an integer!", fg = "red")
            return
        
        for i in range(amount):
            unique_index = self.started_containers + i

            port = self.port + unique_index
            cont = self.create_container(f"cont_{unique_index}", port)
            self.append_container(cont)

        self.started_containers += amount

        label.config(text = f"Started {amount} containers successfully!", fg = "green")
    
    """Stoppa e rimuove tutti i container nella lista containers"""
    def stop_containers(self, label):
        if len(self.container_list) == 0:
            label.config(text = "No containers to stop!!", fg = "black")
            return
        
        for i in range(len(self.container_list)):
            container = self.container_list[0] # perche ogni volta scalano
            
            container.stop()
            container.remove()
            self.container_list.remove(container)

        label.config(text = f"All containers stopped and removed!", fg = "green")


class GUI_Manager:
    def __init__(self, container_manager):
        self.cm = container_manager
        self.window = tk.Tk()
        self.bg_color = "white"

    def configure(self):
        #self.window.geometry("1500x600")
        #self.window.resizable(False, False)
        self.window.title("Docker Container Manager")
        self.window.configure(background=self.bg_color)

        label1 = tk.Label(self.window, text="Inserisci il numero di container:", fg="black", bg=self.bg_color, font=("Verdana", 16))
        label1.grid(row=0, column=0)

        info_label = tk.Label(self.window, text="", bg=self.bg_color ,fg="black", font=("Verdana", 10))
        info_label.grid(row=2, column=0)

        amount_input = tk.Entry()
        amount_input.grid(row=1, column=0, pady=10)

        def start_containers_thread():
            threading.Thread(target=lambda: self.cm.start_containers(info_label, amount_input.get()), daemon=True).start()
            
        start_button = tk.Button(text="Start containers", command=start_containers_thread)
        start_button.grid(row=4, column=0)

        def stop_containers_thread():
            threading.Thread(target=lambda: self.cm.stop_containers(info_label), daemon=True).start()

        start_button = tk.Button(text="Stop and remove all containers", command=stop_containers_thread)
        start_button.grid(row=5, column=0)

cm = ContainerManager(6000)
gui = GUI_Manager(cm)
cm.set_gui_manager(gui)

gui.configure()

if __name__ == "__main__":
    gui.window.mainloop()