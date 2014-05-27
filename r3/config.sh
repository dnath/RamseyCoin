#! /bin/sh

aws_directory='aws_tools'
code_directory='Ramsey'
aws_git='https://github.com/awslabs/aws-python-sample.git'
ramsey_git='https://github.com/dnath/RamseyCoin.git'


if [ -n "$(command -v yum)" ]; then
  cmd='yum'
elif [ -n "$(command -v apt-get)" ]; then
  cmd='apt-get'
else
  echo 'Failed to find yum/apt-get !!'
  exit
fi

echo 'Repo Update command = ' $cmd

## curl
if [ -z "$(command -v curl)" ]; then
  echo 'Installing curl...'
  sudo $cmd -y install curl
fi

## build-essential : make
if [ -z "$(command -v make)" ]; then
  echo 'Installing build-essential...'
  sudo $cmd -y install build-essential
fi

## gcc
if [ -z "$(command -v gcc)" ]; then
  echo 'Installing gcc...'
  sudo $cmd -y install gcc
fi

## git
if [ -z "$(command -v git)" ]; then
  echo 'Installing git...'
  sudo $cmd -y install git
fi

## vim
if [ -z "$(command -v vim)" ]; then
  echo 'Installing vim...'
  sudo $cmd -y install vim
fi

## python
if [ -z "$(command -v python)" ]; then
  echo 'Installing python...'
  sudo $cmd -y install python
fi

#pip
if [ -z "$(command -v pip)" ]; then
  echo 'Installing pip...'
  sudo $cmd -y install pip
fi

mkdir $aws_directory
cd $aws_directory
git clone $aws_git
pip install boto

cd ..
mkdir $code_directory
cd $code_directory
git clone $ramsey_git



