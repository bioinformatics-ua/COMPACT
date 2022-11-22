# COMPACT
<H2><b>COMPressor tAxonomic ClassificaTion</b></H2>

### Team
  * Jorge M. Silva<sup id="a1">[1](#f1)</sup>
  * João R. Almeida<sup id="a1">[1](#f1)</sup><sup id="a2">[2](#f2)</sup>

1. <small id="f1"> University of Aveiro, Dept. Electronics, Telecommunications and Informatics (DETI / IEETA), Aveiro, Portugal </small> [↩](#a1)
2. <small id="f2"> University of A Coruña, Dept. of Information and Communications Technologies, A Coruña, Spain </small> [↩](#a2)

### How to use?
#### Download Project
Get COMPACT project using:
```bash
git clone https://github.com/jorgeMFS/COMPACT.git
cd COMPACT/
```

#### Using Docker
To perform installation correctly, docker and docker compose must be installed in the system (see https://docs.docker.com/engine/install/ubuntu/). 

Then, follow these instructions:
```sh
git clone https://github.com/jorgeMFS/COMPACT.git
cd COMPACT
docker-compose build
docker-compose up -d && docker exec -it compact bash && docker-compose down
```

#### Install Compressors
Give run Install Compressors for Benchmark:
``` bash
bash install_compressors.sh;
```

### Result Replication
To run the pipeline and obtain all the Reports in the folder reports, use the following commands.


#### Download sequences I
For obtaining random sequences for baseline test performance run:

``` bash
cd src/
python3 getRandomSequences.py 
```

#### Baseline test
For baseline compression test run:

``` bash
cd src/
python3 compress_baseline.py
```

#### Download sequences II
For obtaining random sequences for taxonomic classification run:

``` bash
cd src/
python3 getDatabaseSequences.py 
```

### Classifiers

#### Feature selection for f1-score and accuracy

```bash
cd src/
python3 classifier.py -fs -ac -b > ../results/feature_selection.txt
```

#### All columns for f1-score and accuracy

```bash
cd src/
python3 classifier.py -ac -b > ../results/f1score_accuracy_all_columns.txt
```

#### Each column individually for f1-score and accuracy

```bash
cd src/
python3 classifier.py -b > ../results/f1score_accuracy_single.txt
```

#### Classification report for each compressor

```bash
cd src/
python3 classifier.py -cr > ../results/classification_reports_single.txt
```

#### Classification f1-score and accuracy for all possible feature combinations

```bash
cd src/
python3 classifier.py -bf -b > ../results/f1score_accuracy_all_combinations.txt
```

#### Classification report for all compressors

```bash
cd src/
python3 classifier.py -cr -ac > ../results/classification_report_all_columns.txt
```

#### Classification report for all compressors

```bash
cd src/
python3 classifier.py -bf -cr > ../results/classification_report_all_combinations.txt
```

### Cite

Please cite the following, if you use COMPACT in your work:

```bib
@inproceedings{silva2022value,
  title={The value of compression for taxonomic identification},
  author={Silva, Jorge Miguel and Almeida, Joao Rafael},
  booktitle={2022 IEEE 35th International Symposium on Computer-Based Medical Systems (CBMS)},
  pages={276--281},
  year={2022},
  organization={IEEE}
}
```

### Issues
Please let us know if there are any
[issues](https://github.com/bioinformatics-ua/COMPACT/issues).
