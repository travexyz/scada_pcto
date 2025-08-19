import docker, threading

class ContainerManager:
    """
    Gestisce la creazione, l'avvio, l'arresto e la rimozione dei container Docker.
    Permette l'integrazione con una GUI e la configurazione tramite file di configurazione.
    """
    def __init__(self, port, config):
        """
        Inizializza il ContainerManager.

        Args:
            port (int): Porta di base per l'esposizione dei container.
            config: Oggetto di configurazione per la lettura dei parametri.
        """
        self.client = docker.from_env()
        self.gui_manager = None
        self.port = port

        self.lock = threading.Lock()
        self.container_list = []
        self.started_containers = 0

        self.config = config

    def set_gui_manager(self, gui_manager):
        """
        Imposta il gestore della GUI.

        Args:
            gui_manager: Istanza del gestore GUI da associare.
        """
        self.gui_manager = gui_manager
    
    def create_container(self, name, port):
        """
        Crea e avvia un nuovo container Docker.

        Args:
            name (str): Nome del container.
            port (int): Porta da esporre.

        Returns:
            container: Istanza del container creato.
        """
        return self.client.containers.run(
            self.config.configreader['configuration']['container_image'],
            name=name,
            ports={'80/tcp': port},
            detach=True
        )

    def append_container(self, container):
        """
        Aggiunge un container alla lista dei container gestiti.

        Args:
            container: Istanza del container da aggiungere.
        """
        self.container_list.append(container)

    def start_container(self, container):
        """
        Avvia un container specifico.

        Args:
            container: Istanza del container da avviare.
        """
        container.start()

    def stop_container(self, container):
        """
        Ferma un container specifico.

        Args:
            container: Istanza del container da fermare.
        """
        container.stop()

    def remove_container(self, container):
        """
        Ferma e rimuove un container specifico.

        Args:
            container: Istanza del container da eliminare.
        """
        container.stop()
        container.remove()

    def start_containers(self, status_label, amount):
        """
        Avvia un certo numero di container e aggiorna la GUI.

        Args:
            label: Label della GUI da aggiornare con lo stato.
            amount: Numero di container da avviare (accettato come stringa, convertito a int).
        """
        try:
            amount = int(amount)
        except ValueError:
            status_label.config(text="Invalid input, insert an integer!", fg="red")
            return
        
        with self.lock:
            for i in range(amount):
                unique_index = self.started_containers + i
                port = self.port + unique_index
                cont = self.create_container(f"cont_{unique_index}", port)
                self.append_container(cont)

            self.started_containers += amount
            status_label.config(text=f"Started {amount} containers successfully!", fg="green")

    def stop_containers(self, label):
        """
        Ferma e rimuove tutti i container gestiti e aggiorna la GUI.

        Args:
            label: Label della GUI da aggiornare con lo stato.
        """
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
