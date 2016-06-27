# MTG Card Identification with Python and OpenCV

## Base Tools

```
sudo apt-get update
sudo apt-get install -y vim git curl build-essential automake autoconf gcc \
 make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
 libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
 openssh-server python-dev python-pip cheese vlc zsh
```

## Oh-My-Zsh (optional)

sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"


## Card Scan

```
git clone https://github.com/YenTheFirst/card_scan.git
cd card_scan
pip install -r requirements.txt
```

## If installing globally install python-opencv package

```
sudo apt-get -y install python-opencv python-numpy libqt4-dev
```

## PyENV

```
curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

# Add the following to ~/.bashrc:

```
export PYENV_ROOT="${HOME}/.pyenv"

if [ -d "${PYENV_ROOT}" ]; then
    export PATH="${PYENV_ROOT}/bin:${PATH}"
    eval "$(pyenv init -)"
fi
```

*Restart your terminal session*

# Setup Python Virtual Environment

```
# If installing in a virtual environment
# $ pyenv install 2.7.11
# pyenv local 2.7.11
# pyenv virtualenv 2.7.11 cardscan
# pyenv local cardscan
pip install -r requirements.txt
```

# Could potentially use card scans of the cropped images for magic workstation

```
wine 
```

## Cockatrice

Install Cockatrice for an updated card xml data set

1. Download from https://cockatrice.github.io/
2. Install with Ubuntu Software Center to get all dependancies
3. Run Oracle card download
