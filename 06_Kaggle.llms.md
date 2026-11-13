# Kaggle

Kaggle

Author

Benedict Thekkel

``` python
pip list | grep kaggle
```

    kaggle                    1.6.14
    Note: you may need to restart the kernel to use updated packages.

    mkdir -p ~/.kaggle

    chmod 600 ~/.kaggle/kaggle.json

``` python
import kaggle
```

## List Datasets

``` python
import kaggle

# List datasets
datasets = kaggle.api.dataset_list()
for dataset in datasets:
    print(dataset.ref)
```

    teocalvo/teomewhy-loyalty-system
    shreyanshverma27/online-sales-dataset-popular-marketplace-data
    damirdizdarevic/uefa-euro-2024-players
    anuchhetry/product-sales
    rabieelkharoua/air-quality-and-health-impact-dataset
    mayankanand2701/tesla-stock-price-dataset
    rabieelkharoua/students-performance-dataset
    informrohit1/smartphones-dataset
    muhammadroshaanriaz/e-commerce-trends-a-guide-to-leveraging-dataset
    rashadrmammadov/heart-disease-prediction
    rabieelkharoua/cancer-prediction-dataset
    darrylljk/worlds-best-universities-qs-rankings-2025
    rabieelkharoua/predict-liver-disease-1700-records-dataset
    programmerrdai/ai-computation-and-hardware-trends
    monisamir/global-salary-analysis
    rabieelkharoua/diabetes-health-dataset-analysis
    mexwell/pizza-sales
    rashadrmammadov/lung-cancer-prediction
    mjdskaggle/2024-population-projections-by-country
    shreyaskeote23/india-population-data

## Search for a Dataset

``` python
# Search for a specific dataset
datasets = kaggle.api.dataset_list(search='titanic')
for dataset in datasets:
    print(dataset.ref)
```

    heptapod/titanic
    brendan45774/test-file
    azeembootwala/titanic
    yasserh/titanic-dataset
    rahulsah06/titanic
    shubhamgupta012/titanic-dataset
    fossouodonald/titaniccsv
    prkukunoor/TitanicDataset
    hesh97/titanicdataset-traincsv
    ibrahimelsayed182/titanic-dataset
    pavlofesenko/titanic-extended
    jamesleslie/titanic-cleaned-data
    broaniki/titanic
    zain280/titanic-data-set
    sakshisatre/titanic-dataset
    kittisaks/testtitanic
    abhinavralhan/titanic
    vinicius150987/titanic3
    mahmoudshogaa/titanic-dataset
    ashishkumarjayswal/titanic-datasets

## Download a Dataset

``` python
# Download the Titanic dataset
kaggle.api.dataset_download_files('heptapod/titanic', path='Data/Dataset/titanic', unzip=True)
```

    Dataset URL: https://www.kaggle.com/datasets/heptapod/titanic

## List competitions

``` python
competitions = kaggle.api.competitions_list()
for competition in competitions:
    print(competition.ref)
```

    https://www.kaggle.com/competitions/arc-prize-2024
    https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize
    https://www.kaggle.com/competitions/lmsys-chatbot-arena
    https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2
    https://www.kaggle.com/competitions/leash-BELKA
    https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim
    https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification
    https://www.kaggle.com/competitions/llm-20-questions
    https://www.kaggle.com/competitions/uspto-explainable-ai
    https://www.kaggle.com/competitions/playground-series-s4e6
    https://www.kaggle.com/competitions/titanic
    https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques
    https://www.kaggle.com/competitions/spaceship-titanic
    https://www.kaggle.com/competitions/digit-recognizer
    https://www.kaggle.com/competitions/nlp-getting-started
    https://www.kaggle.com/competitions/store-sales-time-series-forecasting
    https://www.kaggle.com/competitions/connectx
    https://www.kaggle.com/competitions/gan-getting-started
    https://www.kaggle.com/competitions/tpu-getting-started
    https://www.kaggle.com/competitions/contradictory-my-dear-watson

## Download competition data

``` python
kaggle.api.competition_download_files('titanic', path='Data/Competition/titanic')
```

TODO:

- Titanic
- Digit recognizer
- Store Sales
- Competition

``` python
from nbdevAuto import functions
```

``` python
functions.kaggle_competition_download??
```

    Signature:
    functions.kaggle_competition_download(
        name: str,
        folderpath: str = './Data',
    )
    Source:   
    def kaggle_competition_download(name:str, folderpath:str = './Data'):
        'download competition files from kaggle'
        import os
        import shutil
        from pathlib import Path
        
        iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')
        if iskaggle: path = Path(f'../input/{name}')
        else:
            path = Path(f'{folderpath}/{name}')
            if path.exists():print("file exists")
            else:
                import zipfile,kaggle
                kaggle.api.competition_download_cli(competition = name, path = path)
                zipfile.ZipFile(f'{path}/{name}.zip').extractall(path)
    File:      ~/miniconda3/envs/pfast/lib/python3.12/site-packages/nbdevAuto/functions.py
    Type:      function

``` python
functions.kaggle_dataset_download?
```

    Signature:
    functions.kaggle_dataset_download(
        user: str,
        name: str,
        folderpath: str = './Data',
    )
    Source:   
    def kaggle_dataset_download(user:str,
                                name:str,
                                folderpath:str = './Data'):
        'download competition files from kaggle'
        import os
        import shutil
        from pathlib import Path
        iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')
        if iskaggle: path = Path(f'../input/{name}')
        else:
            path = Path(f'{folderpath}/{name}')
            if path.exists():print("file exists")
            else:
                import zipfile,kaggle
                kaggle.api.dataset_download_files(dataset = f'{user}/{name}', path = path)
                zipfile.ZipFile(f'{path}/{name}.zip').extractall(path)
    File:      ~/miniconda3/envs/pfast/lib/python3.12/site-packages/nbdevAuto/functions.py
    Type:      function

Back to top
