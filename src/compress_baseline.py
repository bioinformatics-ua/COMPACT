#!python
#!/usr/bin/env python

'''
  Usage: python3 src/compress_baseline.py
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

Name = "compression_time"
percentages = [0,1,2,4,6,8,10]
tmpDir = os.path.join(root, "tmp/")
tmpSeqPath = join("..","tmpSq")
domains = ["viral", "bacteria", "archaea", "fungi", "plant", "protozoa", "mitochondrion", "plastid"]


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
             "NAF_comp","NUHT_comp","pufferfish_comp","UHT_comp","unzip_comp","xz_comp","zstd_comp",
             "bzip2_time","Cmix_time","GeCo3_time","gzip_time","JARVIS_time","MFCompress_time",
             "NAF_time","NUHT_time","pufferfish_time","UHT_time","unzip_time","xz_time","zstd_time"])
    
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
                "NAF_comp": None,"NUHT_comp": None,"pufferfish_comp": None,"UHT_comp": None,"unzip_comp": None,"xz_comp": None,"zstd_comp": None,
                "bzip2_time": None,"Cmix_time": None,"GeCo3_time": None,"gzip_time": None,"JARVIS_time": None,"MFCompress_time": None,
                "NAF_time": None,"NUHT_time": None,"pufferfish_time": None,"UHT_time": None,"unzip_time": None,"xz_time": None,"zstd_time": None
            }

            print(f"\tFile {fileName}")
            filePath = join(mergedPath, domain, fileName)
            if isfile(filePath):
                decompressedPath= filePath.replace(".gz", "")
                os.system(f'gzip -k -d {filePath}')
                

                os.system(f'zcat {filePath} | grep -v ">" | tr -d -c "ACGT" > {tmpPath}/GENOME_FILE')
                original_file=join(tmpPath,"GENOME_FILE")
                original_sz = os.path.getsize(original_file)
                
                os.system(f'{compressors_path}compress {decompressedPath} ')
                os.system(f'{compressors_path}ennaf {decompressedPath} -o GENOME_FILE.naf --temp-dir tlm')
                os.system(f'pufferfish -i GENOME_FILE -o GENOME_FILE.puf [-c] ')

                #CMIX
                # start_cmix = time.time()
                # os.system(f"{compressors_path}cmix -c GENOME_FILE cmix.seq")
                # end_cmix = time.time()
                # compressed_file=join(tmpPath,"cmix.seq")
                # cmp_sz = os.path.getsize(compressed_file)
                # elapsed_time_cmix=end_cmix-start_cmix
                # csvEntry["Cmix_comp"] = str(cmp_sz/original_sz*2)
                # csvEntry["Cmix_time"] = elapsed_time_jarvis

                #JARVIS
                # start_jarvis = time.time()
                # os.system(f"JARVIS -l 3 {tmpPath}/GENOME_FILE ")
                # end_jarvis = time.time()
                # compressed_file=join(tmpPath,"GENOME_FILE.jc")
                # cmp_sz = os.path.getsize(compressed_file)
                # elapsed_time_jarvis=end_jarvis-start_jarvis

                # csvEntry["JARVIS_comp"] = str(cmp_sz/original_sz*2)
                # csvEntry["JARVIS_time"] = elapsed_time_jarvis
                # print(str(cmp_sz/original_sz))
                
                sys.exit()
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