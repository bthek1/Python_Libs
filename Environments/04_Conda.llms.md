# Conda

Conda

Author

Benedict Thekkel

## Install Conda

``` bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

## Initialize Conda

``` bash
~/miniconda3/bin/conda init bash
```

## Creating and Managing Environments

``` bash
conda create --name myenv
```

> Example

``` bash
conda create --name myenv python=3.8 numpy pandas
```

## Activating an Environment

``` bash
conda activate myenv
```

## Deactivating an Environment

``` bash
conda deactivate
```

## Listing Environments

``` bash
conda env list
```

## Installing and Managing Packages

``` bash
conda install scipy
```

## Updating Packages

``` bash
conda update numpy
```

## Removing Packages

``` bash
conda remove scipy
```

## Removing an Environment

``` bash
conda env remove --name myenv
```

## Searching for Packages

``` bash
conda search beautifulsoup4
```

## Using Channels

> Conda channels are locations where packages are stored. By default, Conda uses the defaults channel, but you can add others like conda-forge.

------------------------------------------------------------------------

### Adding a Channel

``` bash
conda config --add channels conda-forge
```

### Installing from a Specific Channel

``` bash
conda install -c conda-forge opencv
```

### Listing Conda Channels

``` bash
conda config --show channels
```

``` python
!conda config --show channels
```

    channels:
      - defaults

Back to top
