import argparse


class ArgumentParser(object):

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        self.__configure_parser(parser)
        self.__args = parser.parse_args()

    @property
    def args(self):
        return self.__args

    def __configure_parser(self, parser):
        parser.add_argument('-b', '--build', help='Build a container', nargs='*')
        parser.add_argument('-r', '--run', help='Run a container', nargs='*')
        parser.add_argument('-rb', '--rebuild', help='Build and Run a container', nargs='*')

        parser.add_argument('-rt', '--restart', help='Restart a container', nargs='*')

        parser.add_argument('-s', '--stop', help='Stop a container', nargs='*')
        parser.add_argument('-rm', '--remove', help='Remove a container', nargs='*')
        parser.add_argument('-srm', '--sremove', help='Stop and Remove a container', nargs='*')

        parser.add_argument('-a', '--all',
                            help='Selected operation will be accept for all of containers',
                            action='count')

        parser.add_argument('--containers', help='Show information about available containers', action='count')
        parser.add_argument('--state', help='Show containers state "online/offline"', action='count')
        parser.add_argument('--configure', help='Path to container-config.json.', type=open)
        parser.add_argument('--config_clear', help='Clear configure file', action='count')
