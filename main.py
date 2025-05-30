import docker
import tkinter as tk
from tkinter import messagebox
import threading

class ContainerManager:
    def __init__(self, port):
        self.client = docker.from_env()
        self.gui_manager = None
        self.port = port

        self.lock = threading.Lock()
        self.container_list = []
        self.started_containers = 0

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager
    
    def create_container(self, name, port):
        return self.client.containers.run(
            'nginx:latest',
            name=name,
            ports={'80/tcp': port},
            detach=True
        )

    def append_container(self, container):
        self.container_list.append(container)

    def stop_container(self, container):
        container.stop()

    def delete_container(self, container):
        container.stop()
        container.remove()

    def start_containers(self, label, amount):
        try:
            amount = int(amount)
        except ValueError:
            label.config(text="Invalid input, insert an integer!", fg="red")
            return
        
        with self.lock:
            for i in range(amount):
                unique_index = self.started_containers + i
                port = self.port + unique_index
                cont = self.create_container(f"cont_{unique_index}", port)
                self.append_container(cont)

            self.started_containers += amount
            label.config(text=f"Started {amount} containers successfully!", fg="green")

    def stop_containers(self, label):
        if len(self.container_list) == 0:
            label.config(text="No containers to stop!!", fg="black")
            return
        
        with self.lock:
            for i in range(len(self.container_list)):
                container = self.container_list[0]
                container.stop()
                container.remove()
                self.gui_manager.remove_label(container)
                self.container_list.remove(container)

            label.config(text="All containers stopped and removed!", fg="green")


class GUI_Manager:
    def __init__(self, container_manager):
        self.cm = container_manager
        self.window = tk.Tk()
        self.bg_color = "white"
        self.status_labels = []

    def configure(self):
        self.window.title("Docker Container Manager")
        self.window.configure(background=self.bg_color)

        label1 = tk.Label(self.window, text="Inserisci il numero di container:", fg="black", bg=self.bg_color, font=("Verdana", 16))
        label1.grid(row=0, column=0)

        info_label = tk.Label(self.window, text="", bg=self.bg_color, fg="black", font=("Verdana", 10))
        info_label.grid(row=2, column=0)

        amount_input = tk.Entry()
        amount_input.grid(row=1, column=0, pady=10)

        def start_containers_thread():
            if not self.cm.lock.locked():
                if messagebox.askyesno(title="Warning", message=f"Are you sure you want to start {amount_input.get()} containers?", icon="warning"):
                    info_label.config(text="Starting containers...", fg="black")
                    threading.Thread(target=lambda: self.handle_start(info_label, amount_input.get()), daemon=True).start()
                else:
                    pass
            else:
                info_label.config(text="Another thread is running, please wait!", fg="red")
            
        start_button = tk.Button(text="Start containers", command=start_containers_thread)
        start_button.grid(row=4, column=0)

        def stop_containers_thread():
            if not self.cm.lock.locked():
                info_label.config(text=f"Stopping {len(self.cm.container_list)} containers...", fg="black")
                threading.Thread(target=lambda: self.cm.stop_containers(info_label), daemon=True).start()
            else:
                info_label.config(text="Another thread is running, please wait!", fg="red")

        stop_button = tk.Button(text="Stop and remove all containers", command=stop_containers_thread)
        stop_button.grid(row=5, column=0)

        self.update_container_info()

    def handle_start(self, label, amount):
        self.cm.start_containers(label, amount)
        
        for container in self.cm.container_list[len(self.status_labels):]:
            idx = len(self.status_labels)

            name = f"{container.name} ({container.id[:12]})"
            port = container.attrs['HostConfig']['PortBindings']['80/tcp'][0]['HostPort']

            name_label = tk.Label(self.window, text=name, bg=self.bg_color, font=("Verdana", 12))
            name_label.grid(row=idx, column=1, padx=10)

            port_label = tk.Label(self.window, text=f"Porta: {port}", bg=self.bg_color, font=("Verdana", 12))
            port_label.grid(row=idx, column=2, padx=10)

            status_label = tk.Label(self.window, text="Stato: ?", bg=self.bg_color, font=("Verdana", 12))
            status_label.grid(row=idx, column=3, padx=10)

            self.status_labels.append((container, name_label, port_label, status_label))

    def update_container_info(self):
        for container, _name, _port, status_label in self.status_labels:
            try:
                container.reload()
                status_label.config(text=f"Stato: {container.status}")
            except:
                self.cm.container_list.remove(container)
                self.remove_label(container)
        
        self.window.after(2000, self.update_container_info)

    def remove_label(self, cont):
        for c, name_label, port_label, status_label in self.status_labels:
            if c == cont:
                name_label.destroy()
                port_label.destroy()
                status_label.destroy()
                self.status_labels.remove((c, name_label, port_label, status_label))
                break


cm = ContainerManager(6000)
gui = GUI_Manager(cm)
cm.set_gui_manager(gui)

gui.configure()

if __name__ == "__main__":
    gui.window.mainloop()
