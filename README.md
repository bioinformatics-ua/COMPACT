# COMPACT
<H2><b>COMPressor tAxonomic ClassificaTion</b></H2>


## Download Project
Get COMPACT project using:
```bash
git clone https://github.com/jorgeMFS/COMPACT.git
cd COMPACT/
```

## Using Docker
To perform installation correctly, docker and docker compose must be installed in the system (see https://docs.docker.com/engine/install/ubuntu/). 


Then follow these instructions:
```sh
git clone https://github.com/jorgeMFS/COMPACT.git
cd COMPACT
docker-compose build
docker-compose up -d && docker exec -it compact bash && docker-compose down
```

## Install Compressors
Give run Install Compressors for Benchmark:
``` bash
bash install_compressors.sh;
```

## Result Replication
To run the pipeline and obtain all the Reports in the folder reports, use the following commands.


## Download sequences I
For obtaining random sequences for baseline test performance run:

``` bash
cd src/
python3 getRandomSequences.py 
```

## Baseline test
For baseline compression test run:

``` bash
cd src/
python3 compress_baseline.py
```

## Download sequences II
For obtaining random sequences for taxonomic classification run:

``` bash
cd src/
python3 getDatabaseSequences.py 
```

## Classifiers

### Feature selection for f1-score and accuracy

```bash
python3 classifier.py -fs -ac -b > ../results/feature_selection.txt
```

### All columns for f1-score and accuracy
```bash
python3 classifier.py -ac -b > ../results/f1score_accuracy_all_columns.txt
```

### Each column individually for f1-score and accuracy
```bash
python3 classifier.py -b > ../results/f1score_accuracy_single.txt
```

### Classification report for each compressor
```bash
python3 classifier.py -cr > ../results/classification_reports_single.txt
```

### Classification f1-score and accuracy for all possible feature combinations
```bash
python3 classifier.py -bf -b > ../results/f1score_accuracy_all_combinations.txt
```

### Classification report for all compressors
```bash
python3 classifier.py -cr -ac > ../results/classification_report_all_columns.txt
```

### Classification report for all compressors
```bash
    python3 classifier.py -bf -cr > ../results/classification_report_all_combinations.txt
```