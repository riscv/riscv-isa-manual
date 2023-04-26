#!/bin/bash

: '
This script is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

SPDX-License-Identifier: CC-BY-SA-4.0

----------------------------------------------------------------------

This script automates the process of building and cleaning the project 
in either a container or on the host system. It supports running on 
Ubuntu 22.04 or later for host builds and can run on macOS and Ubuntu 
for container builds.

Usage
To run the script, you need to pass two command-line arguments:

The first argument should be either container or host. 
    Use container to run the build in a container (supported on macOS and Ubuntu), 
    or host to run the build on the host system (only supported on Ubuntu 22.04 
    or later for now).
The second argument should be either build or clean. 
    Use build to build the project, or clean to clean the build artifacts.

The script can be run with the following command:
    build-locally.sh <container|host> <build|clean>
'

# Function to check which container runtime is installed
check_runtime() {
    if command -v docker >/dev/null 2>&1; then
        CONTAINER_RUNTIME="docker"
    elif command -v podman >/dev/null 2>&1; then
        CONTAINER_RUNTIME="podman"
    else
        CONTAINER_RUNTIME=""
    fi
}

# Function to run Docs build or clean on container
run_container() {
    OPERATION=$1

    if [ -z "$CONTAINER_RUNTIME" ]; then
        echo "No container runtime (Docker or Podman) detected. Please install either Docker or Podman and try again."
        echo "Docker: https://docs.docker.com/engine/install/"
        echo "Podman: https://podman.io/getting-started/installation.html"
        exit 1
    else
        echo "Running container with $CONTAINER_RUNTIME..."
        cd ..
        $CONTAINER_RUNTIME run --rm -v $(pwd):/build riscvintl/riscv-docs-base-container-image:latest /bin/sh -c 'cd ./build && make'
    fi
}

# Function to run Docs build on host
run_makefile() {
    if command -v make >/dev/null 2>&1; then
        echo "Running build on host..."
        make
    else
        echo "Make not found. Please install it and try again."
        exit 1
    fi
}

function delete_files_with_extensions() {
    # Array of file extensions to delete
    extensions=("pdf" "aux" "log" "bbl" "blg" "toc" "out" "fdb_latexmk" "fls" "synctex.gz")

    # Loop through each file extension and delete the files
    for ext in "${extensions[@]}"; do
        find . -type f -iname "*.${ext}" -exec rm -f {} \;
    done
}

# Function to clean the build according to the selection: container or host
clean_build() {
    BUILD_ENV=$1

    case "$BUILD_ENV" in
        container)
            echo "Cleaning build in container environment..."
            check_runtime
            delete_files_with_extensions
            cd ..
            $CONTAINER_RUNTIME run --rm -v $(pwd):/build riscvintl/riscv-docs-base-container-image:latest /bin/sh -c 'cd ./build && make clean'
            ;;
        host)
            echo "Cleaning build in host environment..."
            make clean
            delete_files_with_extensions
            ;;
        *)
            echo "Invalid build environment: $BUILD_ENV"
            echo "Usage: clean_build <container|host>"
            exit 1
            ;;
    esac
}

