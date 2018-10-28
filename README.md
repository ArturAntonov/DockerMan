# docker_man
Python tool for managing docker containers ( run, stop, rebuild and other operations).

The main special ability is --rebuild and --restart operations for one or for all containers at once.

Also you can use other commands for one or for all containers at once.

All commands for each container append to a special Command queue. This queue sorts commands and prevent run mutually exclusive commands.

For example, if you choose both of commands 'STOP' AND 'RESTART', the docker_man will execute only 'RESTART', because 'STOP' command includes in 'RESTART' etc.

## Install
For install just run command:

`pip install git+https://github.com/ArturAntonov/DockerMan.git@master#egg=docker_man`


Where:

```
@master - repository branch.
#egg=docker_man - a name for a folder in the site-packages, where docker_man files will be placed.
```
  

After install, you should add a path to the docker_man executive file if you want to use docker_man in a terminal. 

Docker_man will be installed to the Scripts folder of your virtual environment. For example, in win 10 folder is  `C:\<some_path>\envs\<some_project>\Scripts`

## Usage
* First, you should configure docker_man for work with your containers.

`docker_man --configure <path_to_config.json>`

After this you can use docker_man.

* For help use `docker_man --help`


## Configuration.json format

Used format of configuration file:
```
{
    "containers": [
        {
            "alias": "[Required] this alias uses for terminal calls",
            "container_name": "[Required] this name uses for docker commands call. It should be equal name from build and run commands.",
            "description": "[Optional] description for container. It uses for --containers command",
            "build": "[Required] command for build image",
            "run": "[Required] command for run docker container"
        }
    ]
}
```

Example:
```
{
  "containers": [
    {
      "alias": "my_best_service",
      "container_name": "best_service",
      "description": "Container for my best service",
      "build": "docker build -t best_service -f best_service/Dockerfile .",
      "run": "docker run -d -p 1234:1234 -ti --name best_service best_service"
    }
  ]
}
```

### Important note

You should write a path to a Dockerfile depend on a directory from which you want to call the docker_man. 

For example, a path to a Dockerfile is "best_service/Dockerfile", in this case, you should call the docker_man from root folder for the "best_service/Dockerfile".

If you write the full path to a Dockerfile, then no matter from which directory you cal the docker_man.

In other words, the docker_man see paths relatively itself.
