CC = gcc
CFLAGS = -Wall -Iinclude
LIBS = -lSDL2 -lm

# Release build flags (with obfuscation/stripping including)
RELEASE_FLAGS = -O3 -s -DNDEBUG \
    -fno-asynchronous-unwind-tables \
    -fomit-frame-pointer \
    -fvisibility=hidden \
    -ffunction-sections \
    -fdata-sections \
    -Wl,--gc-sections \
    -fno-ident \
    -fno-stack-protector \
    -fPIE -pie \
    -Wl,-z,relro,-z,now \
    -Wl,--strip-all

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LIBS += -lSDL2
endif
ifeq ($(UNAME_S),Darwin)
    LIBS += -lSDL2
    CFLAGS += -I/usr/local/include
endif

BUILD_DIR = build
SRCS = $(wildcard src/*.c)
OBJS = $(patsubst src/%.c,$(BUILD_DIR)/%.o,$(SRCS))

$(BUILD_DIR)/%.o: src/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

.PHONY: all clean install-deps release debug

# Default: debug build
all: check-sdl tie-dye-chain-attack

# Release build: optimized and stripped
release: CFLAGS += $(RELEASE_FLAGS)
release: clean check-sdl tie-dye-chain-attack
	@echo "Release build complete - symbols stripped"
	strip --strip-all tie-dye-chain-attack 2>/dev/null || strip tie-dye-chain-attack

# Debug build: keep symbols
debug: CFLAGS += -g -O0
debug: clean check-sdl tie-dye-chain-attack
	@echo "Debug build complete - symbols preserved"

tie-dye-chain-attack: $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Check if SDL2 is installed
check-sdl:
	@command -v sdl2-config >/dev/null 2>&1 || { echo "SDL2 not found. Run 'make install-deps' to install."; exit 1; }

# Attempt to install SDL2 (requires sudo on Linux)
install-deps:
	@echo "Attempting to install SDL2..."
ifeq ($(shell uname -s),Linux)
	@if command -v apt-get >/dev/null 2>&1; then \
		echo "Detected Debian/Ubuntu. Installing..."; \
		sudo apt-get update && sudo apt-get install -y libsdl2-dev; \
	elif command -v dnf >/dev/null 2>&1; then \
		echo "Detected Fedora/RHEL. Installing..."; \
		sudo dnf install -y SDL2-devel; \
	elif command -v pacman >/dev/null 2>&1; then \
		echo "Detected Arch Linux. Installing..."; \
		sudo pacman -S --noconfirm sdl2; \
	else \
		echo "Unsupported Linux distribution. Please install SDL2 manually."; \
		exit 1; \
	fi
else ifeq ($(shell uname -s),Darwin)
	@if command -v brew >/dev/null 2>&1; then \
		echo "Installing via Homebrew..."; \
		brew install sdl2; \
	else \
		echo "Homebrew not found. Please install Homebrew first or install SDL2 manually."; \
		exit 1; \
	fi
else
	@echo "Windows detected. Please install SDL2 manually (see README.md)"
endif

clean:
	rm -rf $(BUILD_DIR) tie-dye-chain-attack

help:
	@echo "Available targets:"
	@echo "  make              - Build the project (debug)"
	@echo "  make release      - Build optimized with stripped symbols"
	@echo "  make debug        - Build with debug symbols"
	@echo "  make install-deps - Install SDL2 (Linux/macOS only)"
	@echo "  make clean        - Remove all build artifacts"
	@echo "  make help         - Show this help message"
