.PHONY: build-wheel install-wheel install-dev uninstall-wheel clean very-clean help

PACKAGE_NAME := {% cookiecutter.project_name %}
DIST_DIR := dist

build-wheel:
	python -m build --wheel

install-wheel: build-wheel
	pip install --upgrade $(DIST_DIR)/$(PACKAGE_NAME)-*.whl

uninstall-wheel:
	pip uninstall -y $(PACKAGE_NAME) || true

install-dev: uninstall-wheel install-wheel

help:
	awk -F: '/^[a-zA-Z0-9._-]+:/ {print $1}' Makefile

# Paths
FREEZE := full-requirements.txt
DIRECT := direct-names.txt
REQ_IN := requirements.in
REQ_TXT := requirements.txt

.PHONY: ensure-tools freeze top-level make-unpinned make-pinned clean

ensure-tools:
	python scripts/ensure_tools.py

freeze: ensure-tools
	pip freeze > $(FREEZE)

# produce a file with only top-level package names (no versions)
top-level:
	# require pipdeptree
	pipdeptree --local --warn silence --freeze | sed -n 's/==.*//p' | sed -n '/^[^[:space:]]/p' | sort -u > $(DIRECT)

# build an unpinned requirements.in (names only) and preserve editable/local lines from freeze
make-unpinned: freeze top-level
	# keep editable/local lines from pip freeze
	grep -E '(^-e |@ file://|^{% cookiecutter.project_name %}|^\\-e )' $(FREEZE) > local-lines.tmp || true
	# strip versions from top-level names
	sed 's/==.*//' $(DIRECT) > names-unpinned.tmp
	cat local-lines.tmp > $(REQ_IN)
	# remove common dev packages when producing requirements.in
	grep -v -E '^(build|pip|pipdeptree|pytest|tox|virtualenv|wheel|setuptools|twine|coverage)' names-unpinned.tmp >> $(REQ_IN) || true
	rm -f local-lines.tmp names-unpinned.tmp

# produce a pinned requirements.txt containing exact versions for top-level packages + editable/local lines
make-pinned: freeze top-level
	grep -F -f $(DIRECT) $(FREEZE) > $(REQ_TXT) || true
	grep -E '(^-e |@ file://|^{% cookiecutter.project_name %}|^\\-e )' $(FREEZE) >> $(REQ_TXT) || true
	# optional: sort/unique while keeping editable lines at top
	awk '/^-e/ {print; next} {print | "sort -u"}' $(REQ_TXT) > $(REQ_TXT).tmp || true
	mv $(REQ_TXT).tmp $(REQ_TXT) || true

clean:
	rm -f $(FREEZE) $(DIRECT) $(REQ_IN) $(REQ_TXT)
	rm -rf $(DIST_DIR) *.egg-info

very-clean: clean
	rm -fr data build

# =========================
# Requirements
# =========================

requirements.txt: requirements.in
	pip-compile --upgrade $<

dev-requirements.txt: dev-requirements.in
	pip-compile --upgrade $<

.PHONY: requirements dev-requirements dev test build run

requirements: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt

dev-requirements: dev-requirements.txt
	pip install --upgrade pip
	pip install -r dev-requirements.txt

# =========================
# Development environment
# =========================

dev: requirements dev-requirements
	pip install -e .

# =========================
# Testing
# =========================

test:
	pytest -v

# =========================
# Build
# =========================

build:
	python -m build

# =========================
# Run CLI
# =========================

run:
	python -m contact_importer.cli