check_dependencies_linux() {
    echo "Checking dependencies on Linux..."
    missing_dependencies=()
    dependencies=("bison" "build-essential" "cmake" "curl" "flex" "fonts-lyx" "git" "graphviz" \
    "default-jre" "libcairo2-dev" "libffi-dev" "libgdk-pixbuf2.0-dev" "libglib2.0-dev" "libpango1.0-dev" \
    "libxml2-dev" "make" "pkg-config" "ruby" "ruby-dev" "libwebp-dev" "libzstd-dev")

    for dependency in "${dependencies[@]}"; do
        if ! dpkg -l | grep -q "^ii.*$dependency"; then
            missing_dependencies+=("$dependency")
        fi
    done

    if [ ${#missing_dependencies[@]} -gt 0 ]; then
        echo "The following dependencies are missing:"
        for missing_dependency in "${missing_dependencies[@]}"; do
            echo " - $missing_dependency"
        done
        echo "Please install them and try again."
        exit 1
    else
        echo "All dependencies are installed."
    fi
}

check_rubygems_dependencies() {
    echo "Checking Ruby gem dependencies..."
    missing_gems=()
    gems=("asciidoctor" "asciidoctor-bibtex" "asciidoctor-diagram" "asciidoctor-mathematical" \
    "asciidoctor-pdf" "citeproc-ruby" "coderay" "csl-styles" "json" "pygments.rb" "rghost" "rouge" "ruby_dev")

    for gem in "${gems[@]}"; do
        if ! gem list | grep -q "^$gem"; then
            missing_gems+=("$gem")
        fi
    done

    if [ ${#missing_gems[@]} -gt 0 ]; then
        echo "The following Ruby gems are missing:"
        for missing_gem in "${missing_gems[@]}"; do
            echo " - $missing_gem"
        done
        echo "Please install them and try again."
        exit 1
    else
        echo "All Ruby gem dependencies are installed."
    fi
}

check_npm_dependencies() {
    echo "Checking Node.js dependencies..."
    missing_deps=()
    deps=("wavedrom-cli" "bytefield-svg")

    for dep in "${deps[@]}"; do
        if ! npm list -g --depth=0 | grep -q "$dep"; then
            missing_deps+=("$dep")
        fi
    done

    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo "The following Node.js dependencies are missing:"
        for missing_dep in "${missing_deps[@]}"; do
            echo " - $missing_dep"
        done
        echo "Please install them and try again."
        exit 1
    else
        echo "All Node.js dependencies are installed."
    fi
}

# Function to check the operating system and supported build methods
verify_os_and_build() {
    os="$(uname)"
    if [ "$os" = "Darwin" ]; then
        if [ "$1" = "host" ]; then
            echo "Build on host is not supported on macOS yet. Please use 'container' option."
            exit 1
        fi
    elif [ "$os" = "Linux" ]; then
        if [ "$1" = "host" ]; then
            if command -v lsb_release >/dev/null 2>&1 && [ "$(lsb_release -is)" = "Ubuntu" ]; then
                ubuntu_version="$(lsb_release -rs | cut -d. -f1)"
                if [ "$ubuntu_version" -lt 22 ]; then
                    echo "Build on host is only supported on Ubuntu 22.04 or later. Please use 'container' option or update your Ubuntu version."
                    exit 1
                fi
            else
                echo "Build on host is only supported on Ubuntu 22.04 or later. Please use 'container' option or switch to Ubuntu."
                exit 1
            fi
        fi
    else
        echo "This script only supports macOS and Ubuntu. Please use a supported operating system."
        exit 1
    fi
}

build_on_container() {
    echo "Building on container..."
    check_runtime
    run_container
}

build_on_host() {
    echo "Building on host..."
    check_dependencies_linux
    check_rubygems_dependencies
    check_npm_dependencies
    run_makefile
}

# Function to handle command-line arguments
handle_argument() {
    if [ $# -lt 2 ]; then
        echo "Usage: $0 <container|host> <build|clean>"
        echo "  container - run build on container"
        echo "  host - run build on host (only supported on Ubuntu 22.04 or later for now)"
        exit 1
    fi

    verify_os_and_build "$1"

    case "$1" in
        container)
            case "$2" in
                build) build_on_container ;;
                clean) clean_build "container" ;;
                *)
                    echo "Invalid operation: $2"
                    echo "Usage: $0 container <build|clean>"
                    exit 1
                    ;;
            esac
            ;;
        host)
            case "$2" in
                build) build_on_host ;;
                clean) clean_build "host" ;;
                *)
                    echo "Invalid operation: $2"
                    echo "Usage: $0 host <build|clean>"
                    exit 1
                    ;;
            esac
            ;;
        *)
            echo "Invalid option: $1"
            echo "Usage: $0 <container|host> <build|clean>"
            exit 1
            ;;
    esac
}

# Call the function with the command-line argument
handle_argument "$@"
