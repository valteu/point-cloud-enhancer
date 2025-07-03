FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4


RUN apt-get update && apt-get install -y --no-install-recommends \
    git cmake ninja-build build-essential \
    libboost-program-options-dev libboost-graph-dev libboost-system-dev \
    libeigen3-dev libflann-dev libfreeimage-dev libmetis-dev \
    libgoogle-glog-dev libgtest-dev libgmock-dev libsqlite3-dev \
    libglew-dev qtbase5-dev libqt5opengl5-dev libcgal-dev libcgal-qt5-dev \
    libceres-dev gcc-10 g++-10 \
    libeigen3-dev \
    libpcl-dev \
    wget unzip && \
    rm -rf /var/lib/apt/lists/*

ENV CC=/usr/bin/gcc-10
ENV CXX=/usr/bin/g++-10
ENV CUDAHOSTCXX=/usr/bin/g++-10

RUN git clone https://github.com/colmap/colmap.git /opt/colmap && \
    mkdir -p /opt/colmap/build && \
    cd /opt/colmap/build && \
    cmake .. -GNinja -DCMAKE_CUDA_ARCHITECTURES="75;86;89" && \
    ninja && \
    ninja install

RUN git clone https://github.com/ETH3D/multi-view-evaluation /opt/multi-view-evaluation
RUN cd /opt/multi-view-evaluation; mkdir build; cd build; cmake ../. ; make;

RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
