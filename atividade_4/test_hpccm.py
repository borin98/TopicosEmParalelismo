#!/usr/bin/env python

"""This python code creates a Dockerfile with open_mpi==4.1.5 (latest version) and clang==15 using the python package HPCCM.

Also, this script was inspired using the workshop [MAKING CONTAINERS EASIER WITH
HPC CONTAINER MAKER](https://bluewaters.ncsa.illinois.edu/liferay-content/document-library/content/HPC%20Container%20Maker%20NCSA%20Webinar.pdf)

To test two functions, you can use the following docker command

# Test the version of clang and open_mpi
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "clang --version && echo "" && mpirun --version"

# Test the compiled hello world for clang and mpi in the container
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "mpirun -n 4 --allow-run-as-root mpi_hello_world && echo "" && ./usr/local/bin/clang_hello_world"

# Test the build to the hello world and run the compiled hello world for clang and mpi in the container (it's the same hello_world as bellow)
docker pull gabrielborimacedo/openmpi_mo:latest && docker run -it --rm gabrielborimacedo/openmpi_mo:latest sh -c "mpicc -o /usr/local/bin/mpi_hello_world /var/tmp/mpi_hello_world.c && mpirun -n 4 --allow-run-as-root mpi_hello_world && echo "" && clang -o /usr/local/bin/clang_hello_world /var/tmp/clang_hello_world.c && ./usr/local/bin/clang_hello_world"

OBS : both hello_world for clang and mpi are on the path /var/tmp/ inside the container
Also, you can find the dockerhub of the repository [here](https://hub.docker.com/r/gabrielborimacedo/openmpi_mo)
"""

import hpccm
from hpccm.building_blocks import *
from hpccm.primitives import baseimage, copy, shell

### Create container Stage
Stage0 = hpccm.Stage()

### Linux distribution
Stage0 += baseimage(image="ubuntu:22.04")

### Compiler
compiler = llvm(version="15", eula=True)
compiler += gnu(version="11", eula=True)
Stage0 += compiler

### openmpi installation
Stage0 += openmpi(cuda=False, infiniband=False, version="4.1.5", toolchain=compiler.toolchain)

### MPI benchmark
Stage0 += copy(src='mpi_hello_world.c', dest='/var/tmp/mpi_hello_world.c')
Stage0 += shell(commands=['mpicc -o /usr/local/bin/mpi_hello_world /var/tmp/mpi_hello_world.c'])

### Clang benchmark
Stage0 += copy(src='clang_hello_world.c', dest='/var/tmp/clang_hello_world.c')
Stage0 += shell(commands=['clang -o /usr/local/bin/clang_hello_world /var/tmp/clang_hello_world.c'])

### Downloading miniVite package
# Set the working directory for miniVite
Stage0 += apt_get(ospackages=["git", "build-essential", "make", "ca-certificates"])
Stage0 += shell(commands=['git clone https://github.com/ECP-ExaGraph/miniVite.git'])
Stage0 += copy(src="Makefile", dest="/miniVite")
Stage0 += shell(commands=['cd miniVite',
                          'make',
                          'mpiexec --allow-run-as-root -n 2 bin/./minivite -l -n 100'])  # Build miniVite

# Testing if the mpi is working
Stage0 += shell(commands=['mpirun --allow-run-as-root --help'])
Stage0 += shell(commands=['echo "mpi version"'])
Stage0 += shell(commands=['mpirun --allow-run-as-root --version'])
Stage0 += shell(commands=['mpirun -n 4 --allow-run-as-root mpi_hello_world'])

# Testing the Clang version
Stage0 += shell(commands=['echo Clang version'])
Stage0 += shell(commands=['clang --version'])
Stage0 += shell(commands=['./usr/local/bin/clang_hello_world'])

### Set container specification output format
hpccm.config.set_container_format("docker")

### Output container specification
print(Stage0)
