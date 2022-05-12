FROM ubuntu:20.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update && apt install -y wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh\
    && mkdir /root/.conda \
    && bash Miniconda3-py39_4.11.0-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py39_4.11.0-Linux-x86_64.sh

RUN apt-get update -y && apt-get install -y bc

RUN apt-get install -y zip 
RUN apt-get install -y bzip2
RUN apt-get install -y xz-utils 
RUN apt-get install -y zstd
RUN apt-get install -y gzip

RUN apt-get install -y gcc-multilib

RUN apt-get install -y build-essential

RUN apt-get install -y clang

RUN apt-get install -y git

RUN conda install anaconda-client --yes

RUN conda install -c bioconda libgcc --yes

RUN pip3 install -r requirements.pip

RUN chmod +x ./*sh

ADD . /compact 

WORKDIR /compact

CMD tail -f >> /dev/null