FROM ubuntu:22.04

# LLVM compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        clang-15 \
        libomp-15-dev && \
    rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/clang clang $(which clang-15) 30 && \
    update-alternatives --install /usr/bin/clang++ clang++ $(which clang++-15) 30

# OpenMPI version 4.1.5
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bzip2 \
        file \
        hwloc \
        libnuma-dev \
        make \
        openssh-client \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-4.1.5.tar.bz2 && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/openmpi-4.1.5.tar.bz2 -C /var/tmp -j && \
    cd /var/tmp/openmpi-4.1.5 &&  CC=clang CXX=clang++ ./configure --prefix=/usr/local/openmpi --disable-getpwuid --enable-orterun-prefix-by-default --without-cuda --without-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-4.1.5 /var/tmp/openmpi-4.1.5.tar.bz2
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

COPY mpi_hello_world.c /var/tmp/mpi_hello_world.c

RUN mpicc -o /usr/local/bin/mpi_hello_world /var/tmp/mpi_hello_world.c

COPY clang_hello_world.c /var/tmp/clang_hello_world.c

RUN clang -o /usr/local/bin/clang_hello_world /var/tmp/clang_hello_world.c

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
        make && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ECP-ExaGraph/miniVite.git

COPY Makefile /miniVite

RUN cd /miniVite && \
    make && \
    mv ./miniVite /usr/local/bin/ && \
    rm -rf /miniVite && \
    apt-get purge --auto-remove git -y && \
    apt-get purge --auto-remove make -y

RUN mpirun --allow-run-as-root --help

RUN echo "mpi version"

RUN mpirun --allow-run-as-root --version

RUN mpirun -n 4 --allow-run-as-root mpi_hello_world

RUN echo Clang version

RUN clang --version

RUN ./usr/local/bin/clang_hello_world

RUN mpirun --allow-run-as-root -n 2 /usr/local/bin/miniVite -n 100



