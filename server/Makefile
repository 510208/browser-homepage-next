
UV ?= uv

SERVER_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
BUILD_DIR := $(SERVER_DIR)/dist

APP_NAME := browser-homepage-server
BINARY := $(BUILD_DIR)/$(APP_NAME)

INSTALL_DIR ?= $(HOME)/.local/bin

NUITKA_FLAGS := \
    --mode=standalone \
    --enable-plugin=pyside6 \
    --output-dir=dist \
    --output-filename=$(APP_NAME) \
    --include-data-files=icon.png=icon.png

.PHONY: help sync build run clean rebuild install uninstall

help:
	@echo "Browser Homepage Server"
	@echo ""
	@echo "  sync       Install dependencies"
	@echo "  build      Compile with Nuitka"
	@echo "  run        Run compiled server"
	@echo "  clean      Remove build artifacts"
	@echo "  rebuild    Clean and rebuild"
	@echo "  install    Install executable"
	@echo "  uninstall  Remove installed executable"

sync:
	cd "$(SERVER_DIR)" && $(UV) sync

build:
	cd "$(SERVER_DIR)" && $(UV) run nuitka \
		$(NUITKA_FLAGS) \
		main.py

run: build
	"$(BINARY)"

clean:
	rm -rf "$(BUILD_DIR)" \
		"$(SERVER_DIR)/main.build" \
		"$(SERVER_DIR)/main.dist" \
		"$(SERVER_DIR)/main.onefile-build"

rebuild: clean build

install: build
	install -Dm755 "$(BINARY)" "$(INSTALL_DIR)/$(APP_NAME)"

uninstall:
	rm -f "$(INSTALL_DIR)/$(APP_NAME)"
