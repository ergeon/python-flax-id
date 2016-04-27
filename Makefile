.PHONY: clean deploy distclean install pep8 test

# Project settings
PROJECT = flax_id

# Virtual environment settings
ENV ?= venv
VENV = $(shell python -c "import sys; print(int(hasattr(sys, 'real_prefix')));")

# Python commands
ifeq ($(VENV),1)
	FLAKE8 = flake8
	TOX = tox
else
	FLAKE8 = $(ENV)/bin/flake8
	TOX = $(ENV)/bin/tox
endif

# Setup bootstrap args & tox settings
has_bootstrapper = $(shell python -m bootstrapper --version 2>&1 | grep -v "No module")
requirements = -r requirements.txt

# List directories
dist_dir = ./dist
tox_dir = ./.tox
clean_dirs = ./$(PROJECT) $(ENV) $(shell [ -d $(tox_dir) ] && echo $(tox_dir) || :)


all: install

clean:
	find $(clean_dirs) \( -name "*.pyc" -o -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

distclean: clean
	rm -rf $(ENV)/ ./build/ $(dist_dir)/ ./*egg* ./.coverage $(tox_dir)/

install: .install

.install: requirements.txt setup.py
ifneq ($(has_bootstrapper),)
	python -m bootstrapper -e $(ENV)/
else
	[ ! -d $(ENV)/ ] && virtualenv $(ENV)/ || :
	$(ENV)/bin/pip install $(requirements)
endif
	touch $@

pep8: .install
	$(FLAKE8) --statistics ./$(PROJECT)/ setup.py

test: .install clean pep8
	$(TOX)
