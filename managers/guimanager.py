import json
import threading
import tkinter as tk
from tkinter import messagebox

class GUIManager:
    """
    Gestisce l'interfaccia grafica per il controllo dei container Docker.
    Permette di avviare, fermare e monitorare lo stato dei container tramite una GUI Tkinter.
    """
    def __init__(self, container_manager):
        """
        Inizializza il gestore GUI.

        Args:
            container_manager: Istanza del gestore dei container Docker.
        """
        self.cm = container_manager
        self.window = tk.Tk()
        self.bg_color = "white"
        self.status_labels = []

    def configure(self):
        """
        Configura la finestra principale e i widget dell'interfaccia grafica.
        """
        self.window.title("Docker Container Manager")
        self.window.configure(background=self.bg_color)

        label1 = tk.Label(self.window, text="Inserisci il numero di container:", fg="black", bg=self.bg_color, font=("Verdana", 16))
        label1.grid(row=0, column=0)

        info_label = tk.Label(self.window, text="", bg=self.bg_color, fg="black", font=("Verdana", 10))
        info_label.grid(row=2, column=0)

        amount_input = tk.Entry()
        amount_input.grid(row=1, column=0, pady=10)

        def start_containers_thread():
            """
            Avvia i container in un thread separato per non bloccare la GUI.
            """
            # Acquisisce direttamente il lock nella sezione critica
            if not self.cm.lock.locked():
                with self.cm.lock:
                    if messagebox.askyesno(title="Warning", message=f"Are you sure you want to start {amount_input.get()} containers?", icon="warning"):
                        info_label.config(text="Starting containers...", fg="black")
                        threading.Thread(target=self.handle_start, args=(info_label, amount_input.get()), daemon=True).start()
            else:
                info_label.config(text="Another thread is running, please wait!", fg="red")
            
        start_button = tk.Button(text="Start containers", command=start_containers_thread)
        start_button.grid(row=4, column=0)

        def stop_containers_thread():
            """
            Ferma e rimuove tutti i container in un thread separato.
            """
            if not self.cm.lock.locked():
                with self.cm.lock:
                    info_label.config(text=f"Stopping {len(self.cm.container_list)} containers...", fg="black")
                    threading.Thread(target=self.cm.stop_containers, args=(info_label,), daemon=True).start()
            else:
                info_label.config(text="Another thread is running, please wait!", fg="red")

        stop_button = tk.Button(text="Stop and remove all containers", command=stop_containers_thread)
        stop_button.grid(row=5, column=0)

    def handle_start(self, info_label, amount):
        """
        Avvia i container e aggiorna la GUI con le nuove informazioni.

        Args:
            label: Label di stato da aggiornare.
            amount: Numero di container da avviare.
        """
        self.cm.start_containers(info_label, amount)
        
        for container in self.cm.container_list[len(self.status_labels):]:
            idx = len(self.status_labels)

            name = f"{container.name} ({container.id[:12]})"
            port = container.attrs['HostConfig']['PortBindings']['80/tcp'][0]['HostPort']

            name_label = tk.Label(self.window, text=name, bg=self.bg_color, font=("Verdana", 12))
            name_label.grid(row=idx, column=1, padx=10, pady=10)

            port_label = tk.Label(self.window, text=f"Porta: {port}", bg=self.bg_color, font=("Verdana", 12))
            port_label.grid(row=idx, column=2, padx=10, pady=10)

            status_label = tk.Label(self.window, text="Stato: ?", bg=self.bg_color, font=("Verdana", 12))
            status_label.grid(row=idx, column=3, padx=10, pady=10)

            # Pulsante Stop
            def stop_container_thread(c=container):
                with self.cm.lock:
                    info_label.config(text="Stopping container...", fg="black")
                    try:
                        self.cm.stop_container(c)
                        info_label.config(text="Container stopped successfully!", fg="green")
                    except Exception as e:
                        info_label.config(text=f"Error: {e}", fg="red")
            stop_button = tk.Button(
                text="Stop",
                command=lambda c=container: threading.Thread(target=stop_container_thread, args=(c,), daemon=True).start()
            )
            stop_button.grid(row=idx, column=4, padx=10, pady=10)

            # Pulsante Start
            def start_container_thread(c=container):
                with self.cm.lock:
                    info_label.config(text="Starting container...", fg="black")
                    try:
                        self.cm.start_container(c)
                        info_label.config(text="Container started successfully!", fg="green")
                    except Exception as e:
                        info_label.config(text=f"Error: {e}", fg="red")

            start_button = tk.Button(
                text="Start",
                command=lambda c=container: threading.Thread(target=start_container_thread, args=(c,), daemon=True).start()
            )
            start_button.grid(row=idx, column=5, padx=10, pady=10)

            # Pulsante Remove
            def remove_container_thread(c=container):
                with self.cm.lock:
                    info_label.config(text="Removing container...", fg="black")
                    try:
                        self.cm.remove_container(c)
                        info_label.config(text="Container removed successfully!", fg="green")
                    except Exception as e:
                        info_label.config(text=f"Error: {e}", fg="red")
            remove_button = tk.Button(
                text="Remove",
                command=lambda c=container: threading.Thread(target=remove_container_thread, args=(c,), daemon=True).start()
            )
            remove_button.grid(row=idx, column=6, padx=10, pady=10)

            signal_type_label = tk.Label(self.window, text="Tipo: ?", bg=self.bg_color, font=("Verdana", 12))
            signal_type_label.grid(row=idx, column=7, padx=10, pady=10)

            data_label = tk.Label(self.window, text="Data: ?", bg=self.bg_color, font=("Verdana", 12))
            data_label.grid(row=idx, column=8, padx=10, pady=10)

            threading.Thread(target=self.update_containers_status, daemon=True).start()
            threading.Thread(target=self.update_container_data, args=(container, signal_type_label, data_label), daemon=True).start()

            self.status_labels.append((container, name_label, port_label, status_label, stop_button, start_button, remove_button, signal_type_label, data_label))

    def update_container_data(self, container, signal_type_label, data_label):
        # Leggo l'output dal container
        for line in container.logs(stream=True, follow=True):
            msg = line.decode("utf-8").strip()
            try:
                data = json.loads(msg)
                print(f"[{container.name}] {data['index']} -> {data['value']}")
                signal_type_label.config(text=f"Tipo: {data['signal']}")
                data_label.config(text=f"Data: {data['value']}")
            except json.JSONDecodeError:
                print("JSONDecodeError")
                pass

    def update_containers_status(self):
        """
        Aggiorna periodicamente lo stato dei container nella GUI.
        Rimuove dalla GUI i container che non esistono più.
        """
        for container, _, _, status_label, _, _, _, _, _ in self.status_labels:
            try:
                container.reload()
                status_label.config(text=f"Stato: {container.status}")
            except:
                self.cm.container_list.remove(container)
                self.remove_label(container)
        
        self.window.after(100, self.update_containers_status)

    def remove_label(self, cont):
        """
        Rimuove le label associate a un container dalla GUI.

        Args:
            cont: Il container di cui rimuovere le label.
        """
        for c, name_label, port_label, status_label, stop_button, start_button, remove_button, signal_type_label, data_label in self.status_labels:
            if c == cont:
                name_label.destroy()
                port_label.destroy()
                status_label.destroy()
                stop_button.destroy()
                start_button.destroy()
                remove_button.destroy()
                signal_type_label.destroy()
                data_label.destroy()
                self.status_labels.remove(
                    (c, name_label, port_label, status_label, stop_button, start_button, remove_button, signal_type_label, data_label)
                )
                break

