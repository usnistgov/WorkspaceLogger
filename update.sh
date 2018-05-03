export XAUTHORITY=$HOME/.Xauthority
export DISPLAY=":0"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
$HOME/anaconda3/bin/python update.py
