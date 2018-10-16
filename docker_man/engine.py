from typing import Dict, Set, List

from docker_man.command import Command
from docker_man.configurator import Configurator
from docker_man.container import Container


class Engine(object):
    def __init__(self, args) -> None:
        self.args = args
        self.configurator = Configurator()
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

        # read args and run containers command.
        self.send_commands(self.args)
        self.activate_commands(self._active_containers)

    def init_containers(self, config) -> Dict[str, Container]:
        containers = dict()
        for cfg in config['containers']:
            container = Container(name=cfg['name'], container_name=cfg['container_name'],
                                  build=cfg['build'], run=cfg['run'],
                                  description=cfg.get('description'))
            containers[cfg['name']] = container
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