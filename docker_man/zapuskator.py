from docker_man.argument_parser import ArgumentParser
from docker_man.engine import Engine


def main():
    args = ArgumentParser().args
    # print(f'args for engine is {args}')
    Engine(args).run()


if __name__ == '__main__':
    main()
