# Example .devcontainer/Dockerfile
#FROM mcr.microsoft.com/devcontainers/base:ubuntu
FROM mcr.microsoft.com/devcontainers/python:3.12

# install extra packages
RUN apt-get update \
    && apt-get install -y \
      curl \
      git \
    && rm -rf /var/lib/apt/lists/*

# set up non-root user (if you had that in devcontainer.json)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# …and so on with any ENV, COPY, or other RUN steps you had inline.