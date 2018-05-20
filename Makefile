PROJECT := utaws
CUR_DIR = $(shell pwd)
PYTHON_VERSION := python3
PYTHON3_PATH := $(shell which $(PYTHON_VERSION))
GIT := $(shell which git)
VENV_DIR := $(CUR_DIR)/p3_venv
PIP_CALL := $(VENV_DIR)/bin/pip
ACTIVATE = $(shell . $(VENV_DIR)/bin/activate)
MAKE = $(shell which make)
MODULE_PATH := $(CUR_DIR)/$(PROJECT)
SCRIPTS := $(CUR_DIR)/scripts
DOC_PATH := $(CUR_DIR)/docs
REQUIREMENT = $(CUR_DIR)/requirements.txt
VERSION_FILE = $(CUR_DIR)/$(PROJECT)/_version.py


# --- rollup targets  ----------------------------------------------------------


.PHONY: fresh-install fresh-test-install deploy-test deploy-prod

zero-install: clean setup-venv install   ## Install (source: pypi). Zero prebuild artifacts

zero-test-install: clean setup-venv test-install  ## Install (source: testpypi). Zero prebuild artifacts

deploy-test: clean testpypi  ## Deploy (testpypi), generate all prebuild artifacts

deploy-prod: clean pypi   ## Deploy (pypi), generate all prebuild artifacts


# --- targets ------------------------------------------------------------------


.PHONY: pre-build
pre-build:    ## Remove residual build artifacts
	rm -rf $(CUR_DIR)/dist
	mkdir $(CUR_DIR)/dist


.PHONY: setup-venv
setup-venv:    ## Create and activiate python venv
	$(PYTHON3_PATH) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(PIP_CALL) install -U setuptools pip && \
	$(PIP_CALL) install -r $(REQUIREMENT)


.PHONY: test
test:     ## Run pytest unittests
	if [ $(PDB) ]; then PDB = "true"; \
	bash $(CUR_DIR)/scripts/make-test.sh $(CUR_DIR) $(VENV_DIR) $(MODULE_PATH) $(PDB); \
	elif [ $(MODULE) ]; then PDB = "false"; \
	bash $(CUR_DIR)/scripts/make-test.sh $(CUR_DIR) $(VENV_DIR) $(MODULE_PATH) $(PDB) $(MODULE); \
	elif [ $(COMPLEXITY) ]; then COMPLEXITY = "run"; \
	bash $(CUR_DIR)/scripts/make-test.sh $(CUR_DIR) $(VENV_DIR) $(MODULE_PATH) $(COMPLEXITY) $(MODULE); \
	else bash $(CUR_DIR)/scripts/make-test.sh $(CUR_DIR) $(VENV_DIR) $(MODULE_PATH); fi


docs:  setup-venv    ## Generate sphinx documentation
	. $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install sphinx sphinx_rtd_theme autodoc
	cd $(CUR_DIR) && $(MAKE) clean-docs
	cd $(DOC_PATH) && . $(VENV_DIR)/bin/activate && $(MAKE) html


.PHONY: build
build: pre-build setup-venv    ## Build dist, increment version || force version (VERSION=X.Y)
	if [ $(VERSION) ]; then bash $(SCRIPTS)/version_update.sh $(VERSION); \
	else bash $(SCRIPTS)/version_update.sh; fi && . $(VENV_DIR)/bin/activate && \
	cd $(CUR_DIR) && $(PYTHON3_PATH) setup.py sdist


.PHONY: testpypi
testpypi: build     ## Deploy to testpypi without regenerating prebuild artifacts
	@echo "Deploy $(PROJECT) to test.pypi.org"
	. $(VENV_DIR)/bin/activate && twine upload --repository testpypi dist/*


.PHONY: pypi
pypi: clean build    ## Deploy to pypi without regenerating prebuild artifacts
	@echo "Deploy $(PROJECT) to pypi.org"
	. $(VENV_DIR)/bin/activate && twine upload --repository pypi dist/*


.PHONY: install
install:    ## Install (source: pypi). Build artifacts exist
	if [ ! -e $(VENV_DIR) ]; then $(MAKE) setup-venv; fi; \
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install -U $(PROJECT)


.PHONY: test-install
test-install:  ## Install (source: testpypi). Build artifacts exist
	if [ ! -e $(VENV_DIR) ]; then $(MAKE) setup-venv; fi; \
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install -U $(PROJECT) --extra-index-url https://test.pypi.org/simple/


.PHONY: source-install
source-install:    ## Install (source: local source). Build artifacts exist
	if [ ! -e $(VENV_DIR) ]; then $(MAKE) setup-venv; fi; \
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install .


.PHONY: help
help:   ## Print help index
	@printf "\n\033[0m %-15s\033[0m %-13s\u001b[37;1m%-15s\u001b[0m\n\n" " " "make targets: " $(PROJECT)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[0m%-2s\033[36m%-20s\033[33m %-8s\033[0m%-5s\n\n"," ", $$1, "-->", $$2}' $(MAKEFILE_LIST)
	@printf "\u001b[37;0m%-2s\u001b[37;0m%-2s\n\n" " " "___________________________________________________________________"
	@printf "\u001b[37;1m%-3s\u001b[37;1m%-3s\033[0m %-6s\u001b[44;1m%-9s\u001b[37;0m%-15s\n\n" " " "  make" "deploy-[test|prod] " "VERSION=X" " to deploy specific version"


.PHONY: clean-docs
clean-docs:    ## Remove build artifacts for documentation only
	@echo "Clean docs build"
	if [ -e $(VENV_DIR) ]; then . $(VENV_DIR)/bin/activate && \
	cd $(DOC_PATH) && $(MAKE) clean || true; fi


.PHONY: clean
clean:  clean-docs  ## Remove all build artifacts generated by make
	@echo "Cleanup"
	rm -rf $(VENV_DIR)
	rm -rf $(CUR_DIR)/dist
	rm -rf $(CUR_DIR)/*.egg-info
	rm -f $(CUR_DIR)/README.rst || true
	rm -rf $(CUR_DIR)/$(PROJECT)/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/common/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/dynamodb/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/ec2/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/lambda/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/s3/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/sts/__pycache__ || true
	rm -rf $(CUR_DIR)/$(PROJECT)/tags/__pycache__ || true
	rm -rf $(CUR_DIR)/tests/__pycache__ || true
	rm -rf $(CUR_DIR)/.pytest_cache || true