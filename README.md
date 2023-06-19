iff
==============================

Access project: [Web app link (IP)](https:/az-otrope-iff-st-app-alpha-v0-6am8r9.streamlit.app/)

Setup
------------
Please use the `makefile` to setup your project!

    make create_environment  # will create a virtual-env and create an alias to connect
    work_on_IFF_st
    make dev-install  # this will install all required dependencies
    pre-commit install
    streamlit run src/view/app_alpha.py

Please use `make lint` to clean your project, it will run `black, isort, and flake8`, *black* is already available in pre-commit hook

if you just created the project, please use the command `make create_gcs_bucket` to generate the required bucket for the project

Variables .env
------------
Please create your .env with command `cp .env.template .env`

In order to run properly the project please fill the ``PINECONE_API_KEY`` and ``OPENAI_API_KEY`` and ``PINECONE_INDEX`` and ``PINECONE_ENV``and ``SUPABASE_KEY`` and ``SUPABASE_URL``
environment variables within `.env`.

Run the tests
------------
Please use `make tox` to run your tests, it will create its own python-env and run tests through different python version

Project Organization
------------

    ├── LICENSE
    │
    ├── Makefile            <- Makefile with commands like `make data` or `make train`
    │
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── src                <- Source code for use in this project.
    │   ├── domain         <- Scripts to download or generate data
    │   │
    │   ├── infrastructure  <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── interface       <- Scripts to train models and then use trained models to make predictions
    │   │
    │   ├── usecases        <- Scripts to train models and then use trained models to make predictions
    │   │
    │   └── queries         <- Scripts to train models and then use trained models to make predictions
    │
    └── tox.ini             <- tox file with settings for running tox; see tox.readthedocs.io
--------
