import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class GUIManager:
    def __init__(self, container_manager):
        self.cm = container_manager
        self.window = tk.Tk()
        self.bg_color = "white"
        self.status_labels = []

    def get_selected_image(self):
        global value
        value = self.select.get()
        return value

    def configure(self):
        self.window.title("Docker Container Manager")
        self.window.configure(background=self.bg_color)
        
        self.select = ttk.Combobox(self.window, state="readonly")  # aggiungere nomi di container qua
        self.select['values'] = [
            "nginx:latest",
            "httpd:latest",             
            ]
        
        self.select.set("nginx:latest")
        self.select.grid(row=2, column=0, padx=10, pady=10)


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

