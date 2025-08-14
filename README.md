# README

Phonotacticon is a database containing the basic phonotactic information of spoken lects.

The first version, Phonotacticon 1.0, contains 516 lects spoken in Eurasia.

When using this database, please consult and cite the following article:

    Joo, Ian and Yu-Yin Hsu (2025). “Phonotacticon: a cross-linguistic phonotactic database”. In: Linguistic Typology, 29.2, pp. 405-431. DOI: 10.1515/lingty-2023-0094

## Rebuilding CLDF

To rebuild the CLDF dataset, you will need to install some python packages.

Step 1: get a copy of the dataset. Open a terminal and run:

```shell
mkdir dataset
cd dataset
git clone https://github.com/SimonGreenhill/phonotacticon
```

Step 2: set up a virtual environment and install required packages:

```shell
python3 -m venv env
source ./env/bin/activate
pip install -e phonotacticon
```

Step 3: Rebuild CLDF

```shell
cldfbench makecldf Phonotacticon/cldfbench_Phonotacticon.py
```
