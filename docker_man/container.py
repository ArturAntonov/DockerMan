import subprocess
from operator import itemgetter
from typing import List, Dict, Callable, Any

from docker_man.command import Command


class Container(object):
    commands_priority: Dict[Command, int] = {
        Command.STOP: 1,
        Command.SREMOVE: 2,
        Command.REMOVE: 3,
        Command.BUILD: 4,
        Command.RUN: 5,
        Command.RESTART: 6,
        Command.REBUILD: 7,
    }

    # todo replace try-except to process error handler

    def __init__(self, name, container_name, build, run, description):
        self._name = name
        self._container_name = container_name
        self._run = run
        self._build = build
        self._description = description
        self._container_id = None
        self._commands: List[(Command, int)] = list()
        self._command_queue: List[Callable] = list()

    @property
    def name(self):
        return self._name

    def build(self):
        print('build container', self._name)
        try:
            command_tokens = [token for token in self._build.split(' ') if len(token) > 0]
            process = subprocess.run(command_tokens, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print('build error', e)
        print('end build process')

    def run(self):
        print('run container', self._name)
        try:
            command_tokens = [token for token in self._run.split(' ') if len(token) > 0]
            process = subprocess.run(command_tokens, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print('run error', e)
        print('end run process')

    def stop(self):
        try:
            process = subprocess.run(['docker', 'stop', self._container_name], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print('stop error', e)
        print('stop container', self._name)

    def remove(self):
        # docker command for remove
        try:
            process = subprocess.run(['docker', 'rm', self._container_name], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print('remove error', e)
        print('remove container', self._name)

    def restart(self):
        self._append_to_queue(self._command_queue, self.stop)
        self._append_to_queue(self._command_queue, self.run)
        print('restart container', self._name)

    def rebuild(self):
        self._append_to_queue(self._command_queue, self.stop)
        self._append_to_queue(self._command_queue, self.remove)
        self._append_to_queue(self._command_queue, self.build)
        self._append_to_queue(self._command_queue, self.run)
        print('rebuild container', self._name)

    def sremove(self):
        # docker command for sremove
        self._append_to_queue(self._command_queue, self.stop)
        self._append_to_queue(self._command_queue, self.remove)
        print('sremove container', self._name)

    def set_command(self, command: Command):
        # make from commands list with commands and its priorities
        self._commands.append((command, self.commands_priority[command]))

    def activate_commands(self):
        # Sort commands by priority
        self._commands = sorted(self._commands, key=itemgetter(1))
        for command in self._commands:
            if self.commands_priority.get(command[0]) is None:
                raise Exception('Unknown command')

            if command[0] == Command.BUILD:
                self._append_to_queue(self._command_queue, self.build)
            elif command[0] == Command.RUN:
                self._append_to_queue(self._command_queue, self.run)
            elif command[0] == Command.STOP:
                self._append_to_queue(self._command_queue, self.stop)
            elif command[0] == Command.REMOVE:
                self._append_to_queue(self._command_queue, self.remove)
            elif command[0] == Command.SREMOVE:
                self.sremove()
            elif command[0] == Command.RESTART:
                self.restart()
            elif command[0] == Command.REBUILD:
                self.rebuild()

        # after all commands is done clear commands set
        self._commands.clear()

        # run command queue
        # but before just print list
        for func in self._command_queue:
            func()

        self._command_queue.clear()

    def _append_to_queue(self, queue: List[Callable], func: Callable) -> None:
        if func not in queue:
            queue.append(func)

    def __repr__(self) -> str:
        """
        For default tostring() behavior
        :return:
        """
        return f'\nname: {self._name}, \nbuild: "{self._build}", \nrun: "{self._run}"'

    def __eq__(self, o: Any) -> bool:
        """
        Overrides the default implementation
        For equality behavior. For example, for compare in a set
        """
        return self._name == o.name

    def __hash__(self) -> int:
        """Overrides the default implementation"""
        return hash(self._name + self._build + self._run)
