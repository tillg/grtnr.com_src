# Example .devcontainer/Dockerfile
# Use the Python dev container base image
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install extra packages
RUN apt-get update \
  && apt-get install -y \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

# Set up non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME || true \
  && id -u $USERNAME || useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install zsh and set it as the default shell
RUN apt-get update && apt-get install -y zsh && \
  chsh -s $(which zsh) $USERNAME

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Install Python dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Install the Dev Containers CLI
RUN npm install -g @devcontainers/cli

# Set permissions for the non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

