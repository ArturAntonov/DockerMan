import subprocess
import re


class Watcher(object):
    """
        Watcher watch on docker's containers.
        Watcher know either container is online or offline.

    """

    docker_ps_headers = {
        'container_id': 0,
        'image': 1,
        'command': 2,
        'created': 3,
        'status': 4,
        'ports': 5,
        'names': 6
    }

    def __init__(self) -> None:
        self._containers_meta = {}

        # watch on docker ps list and save meta information for containers
        try:
            process = subprocess.run(['docker', 'ps'], check=True, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

            lines = process.stdout.strip().split('\n')[1:]  # no need to store headers
            p = re.compile(r'\s{2,}')

            for line in lines:
                tokens = p.split(line)
                meta = {}
                for column, index in self.docker_ps_headers.items():
                    meta[column] = tokens[index]
                container_name = tokens[self.docker_ps_headers['names']]
                self._containers_meta[container_name] = meta
        except Exception as e:
            print('Watcher Error. docker ps has failed', e)

    def check_status(self, container_name: str) -> str:
        """
            Method checks status of a container by its name.
        Args:
            container_name (str): the name of the container

        Returns:
            str: ether 'online' or 'offline'
        """
        return 'online' if container_name in self._containers_meta else 'offline'
