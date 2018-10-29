from typing import Dict, Set, List

from docker_man.command import Command
from docker_man.configurator import Configurator
from docker_man.container import Container
from docker_man.watcher import Watcher


class Engine(object):
    def __init__(self, args) -> None:
        self.args = args
        self.configurator = Configurator()
        self.watcher = None
        self.containers: Dict[str, Container] = dict()
        self._active_containers: Set[Container] = set()

    def run(self):

        if self.args.configure is not None:
            self.configurator.parse(self.args.configure)
            print('Configured')
            return

        if self.args.config_clear is not None:
            self.configurator.clear()
            print('Cleared')
            return

        self.configurator.init_configure()

        if self.args.containers is not None:
            self.configurator.display_containers()
            return

        # init containers objects
        self.containers = self.init_containers(self.configurator.config)

        # check status of all containers
        self.watcher = Watcher()
        self._update_containers_meta()

        if self.args.state is not None:
            self._show_containers_states()
            return

        # read args and run containers command.
        self.send_commands(self.args)
        self.activate_commands(self._active_containers)

        # check status of all containers
        self.watcher = Watcher()
        self._update_containers_meta()
        self._show_containers_states()

    def init_containers(self, config) -> Dict[str, Container]:
        containers = dict()
        for cfg in config['containers']:
            container = Container(alias=cfg['alias'], container_name=cfg['container_name'],
                                  build=cfg['build'], run=cfg['run'],
                                  description=cfg.get('description'))
            containers[cfg['alias']] = container
        return containers

    def send_commands(self, args):
        commands = vars(args)
        for command in [key for key in commands.keys() if commands[key] is not None and key != 'all']:
            containers = list()
            if commands.get('all', None) is not None:
                containers = self.containers.values()
            else:
                containers_list = commands[command]
                for container_name in containers_list:
                    container = self.containers.get(container_name, None)
                    if container is not None:
                        containers.append(container)
                    else:
                        raise ValueError(f'No exists container with name {container_name}')
            self.send_command(Command[str.upper(command)], containers)

    def send_command(self, command: Command, containers: List[Container]):
        for container in containers:
            container.set_command(command)
            self._active_containers.add(container)

    def activate_commands(self, containers: Set[Container]):
        for container in containers:
            container.activate_commands()

    def _check_containers_status(self):
        for alias, container in self.containers.items():
            container.state = self.watcher.get_status(container.container_name)

    def _get_containers_ids(self):
        for alias, container in self.containers.items():
            container.container_id = self.watcher.get_container_id(container.container_name)

    def _show_containers_states(self):
        print('\nContainers\' states:')
        for alias, container in self.containers.items():
            print(f'--- {alias} is {container.state.name}')

    def _update_containers_meta(self):
        self._check_containers_status()
        self._get_containers_ids()
