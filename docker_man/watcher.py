import re
import subprocess
from typing import Optional

from docker_man.state import State


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

    def get_status(self, container_name: str) -> State:
        """
            Method checks status of a container by its name.
        Args:
            container_name (str): the name of the container

        Returns:
            str: 'online' or 'offline' or 'stopped'
        """
        return State.OFFLINE if container_name not in self._containers_meta \
            else self._containers_meta[container_name]['status']

    def get_container_id(self, container_name: str) -> Optional[str]:
        return self._containers_meta.get(container_name, {}).get('container_id', None)

    def update_meta(self):
        # watch on docker ps list and save meta information for containers
        try:
            process = subprocess.run(['docker', 'ps', '-a'], check=True, shell=True, stdout=subprocess.PIPE,
                                     encoding='utf-8')

            lines = process.stdout.strip().split('\n')[1:]  # no need to store headers
            p = re.compile(r'\s{2,}')

            for line in lines:
                tokens = p.split(line)

                if len(tokens) < len(self.docker_ps_headers):
                    # it means there's no data in the PORTS column
                    tokens.insert(self.docker_ps_headers['ports'], '')
                meta = {}
                # fill metadata for container
                for column, index in self.docker_ps_headers.items():
                    meta[column] = tokens[index]

                status = tokens[self.docker_ps_headers['status']]
                if 'Up' in status:
                    meta['status'] = State.ONLINE
                elif 'Exited' in status:
                    meta['status'] = State.STOPPED
                else:
                    meta['status'] = State.OFFLINE

                container_name = tokens[self.docker_ps_headers['names']]
                self._containers_meta[container_name] = meta
        except Exception as e:
            print('Watcher Error. docker ps has failed', e)
