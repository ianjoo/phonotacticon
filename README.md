# README





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
