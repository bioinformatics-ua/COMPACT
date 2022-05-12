#!python
#!/usr/bin/env python

'''
  Usage: python3 compress_baseline.py
'''

import os
import sys
from os import listdir, path, makedirs
from os.path import isfile, join, getsize
sys.path.append(os.path.abspath('../src'))
from pprint import pprint
from collections import Counter
import itertools
import time

compressors_path = "../compressors/"
sequencesDir = "./original_sequences/"
mergedPath="../aux/original_sequences/"
root = "../baseline_features/"
UHT_COMP = "../compressors_files/Unbalanced-Huffman-Tree/dist/UHT_compress/"

Name = "compression_time"
percentages = [0,1,2,4,6,8,10]
tmpDir = os.path.join(root, "tmp/")
tmpSeqPath = join("..","tmpSq")
domains = ["viral", "bacteria", "archaea", "fungi", "plant", "protozoa"]


def main():
    _initialize()
    csvContent = getCompressionValues()

def writeCSVLine(line):
    fileName = Name+".csv"
    f = open(join(root, fileName), 'a')
    f.write(",".join(line))
    f.write("\n")
    f.close()

def getCompressionValues():

# ,"bzip2","Cmix","GeCo3","gzip","JARVIS","MFCompress","NAF","NUHT","pufferfish","UHT","unzip","xz","zstd"]

    writeCSVLine(["Domain","bzip2_comp","Cmix_comp","GeCo3_comp","gzip_comp","JARVIS_comp","MFCompress_comp",
             "NUHT_comp","UHT_comp","zip_comp","xz_comp","zstd_comp",
             "bzip2_time","Cmix_time","GeCo3_time","gzip_time","JARVIS_time","MFCompress_time",
             "NUHT_time","UHT_time","zip_time","xz_time","zstd_time"])
    
    # writeCSVLine(["Domain","DNA","AA","GC","L_DNA","L_AA"])
    for domain in listdir(mergedPath):
        print(f"Computing {domain}...")
        tmpPath = join(tmpDir,domain)
        print(tmpPath)
        if not path.exists(tmpPath):
            makedirs(tmpPath)

        for fileName in listdir(join(mergedPath, domain)):
            name = fileName.replace(".fna.gz", "")
            csvEntry = {
                "Domain": domain,
                "bzip2_comp": None,"Cmix_comp": None, "GeCo3_comp": None,"gzip_comp": None,"JARVIS_comp": None,"MFCompress_comp": None,
                "NUHT_comp": None,"UHT_comp": None,"zip_comp": None,"xz_comp": None,"zstd_comp": None,
                "bzip2_time": None,"Cmix_time": None,"GeCo3_time": None,"gzip_time": None,"JARVIS_time": None,"MFCompress_time": None,
                "NUHT_time": None,"UHT_time": None,"zip_time": None,"xz_time": None,"zstd_time": None
            }

            print(f"\tFile {fileName}")
            filePath = join(mergedPath, domain, fileName)
            if isfile(filePath):
                os.system(f'rm {tmpPath}/*')
                decompressedPath = filePath.replace(".gz", "")
                os.system(f'gzip -k -d {filePath}')
                os.system(f'mv {decompressedPath} {tmpPath}/decompressed.fna')
                os.system(f'zcat {filePath} | grep -v ">" | tr -d -c "ACGT" > {tmpPath}/GENOME_FILE')
                original_file=join(tmpPath,"GENOME_FILE")
                original_sz = os.path.getsize(original_file)
                decompressed_sz = os.path.getsize(join(tmpPath,"decompressed.fna"))
                os.system(f'gto_fasta_from_seq  < {tmpPath}/GENOME_FILE > {tmpPath}/x.fa')
                fa_sz=os.path.getsize(join(tmpPath,"x.fa"))
                

                #ZSTD
                start_zstd = time.time()
                os.system(f'zstd -9  {tmpPath}/decompressed.fna -o {tmpPath}/seq.zstd')
                end_zstd = time.time()
                compressed_file=join(tmpPath,"seq.zstd")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_zstd=end_zstd-start_zstd
                csvEntry["zstd_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["zstd_time"] = elapsed_time_zstd

                #XZ
                start_xz = time.time()
                os.system(f'xz -k -9 {tmpPath}/decompressed.fna')
                end_xz = time.time()
                compressed_file=join(tmpPath,"decompressed.fna.xz")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_xz=end_xz-start_xz
                csvEntry["xz_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["xz_time"] = elapsed_time_xz


                #ZIP
                start_zip = time.time()
                os.system(f'zip -9 {tmpPath}/seq.zip {tmpPath}/decompressed.fna')
                end_zip = time.time()
                compressed_file=join(tmpPath,"seq.zip")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_zip=end_zip-start_zip
                csvEntry["zip_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["zip_time"] = elapsed_time_zip

                #BZIP2
                start_bzip2 = time.time()
                os.system(f'bzip2 -k -9 {tmpPath}/decompressed.fna')
                end_bzip2 = time.time()
                compressed_file=join(tmpPath,"decompressed.fna.bz2")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_bzip2=end_bzip2-start_bzip2
                csvEntry["bzip2_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["bzip2_time"] = elapsed_time_bzip2

                #GZIP
                start_gzip = time.time()
                os.system(f'gzip -c {tmpPath}/decompressed.fna > {tmpPath}/seq_gzip.gz')
                end_gzip = time.time()
                compressed_file=join(tmpPath,"seq_gzip.gz")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_gzip=end_gzip-start_gzip
                csvEntry["gzip_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["gzip_time"] = elapsed_time_gzip
                
                #NUHT
                start_nuht = time.time()
                os.system(f'{compressors_path}NUHT_Compress  {tmpPath}/decompressed.fna')
                end_nuht = time.time()
                compressed_file=join(tmpPath,"decompress.nuht")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_nuht=end_nuht-start_nuht
                csvEntry["NUHT_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["NUHT_time"] = elapsed_time_nuht
                
                #UHT
                start_uht = time.time()
                os.system(f'{UHT_COMP}UHT_compress {tmpPath}/decompressed.fna')
                end_uht = time.time()
                compressed_file=join(tmpPath,"decompress_1.uht")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_uht=end_uht-start_uht
                csvEntry["UHT_comp"] = str(cmp_sz/decompressed_sz*2)
                csvEntry["UHT_time"] = elapsed_time_uht


                #MFCompress
                start_mfc = time.time()
                os.system(f"{compressors_path}MFCompressC -3 {tmpPath}/x.fa")
                end_mfc = time.time()
                compressed_file=join(tmpPath,"x.fa.mfc")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_mfc = end_mfc-start_mfc
                csvEntry["MFCompress_comp"] = str(cmp_sz/fa_sz*2)
                csvEntry["MFCompress_time"] = elapsed_time_mfc

                #CMIX
                #start_cmix = time.time()
                #os.system(f"{compressors_path}cmix -c {tmpPath}/GENOME_FILE {tmpPath}/cmix.seq")
                #end_cmix = time.time()
                #compressed_file=join(tmpPath,"cmix.seq")
                #cmp_sz = os.path.getsize(compressed_file)
                #elapsed_time_cmix=end_cmix-start_cmix
                csvEntry["Cmix_comp"] = ""
                csvEntry["Cmix_time"] = ""

                #JARVIS
                start_jarvis = time.time()
                os.system(f"JARVIS -l 3 {tmpPath}/GENOME_FILE ")
                end_jarvis = time.time()
                compressed_file=join(tmpPath,"GENOME_FILE.jc")
                cmp_sz = os.path.getsize(compressed_file)
                elapsed_time_jarvis=end_jarvis-start_jarvis
                csvEntry["JARVIS_comp"] = str(cmp_sz/original_sz*2)
                csvEntry["JARVIS_time"] = elapsed_time_jarvis
                
                #GeCo3
                start_geco = time.time()
                os.system(f"GeCo3 -v -l 3 {tmpPath}/GENOME_FILE | sed '1,6d' | sed '2d' > {tmpPath}/RESULTS_GECO")
                end_geco = time.time()
                elapsed_time_geco=end_geco-start_geco
                os.system(f"cat {tmpPath}/RESULTS_GECO")
                with open(join(tmpPath, "RESULTS_GECO"), 'r') as fp:
                    try:
                        csvEntry["GeCo3_comp"] = str(float(fp.read().split(" ")[7])/2)
                        csvEntry["GeCo3_time"] = elapsed_time_geco
                    except:
                        print(f"WARNING: DNA of {name} was not computed! Maybe lack of free space in RAM!")
                        csvEntry["GeCo3_comp"] = "1"
                os.system(f"rm {tmpPath}/*")
                writeCSVLine(csvEntry.values())



def _initialize():
    if not path.exists(root):
        makedirs(root)
    if not path.exists(tmpDir):
        makedirs(tmpDir)
    if not path.exists(tmpSeqPath):
        makedirs(tmpSeqPath)
    if not path.exists(mergedPath):
        makedirs(mergedPath)

if __name__ == "__main__":
    if "/" in sys.argv[0]:
        print("ERROR: Please run this script inside of src/! There are relative paths defined in this code that need to be respected!")
    else:
        main()