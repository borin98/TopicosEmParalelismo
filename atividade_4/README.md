# Activity 4 : Development: Create a container image with HPCCM

This repository contains a python code that creates a Dockerfile with open_mpi==4.1.5 (latest version)
using [ucx](https://openucx.readthedocs.io/en/master/running.html#running-in-docker-containers)==1.14.1, clang==15,
clang++==15 and the package [miniVite](https://github.com/ECP-ExaGraph/miniVite/tree/master) using the python
package [HPCCM](https://github.com/NVIDIA/hpc-container-maker).

Also, this script was inspired using the workshop [MAKING CONTAINERS EASIER WITH
HPC CONTAINER MAKER](https://bluewaters.ncsa.illinois.edu/liferay-content/document-library/content/HPC%20Container%20Maker%20NCSA%20Webinar.pdf)

## Project tree

```{.shell}
.
├── clang_hello_world.c # clang hello code example
├── Dockerfile # Dockerfile for the image with clang 15 and open_mpi==4.1.5
├── mpi_hello_world.c # open_mpi hello code example
├── out_build_hpccm_log.txt # local log for the image build
├── out_hpccm.sh # shell script to create the Dockerfile
├── compiler.m4 # .m4 file used to install ucx whiout the flag -Werror
├── README.md # README.md docs
└── hpccm_recipe.py # python script that generates the Dockerfile
```

## Using miniVite inside the container

To use miniVite, the compiled file version is located at

```{.shell}
cd /usr/local/bin/miniVite
```

## Container run examples

To test two functions, you can use the following docker command

### Test the version of clang and open_mpi

```{.shell}
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "clang --version && echo "" && mpirun --version"
```

### Test the compiled hello world for clang and mpi in the container

```{.shell}
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "mpirun -n 4 --allow-run-as-root mpi_hello_world && echo "" && ./usr/local/bin/clang_hello_world"
```

### Test the build to the hello world and run the compiled hello world for clang and mpi in the container (it's the same hello_world as bellow)

```{.shell}
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "mpicc -o /usr/local/bin/mpi_hello_world /var/tmp/mpi_hello_world.c && mpirun -n 4 --allow-run-as-root mpi_hello_world && echo "" && clang -o /usr/local/bin/clang_hello_world /var/tmp/clang_hello_world.c && ./usr/local/bin/clang_hello_world"
```

### Test the miniVite container version

```{.shell}
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "mpirun --allow-run-as-root -n 2 miniVite -n 100"
```

#### Important notes

both hello_world for clang and mpi are on the path /var/tmp/ inside the container.
Also, you can find the dockerhub of the
repository [here](https://hub.docker.com/layers/gabrielborimacedo/openmpi_mo/latest/images/sha256-20f542f914c87b85ee61e73072a15b6a8d05cc092a664524ee8f7f150f053841?context=explore).
I recommend to use the tag **latest** to test the container