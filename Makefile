.PHONY: clean deploy distclean install pep8 test

# Project settings
PROJECT = flax_id

# Virtual environment settings
ENV ?= venv
VENV = $(shell python -c "import sys; print(int(hasattr(sys, 'real_prefix')));")

# Python commands
FLAKE8 = $(ENV)/bin/flake8
TOX = $(ENV)/bin/tox
TWINE = $(ENV)/bin/twine

requirements = -r requirements.txt

# List directories
dist_dir = ./dist
tox_dir = ./.tox
clean_dirs = ./$(PROJECT) $(ENV) $(shell [ -d $(tox_dir) ] && echo $(tox_dir) || :)

# Other settings
SLACK_WEBHOOK_URL ?= https://hooks.slack.com/services/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

all: install

clean:
	find $(clean_dirs) \( -name "*.pyc" -o -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

deploy:
	rm -rf $(dist_dir)/
ifneq ($(CIRCLECI),)
	cp ./pypirc.conf ~/.pypirc
else
	$(MAKE) install test
endif
	python setup.py bdist_wheel
	$(TWINE) upload -r ergeon@pypi dist/*
ifneq ($(CIRCLECI),)
	curl -X POST --data-urlencode 'payload={"username": "circleci", "icon_url": "https://slack.global.ssl.fastly.net/d448/plugins/circleci/assets/bot_48.png", "text": "New `$(PROJECT)` version released: `$(shell python -c 'import $(PROJECT); print($(PROJECT).__version__);')`"}' $(SLACK_WEBHOOK_URL)
endif

distclean: clean
	rm -rf $(ENV)/ ./build/ $(dist_dir)/ ./*egg* ./.coverage $(tox_dir)/

install: .install

.install: requirements.txt setup.py
ifneq ($(has_bootstrapper),)
	python -m bootstrapper -e $(ENV)/
else
	[ ! -d $(ENV)/ ] && python3 -m venv $(ENV)/ || :
	$(ENV)/bin/pip install $(requirements)
endif
	touch $@

pep8: .install
	$(FLAKE8) --statistics ./$(PROJECT)/ setup.py

test: .install clean pep8
	$(TOX)
