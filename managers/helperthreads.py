import json
import threading
from tkinter import messagebox

class HelperThreads:
    def __init__(self, container_manager):
        self.container_manager = container_manager

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager

    def set_info_label(self, info_label):
        self.info_label = info_label

    def start_all_containers_thread(self, amount_input):
        """
        Avvia tutti i container in un thread separato, mostrando una conferma all'utente.
        Aggiorna la label di stato in base all'esito.
        """
        if not self.container_manager.lock.locked():
            with self.container_manager.lock:
                if messagebox.askyesno(title="Warning", message=f"Are you sure you want to start {amount_input.get()} containers?", icon="warning"):
                    self.info_label.config(text="Starting containers...", fg="black")
                    threading.Thread(target=self.gui_manager.handle_start, args=(self.info_label, amount_input.get()), daemon=True).start()
        else:
            self.info_label.config(text="Another thread is running, please wait!", fg="red")

    def stop_all_containers_thread(self):
        """
        Ferma e rimuove tutti i container in un thread separato.
        Aggiorna la label di stato in base all'esito.
        """
        if not self.container_manager.lock.locked():
            with self.container_manager.lock:
                self.info_label.config(text=f"Stopping {len(self.container_manager.container_list)} containers...", fg="black")
                threading.Thread(target=self.container_manager.stop_all_containers, args=(self.info_label,), daemon=True).start()
        else:
            self.info_label.config(text="Another thread is running, please wait!", fg="red")

    def stop_container_thread(self, container):
        """
        Ferma un singolo container in modo thread-safe.
        Aggiorna la label di stato in base all'esito.
        """
        with self.container_manager.lock:
            self.info_label.config(text="Stopping container...", fg="black")
            try:
                self.container_manager.stop_container(container)
                self.info_label.config(text="Container stopped successfully!", fg="green")
            except Exception as e:
                self.info_label.config(text=f"Error: {e}", fg="red")

    def start_container_thread(self, container):
        """
        Avvia un singolo container in modo thread-safe.
        Aggiorna la label di stato in base all'esito.
        """
        with self.container_manager.lock:
            self.info_label.config(text="Starting container...", fg="black")
            try:
                self.container_manager.start_container(container)
                self.info_label.config(text="Container started successfully!", fg="green")
            except Exception as e:
                self.info_label.config(text=f"Error: {e}", fg="red")

    def remove_container_thread(self, container):
        """
        Rimuove un singolo container in modo thread-safe.
        Aggiorna la label di stato in base all'esito.
        """
        with self.container_manager.lock:
            self.info_label.config(text="Removing container...", fg="black")
            try:
                self.container_manager.remove_container(container)
                self.info_label.config(text="Container removed successfully!", fg="green")
            except Exception as e:
                self.info_label.config(text=f"Error: {e}", fg="red")

    def update_container_data(self, container, signal_type_label, data_label):
        """
        Legge i dati di output dal container in tempo reale e aggiorna le label della GUI.
        Gestisce eventuali errori di decodifica JSON.
        """
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