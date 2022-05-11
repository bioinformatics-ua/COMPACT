# COMPACT
COMPressor tAxonomic ClassificaTion


## Download Project
Get CANVAS project using:
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




## Download sequences
For obtaining random sequences for performance test run:

``` bash
cd src/
python3 getRandomSequences.py 
```

## Bsseline test
For baseline compression test run:

``` bash
cd src/
python3 compress_baseline.py
```