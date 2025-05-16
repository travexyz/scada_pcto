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
            self.gui_manager.remove_container_labels(container)
            self.container_list.remove(container)

        label.config(text = f"All containers stopped and removed!", fg = "green")


class GUI_Manager:
    def __init__(self, container_manager):
        self.cm = container_manager
        self.window = tk.Tk()
        self.bg_color = "white"
        self.status_labels = []

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
            threading.Thread(target=lambda: self.handle_start(info_label, amount_input.get()), daemon=True).start()
            
        start_button = tk.Button(text="Start containers", command=start_containers_thread)
        start_button.grid(row=4, column=0)

        def stop_containers_thread():
            threading.Thread(target=lambda: self.cm.stop_containers(info_label), daemon=True).start()

        start_button = tk.Button(text="Stop and remove all containers", command=stop_containers_thread)
        start_button.grid(row=5, column=0)

        self.container_panel = tk.Frame(self.window, bg=self.bg_color)
        self.container_panel.grid(row=0, column=1, rowspan=20, padx=20, sticky="n")

        self.update_container_info()
       
    """Gestisce lo start dei docker per aggiornare lo stato"""
    def handle_start(self, label, amount):
        self.cm.start_containers(label, amount)
        
        for container in self.cm.container_list[len(self.status_labels):]:  # solo i nuovi
            idx = len(self.status_labels)  # usato per riga

            name = f"{container.name} ({container.id[:12]})"
            port = container.attrs['HostConfig']['PortBindings']['80/tcp'][0]['HostPort']

             # Crea le Label per nome, porta, stato
            name_label = tk.Label(self.window, text=name, bg=self.bg_color, font=("Verdana", 12))
            name_label.grid(row=idx, column=1, padx=10)

            port_label = tk.Label(self.window, text=f"Porta: {port}", bg=self.bg_color, font=("Verdana", 12))
            port_label.grid(row=idx, column=2, padx=10)

            status_label = tk.Label(self.window, text="Stato: ?", bg=self.bg_color, font=("Verdana", 12))
            status_label.grid(row=idx, column=3, padx=10)

            # Memorizza le Label per ogni container in un dizionario
            self.status_labels.append((container, name_label, port_label, status_label))

    """Aggiorna le info sui container ogni x millisecondi"""
    def update_container_info(self):
        for container, _name, _port, status_label in self.status_labels:
            try:
                container.reload()  # aggiorna stato dal daemon Docker
                status_label.config(text=f"Stato: {container.status}")
            except:
                self.cm.container_list.remove(container)
                self.status_labels.remove((container, _name, _port, status_label))

        threading.Thread(target=lambda: self.window.after(2000, self.update_container_info), daemon=True).start()

    def remove_label(self, cont, name_label, port_label, status_label):
        name_label.destroy()
        port_label.destroy()
        status_label.destroy()
        self.status_labels.remove((cont, name_label, port_label, status_label))  # Rimuovi dalla lista

    def remove_all_labels(self, container):
        # Rimuovi tutte le label associate a un container
        for cont, name_label, port_label, status_label in self.status_labels:
            if cont == container:
                name_label.destroy()
                port_label.destroy()
                status_label.destroy()
                self.status_labels.remove((cont, name_label, port_label, status_label))  # Rimuovi dalla lista
                break

cm = ContainerManager(6000)
gui = GUI_Manager(cm)
cm.set_gui_manager(gui)

gui.configure()

if __name__ == "__main__":
    gui.window.mainloop()