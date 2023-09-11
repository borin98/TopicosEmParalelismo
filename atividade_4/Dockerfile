FROM ubuntu:22.04

# CMake version 3.25.1
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1-linux-x86_64.sh && \
    mkdir -p /usr/local && \
    /bin/sh /var/tmp/cmake-3.25.1-linux-x86_64.sh --prefix=/usr/local --skip-license && \
    rm -rf /var/tmp/cmake-3.25.1-linux-x86_64.sh
ENV PATH=/usr/local/bin:$PATH

# LLVM compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        clang-15 \
        libomp-15-dev && \
    rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/clang clang $(which clang-15) 30 && \
    update-alternatives --install /usr/bin/clang++ clang++ $(which clang++-15) 30

# GDRCOPY version 2.2
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/NVIDIA/gdrcopy/archive/v2.2.tar.gz && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/v2.2.tar.gz -C /var/tmp -z && \
    cd /var/tmp/gdrcopy-2.2 && \
    mkdir -p /usr/local/gdrcopy/include /usr/local/gdrcopy/lib && \
    make CC=clang CXX=clang++ prefix=/usr/local/gdrcopy lib lib_install && \
    rm -rf /var/tmp/gdrcopy-2.2 /var/tmp/v2.2.tar.gz
ENV CPATH=/usr/local/gdrcopy/include:$CPATH \
    LD_LIBRARY_PATH=/usr/local/gdrcopy/lib:$LD_LIBRARY_PATH \
    LIBRARY_PATH=/usr/local/gdrcopy/lib:$LIBRARY_PATH

# KNEM version 1.1.4
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        git && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && cd /var/tmp && git clone --depth=1 --branch knem-1.1.4 https://gitlab.inria.fr/knem/knem.git knem && cd - && \
    mkdir -p /usr/local/knem && \
    cd /var/tmp/knem && \
    mkdir -p /usr/local/knem/include && \
    cp common/*.h /usr/local/knem/include && \
    rm -rf /var/tmp/knem
ENV CPATH=/usr/local/knem/include:$CPATH

# UCX version 1.14.1 Installation

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        autoconf \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/openucx/ucx/releases/download/v1.14.1/ucx-1.14.1.tar.gz && \
    tar xzf ucx-1.14.1.tar.gz

COPY compiler.m4 /ucx/config/m4/compiler.m4

RUN cd ucx-1.14.1 && \
    ./contrib/configure-release --prefix=/usr/local/ucx && \
    make -j8 install && \
    rm -rf ucx-1.14.1 && \
    rm -rf ucx-1.14.1.tar.gz

# OpenMPI 4.1.4 with UCX installation

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
    cd /var/tmp/openmpi-4.1.5 &&  CC=clang CXX=clang++ ./configure --prefix=/usr/local/openmpi --disable-getpwuid --enable-orterun-prefix-by-default --with-ucx=/usr/local/ucx --without-cuda --without-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-4.1.5 /var/tmp/openmpi-4.1.5.tar.bz2
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

# MPI benchmark

COPY mpi_hello_world.c /var/tmp/mpi_hello_world.c

RUN mpicc -o /usr/local/bin/mpi_hello_world /var/tmp/mpi_hello_world.c

# Clang benchmark

COPY clang_hello_world.c /var/tmp/clang_hello_world.c

RUN clang -o /usr/local/bin/clang_hello_world /var/tmp/clang_hello_world.c

# Downloading miniVite package

RUN git clone https://github.com/ECP-ExaGraph/miniVite.git

COPY Makefile /miniVite

RUN cd /miniVite && \
    make && \
    mv ./miniVite /usr/local/bin/ && \
    rm -rf /miniVite && \
    apt-get purge --auto-remove git -y

# Testing if the mpi is working

RUN mpirun --allow-run-as-root --help

RUN echo "mpi version"

RUN mpirun --allow-run-as-root --version

RUN mpirun -n 4 --allow-run-as-root mpi_hello_world

# Testing the Clang version

RUN echo Clang version

RUN clang --version

RUN "./usr/local/bin/clang_hello_world"

# Testing the miniVite package

RUN mpirun -n 2 --allow-run-as-root miniVite -n 100



