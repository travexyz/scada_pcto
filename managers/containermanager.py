import docker, threading

class ContainerManager:
    """_summary_
    """
    def __init__(self, port, config):
        self.client = docker.from_env()
        self.gui_manager = None
        self.port = port

        self.lock = threading.Lock()
        self.container_list = []
        self.started_containers = 0

        self.config = config
        self.config.configure()
        self.config.readconfig('config.ini')

    def set_gui_manager(self, gui_manager):
        """_summary_

        Args:
            gui_manager (_type_): _description_
        """
        self.gui_manager = gui_manager
    
    def create_container(self, name, port):
        return self.client.containers.run(
            self.config.configreader['configuration']['container_image'],
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
