PROJECT_NAME="unreal-rig-tools"
PROJECT_VERSION:=$(shell cat VERSION | head -1)
GIT_COMMIT:=$(shell git describe --dirty --always)
GIT_BRANCH:=$(shell git rev-parse --abbrev-ref HEAD -- | head -1)
LATEST_GIT_COMMIT:=$(shell git log --format="%H" -n 1 | head -1)
BUILD_USER:=$(shell whoami)
BUILD_DATE:=$(shell date +"%Y-%m-%d")
BUILD_DIR:=$(shell pwd)

ifeq ($(GITHUB_ACTIONS), true)
    BLENDER_BIN ?= blender
    # In CI, we usually don't need to 'install' to a local folder, 
    # but we define a temp path just in case.
	BLENDER_PY ?= ./blender-dist/5.0/python/bin/python3.11
	BLENDER_PY_SITE_PACKAGES ?= ./blender-dist/5.0/python/bin/python3.11/site-packages
    LOCAL_BLENDER_ADDONS_DIR = /tmp/blender/addons
else
    # Local macOS settings
    BLENDER_BIN ?= /Applications/Blender.app/Contents/MacOS/Blender
	BLENDER_PY ?= /Applications/Blender.app/Contents/Resources/5.0/python/bin/python3.11
	BLENDER_PY_SITE_PACKAGES ?= /Applications/Blender.app/Contents/Resources/5.0/python/lib/python3.11/site-packages
    LOCAL_BLENDER_ADDONS_DIR = ~/Library/Application\ Support/Blender/5.0/scripts/addons
endif

LOCAL_BLENDER_ADDON_DIR = $(LOCAL_BLENDER_ADDONS_DIR)/unreal_rig_utils

all: info build
	@echo "$@: complete"

.PHONY: info
info:
	@echo "DEBUG: Version: $(PROJECT_VERSION), Branch: $(GIT_BRANCH), Revision: $(GIT_COMMIT)"
	@echo "DEBUG: Build on $(BUILD_DATE) by $(BUILD_USER)"

.PHONY: build
build:
	@echo "$@: started"
	@mkdir -p dist/
	@rm -rf dist/*.zip
	@zip -r dist/unreal_rig_utils-$(PROJECT_VERSION).zip unreal_rig_utils -x "*.DS_Store"
	@unzip -l dist/unreal_rig_utils-$(PROJECT_VERSION).zip
	@echo "$@: complete"

.PHONE: clean
clean:
	@echo "$@: started"
	@rm -rf tests/tmp/*
	@rm -rf .coverage
	@rm -rf coverage.xml
	@rm -rf dist/
	@echo "$@: complete"

.PHONE: test
test: clean
	@echo "$@: started"
	@set -e; for file in tests/*.py; do \
		$(BLENDER_BIN) --background --python $$file; \
	done
	@echo "$@: complete"

.PHONE: coverage
coverage: clean
	@echo "$@: started"
	@mkdir -p tests/tmp/htmlcov
	$(BLENDER_PY) -V
	$(BLENDER_BIN) --background --python tests/test_rig_gen.py
	$(BLENDER_PY) -m coverage report
	$(BLENDER_PY) -m coverage xml -o coverage.xml
	$(BLENDER_PY) -m coverage html -d tests/tmp/htmlcov
	@echo "$@: complete"

.PHONE: install
install: uninstall
	@echo "$@: started"
	@mkdir -p $(LOCAL_BLENDER_ADDONS_DIR)
	@cp -r unreal_rig_utils $(LOCAL_BLENDER_ADDONS_DIR)
	@echo "$@: complete"

.PHONE: uninstall
uninstall:
	@echo "$@: started"
	rm -rf $(LOCAL_BLENDER_ADDON_DIR)
	@echo "$@: complete"

.PHONY: dep
dep:
	@echo "$@: started"
	pip install -r requirements.txt
	$(BLENDER_PY) -m pip install --upgrade --target "$(BLENDER_PY_SITE_PACKAGES)" coverage
	@echo "$@: complete"

.PHONY: release
release:
	@echo "$@: started"
	@if [ $(GIT_BRANCH) != "main" ]; then echo "cannot release to non-main branch $(GIT_BRANCH)" && false; fi
	@git diff-index --quiet HEAD -- || ( echo "git directory is dirty, commit changes first" && false )
	@versioned -patch
	@echo "Patched version"
	@git add VERSION
	@versioned -release -sync unreal_rig_utils/__init__.py -format blender
	@git add unreal_rig_utils/__init__.py
	@git commit -m "released v`cat VERSION | head -1`"
	@git tag -a v`cat VERSION | head -1` -m "v`cat VERSION | head -1`"
	@git push
	@git push --tags
	@@echo "If necessary, run the following commands:"
	@echo "  git push --delete origin v$(PROJECT_VERSION)"
	@echo "  git tag --delete v$(PROJECT_VERSION)"
	@echo "$@: complete"

.PHONY: license
license:
	@echo "$@: started"
	@for f in `find ./unreal_rig_utils -type f -name '*.py'`; do versioned -addlicense -license gpl3 -copyright="Paul Greenberg greenpau@outlook.com" -year=2026 -filepath=$$f; done
	@echo "$@: complete"
