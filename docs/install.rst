Installation
============

Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. warning::

    Please use the `makefile` to setup your project!

    ``make create_environment  # will create a virtual-env and create an alias to connect``

    ``work_on_gorgias-ai``

    ``make dev-install  # this will install all required dependencies``

    ``pre-commit install``

Please use `make lint` to clean your project, it will run `black, isort, and flake8`, *black* is already available in pre-commit hook

if you just created the project, please use the command `make create_gcs_bucket` to generate the required bucket for the project

Variables .env
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

Please create your .env with command `cp .env.template .env`

In order to run properly the project please fill the ``PINECONE_API_KEY`` and ``OPENAI_API_KEY`` and ``PINECONE_INDEX`` and ``PINECONE_ENV``
environment variables within `.env`.
