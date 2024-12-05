# Docker Guide

This document provides instructions on how to build and run the Docker image for this project using the provided scripts.

## Prerequisites

Ensure you have Docker installed on your machine. You can check this by running:

```bash
docker --version
```

Additionally, you need to be able to run Docker commands without `sudo`. To do this, you can add your user to the docker group. Here's how:

1. **Add User to Docker Group**: Run the following command, replacing $USER with your username if needed:

    ```bash
    sudo usermod -aG docker $USER
    ```

2. **Log Out and Back In**: After executing the command, log out of your session and then log back in. This will refresh your group membership.
3. **Verify Group Membership**: To verify that you have been added to the docker group, you can run:

    ```bash
    groups
    ```

## Permissions

Before using the scripts, ensure that you set the execute permissions for all three shell scripts (`build.sh`, `run.sh`, and `build_and_run.sh`). You can do this by running:

```bash
chmod +x build.sh run.sh build_and_run.sh
```

## Building the Docker Image

To build the Docker image, you can use the provided `build.sh` script. This script can take a single argument that sets the image tag. If no argument is provided, it defaults to the `latest` tag. If you try building an image with the same tag, the old image will be removed. Navigate to the directory containing the script and run:

```bash
./build.sh [tag]
```

This script will build the Docker image using the `Dockerfile` in the root directory.

## Running the Docker Container

To run the Docker container, you can use the provided `run.sh` script. Use the following command:

```bash
./run.sh
```

### Options

You can run the `run.sh` script with the following options:

* `--train`: Makes the container start the training process.
* `--interactive`: Run the container in interactive mode.
* `--tag <tag>`: Specify the image tag (default: latest).
* `-h`, `--help`: Show the help message.

## Building and Running the Docker Image

If you want to build and run the Docker image in one step, you can use the build_and_run.sh script:

```bash
./build_and_run.sh
```

This script will first build the Docker image and then run the container in non-interactive mode.

## Entrypoint Script

The `Dockerfile` is configured to run the `entrypoint.sh` script when the container starts. This script serves as the entry point for the container. If the container is started in non-interactive mode, the main Python script will run.

## Environment Compatibility

Please note that the provided scripts (`build.sh`, `run.sh`, and `build_and_run.sh`) should be executed in a bash-compatible environment. The `entrypoint.sh` script will only run within the Docker container.
