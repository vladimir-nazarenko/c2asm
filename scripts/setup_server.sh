sudo pip install virtualenv virtualenvwrapper
cp .bashrc .bashrc.back
echo '
venvwrap="virtualenvwrapper.sh"
#/usr/bin/which $venvwrap
if [ $? -eq 0 ]; then
    venvwrap=`/usr/bin/which $venvwrap`
    source $venvwrap
fi
' >> .bashrc
source .bashrc
mkvirtualenv --python=`which python3` python_web
workon python_web
git clone https://github.com/vladimir-nazarenko/c2asm.git
cd c2asm
pip install -r requirements.txt

