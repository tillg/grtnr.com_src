# FROM ubuntu:22.10
FROM ruby:3.1.2

# Configure apt
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y sudo \
  curl \
  git-core \
  gnupg \
  #linuxbrew-wrapper \
  locales \
  zsh \
  wget \
  fonts-powerline 

# set up locale
RUN locale-gen en_US.UTF-8

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog


# Set the default shell to bash rather than sh
ENV SHELL /bin/zsh

# run the installation script  
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

# install powerlevel10k
RUN git clone https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k

RUN cd $HOME && curl -fsSLO https://raw.githubusercontent.com/romkatv/dotfiles-public/master/.purepower

# zsh configuration
COPY .zshrc $HOME
# COPY Gemfile $HOME
RUN apt-get update
RUN sudo apt-get install ruby-full build-essential zlib1g-dev -y
RUN gem install bundler
# RUN bundle install