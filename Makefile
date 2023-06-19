#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = iff
PYTHON_INTERPRETER = python3.10

ifeq (,$(shell which conda))
	HAS_CONDA=False
else
	HAS_CONDA=True
endif
HAS_CONDA=False


ifeq (,$(shell which zsh))
	EXPORT_FILE="bashrc"
else
	EXPORT_FILE="zshrc"
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dev Dependencies
dev-install: requirements.dev.txt
	./venv/bin/python -m pip install -U pip setuptools wheel
	./venv/bin/python -m pip install -r requirements.dev.txt

## Install Python Dependencies
prod-install: requirements.txt
	./venv/bin/python -m pip install -U pip setuptools wheel
	./venv/bin/python -m pip install -r requirements.txt

## Run streamlit app
run_st: dev-install
	./venv/bin/python -m streamlit run streamlit_app.py

## Lint
lint: dev-install
	./venv/bin/python -m black --config=.black .
	./venv/bin/python -m isort --profile=black .
	./venv/bin/python -m flake8 --config=.flake8 .

## Clean venv
clean_venv:
	rm -rf venv

## Clean project
clean:
	rm -rf __pycache__
	rm -rf pytest_cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Install Python Dependencies
tox: create_environment requirements.dev.txt
	rm -rf .tox
	./venv/bin/python -m tox

## Run Test
test: lint
	./venv/bin/python -m pytest -ra -v -m "not e2e" --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## Run End-to-end test
test-e2e: lint
	./venv/bin/python -m pytest -ra -v -m e2e ./tests

## Run End-to-end-baseline test
test-e2e-baseline: lint
	./venv/bin/python -m pytest -ra -v -m e2e --visual-baseline ./tests

## Set up python interpreter environment
create_environment:
ifeq (True, $(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
	conda create --name $(PROJECT_NAME) python=$(PYTHON_INTERPRETER)
	@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install virtualenv
	@echo ">>> Installing virtualenv if not already installed.\nMake sure the following lines are in shell startup file"
	@bash -c "${PYTHON_INTERPRETER} -m venv venv"
	@echo "$(PWD)/venv/bin/activate"
	@echo "alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\" >> ~/.$(EXPORT_FILE)"
	@bash -c "grep -qxF 'alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\"' ~/.$(EXPORT_FILE) || echo 'alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\"' >> ~/.$(EXPORT_FILE)"
	@echo ">>> New virtualenv created. Activate with:\nwork_on_$(PROJECT_NAME)"
endif

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
## Install spacy models
install_spacy_models:
	$(PYTHON_INTERPRETER) -m spacy download xx_ent_wiki_sm


## Create bucket on gcs
create_gcs_bucket:
	gcloud alpha storage buckets create gs://gorgias-ml-development-$(PROJECT_NAME) --project=gorgias-ml-development --default-storage-class=STANDARD --location=US-EAST1 --uniform-bucket-level-access
	gcloud alpha storage buckets create gs://gorgias-ml-staging-$(PROJECT_NAME) --project=gorgias-ml-staging --default-storage-class=STANDARD --location=US-EAST1 --uniform-bucket-level-access
	gcloud alpha storage buckets create gs://gorgias-ml-production-$(PROJECT_NAME) --project=gorgias-ml-production --default-storage-class=STANDARD --location=US-EAST1 --uniform-bucket-level-access

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
