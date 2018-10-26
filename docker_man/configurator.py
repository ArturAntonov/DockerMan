import json
import os


class Configurator(object):
    configuration_filename = 'container_configuration_local.json'
    configuration_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), configuration_filename)

    def __init__(self) -> None:
        # read information about containers from config.json
        self._config = {}

    @property
    def config(self):
        return self._config

    def init_configure(self):
        try:
            self._read_container_config()
        except FileNotFoundError:
            raise FileNotFoundError('Config file not found or not initialized. Please initialize configuration file')

    def display_containers(self):
        print('Containers information:')
        for container in self._config['containers']:
            print('\tname:', container['name'])
            print('\tcontainer name:', container['container_name'])
            print('\tdescription:', container['description'])
            print('\tbuild command:', container['build'])
            print('\trun command', container['run'])
            print()

    def parse(self, opened_file) -> None:
        """Parse an incoming file and write the config file local (create a copy)

        Args:
            opened_file (_io.TextIOWrapper): opened file from args with type=open
        Returns:
            None:
        Raises:
            SyntaxError: If configuration file is not valid
        """
        configure = json.load(opened_file)

        if not self._is_valid(configure):
            raise SyntaxError('Config file is not valid')

        with (open(self.configuration_path, 'w')) as fout:
            fout.write(json.dumps(configure))

    def clear(self) -> None:
        if os.path.exists(self.configuration_path):
            os.remove(self.configuration_path)

    def _read_container_config(self):
        with (open(self.configuration_path, 'r')) as fout:
            self._config = json.load(fout)

            if not self._is_valid(self._config):
                raise ValueError('Config file is not valid')

    def _is_valid(self, config) -> bool:
        try:
            for container in config.get('containers', None):
                if container.get('alias', None) is None \
                        or container.get('container_name', None) is None \
                        or container.get('build', None) is None \
                        or container.get('run', None) is None:
                    raise Exception(
                        f'Some of fields: name, container_name, run, build are not valid in record {container}')
            return True
        except Exception as e:
            print('validation error ->', e)
            return False
