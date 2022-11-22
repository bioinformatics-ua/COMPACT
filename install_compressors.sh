#!/bin/bash
#
compressor_files_path="compressors_files/"
compressor_path="compressors/"

mkdir -p compressors_files
mkdir -p compressors

rm -rf compressors/*
rm -rf compressors_files/*

Cmix_Installation() {
    mkdir -p ${compressor_files_path}
    wget https://github.com/byronknoll/cmix/archive/refs/tags/v19.1.zip -P ${compressor_files_path}
    unzip ${compressor_files_path}/v19.1.zip 
    cd cmix-19.1/ 
    make
    cp cmix "../${compressor_path}"
    cd ..
    mv cmix-19.1/ ${compressor_files_path}
}

brieflz_Installation(){
    mkdir -p ${compressor_files_path}
    wget https://github.com/jibsen/brieflz/archive/refs/tags/v1.3.0.zip -P ${compressor_files_path}
    unzip -o ${compressor_files_path}v1.3.0.zip
    cd brieflz-1.3.0/example
    make
    cp blzpack "../../${compressor_path}"
    cd ../..
    mv brieflz-1.3.0 ${compressor_files_path}
}

Lizard_Installation(){
    mkdir -p ${compressor_files_path}
    wget https://github.com/inikep/lizard/archive/refs/tags/v1.0.zip -P ${compressor_files_path}
    unzip -o ${compressor_files_path}v1.0.zip
    cd lizard-1.0
    make
    cp lizard "../${compressor_path}"
    cd ../
    mv lizard-1.0 ${compressor_files_path}
}
LZ4_Installation(){
    mkdir -p ${compressor_files_path}
    wget https://github.com/lz4/lz4/archive/refs/tags/v1.9.4.zip  -P ${compressor_files_path}
    unzip -o ${compressor_files_path}v1.9.4.zip
    
}

Brotli__Installation(){
# This specification defines a lossless compressed data format that
#    compresses data using a combination of the LZ77 algorithm and Huffman
#    coding, with efficiency comparable to the best currently available
#    general-purpose compression methods.
    mkdir -p ${compressor_files_path}
    wget https://github.com/google/brotli/archive/refs/tags/v1.0.9.zip -P ${compressor_files_path}
    unzip -o ${compressor_files_path}v1.0.9.zip
    cd brotli-1.0.9;
    mkdir -p out && cd out
    ../configure-cmake
    make
    make test
    make install
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=./installed ..
    cmake --build . --config Release --target install
    cd ../..
    mv brotli-1.0.9 ${compressor_files_path}
}

Libbsc_Installation() {
    #bsc is a high performance file compressor based on lossless,
    #block-sorting data compression algorithms.
    mkdir -p ${compressor_files_path}
    wget  https://github.com/IlyaGrebnov/libbsc/archive/refs/tags/v3.2.4.zip -P ${compressor_files_path}
    unzip -o ${compressor_files_path}/v3.2.4.zip
    cd libbsc-3.2.4/
    make
    cp bsc "../${compressor_path}"
    cd ../
    mv libbsc-3.2.4 ${compressor_files_path}

}
Pufferfish_Installation() {
    #./pufferfish -i <input file> -o <output file> [-c] | [-d]
    cd $compressor_files_path
    git clone https://github.com/alexholehouse/pufferfish.git
    cd pufferfish/src
    make 
    mv  pufferfish ../../../${compressor_path}
    make clean > /dev/null
    cd "../../.."

}


MFCompress_Installation() {
    # ./compress fastq_file.fastq 
    cd $compressor_files_path
    git clone https://github.uconn.edu/sya12005/LFastqC
    cp LFastqC/MFcompress/MFCompressC "../${compressor_path}" 
    cd ".."
}

UHT_Installation() {
    cd $compressor_files_path
    git clone https://github.com/aalokaily/Unbalanced-Huffman-Tree
    cp Unbalanced-Huffman-Tree/dist/UHT_compress/UHT_compress "../${compressor_path}"
    cd ..
}

NAF_Installation() {
    # ennaf file.fa -o file.naf
    cd $compressor_files_path
    git clone --recurse-submodules https://github.com/KirillKryukov/naf.git
    cd naf && make && make test && make install
    cp ennaf/ennaf "../../${compressor_path}"
    cd "../.."
}

NUHT_Installation() {
    cd $compressor_files_path
    git clone https://github.uconn.edu/sya12005/Non-Greedy-Unbalanced-Huffman-Tree-Compressor-for-single-and-multi-fasta-files.git
    cd Non-Greedy-Unbalanced-Huffman-Tree-Compressor-for-single-and-multi-fasta-files
    mv Linux/NUHT_Compress "../../${compressor_path}/NUHT_Compress"
    cd "../.."
}

Lizard_Installation;
exit
conda install -c conda-forge libgcc-ng --yes
conda install -y -c bioconda jarvis --yes
conda install -c bioconda geco3 --yes
conda install -c bioconda naf --yes
conda install -c cobilab gto --yes 

Libbsc_Installation;
Brotli__Installation;
brieflz_Installation;
UHT_Installation;
MFCompress_Installation;
UHT_Installation;
NUHT_Installation;
Cmix_Installation;
chmod +x compressors/*

