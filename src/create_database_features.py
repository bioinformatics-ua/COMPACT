#!python
#!/usr/bin/env python

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
sequencesDir = "./database_sequences/"
mergedPath="../aux/database_sequences/"
root = "../baseline_features/"

Name = "features"
tmpDir = os.path.join(root, "tmp/")
tmpSeqPath = join("..","tmpSq")

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
    writeCSVLine(["Domain","bzip2_comp","JARVIS_comp","MFCompress_comp","NUHT_comp","zstd_comp"])
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
                "bzip2_comp": None,"JARVIS_comp": None,"MFCompress_comp": None,"NUHT_comp": None,"zstd_comp": None,
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
                os.system(f'zstd -9  {tmpPath}/decompressed.fna -o {tmpPath}/seq.zstd')
                compressed_file=join(tmpPath,"seq.zstd")
                cmp_sz = os.path.getsize(compressed_file)
                csvEntry["zstd_comp"] = str(cmp_sz/decompressed_sz)

                #BZIP2
                os.system(f'bzip2 -k -9 {tmpPath}/decompressed.fna')
                compressed_file=join(tmpPath,"decompressed.fna.bz2")
                cmp_sz = os.path.getsize(compressed_file)
                csvEntry["bzip2_comp"] = str(cmp_sz/decompressed_sz)
                
                #NUHT
                os.system(f'{compressors_path}NUHT_Compress  {tmpPath}/decompressed.fna')
                compressed_file=join(tmpPath,"decompress.nuht")
                cmp_sz = os.path.getsize(compressed_file)
                csvEntry["NUHT_comp"] = str(cmp_sz/decompressed_sz)

                #MFCompress
                os.system(f"{compressors_path}MFCompressC -3 {tmpPath}/x.fa")
                compressed_file=join(tmpPath,"x.fa.mfc")
                cmp_sz = os.path.getsize(compressed_file)
                csvEntry["MFCompress_comp"] = str(cmp_sz/fa_sz)

                #JARVIS
                os.system(f"JARVIS -l 3 {tmpPath}/GENOME_FILE ")
                compressed_file=join(tmpPath,"GENOME_FILE.jc")
                cmp_sz = os.path.getsize(compressed_file)
                csvEntry["JARVIS_comp"] = str(cmp_sz/original_sz)

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