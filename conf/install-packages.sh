apt-get -y update
apt-get -y install wget

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 

# Nope - f(^U%(&^$( echo is not idempotent
# sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# 
# so lets do it this way -
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome*.deb

apt-get -y install \
  wget          \
  git           \
  curl          \
  mc            \
  openssh-client \
  python-pip    \
  mercurial     \
  python-dev    \
  libxml2-dev   \
  libxslt-dev   \
  zlib1g-dev    \
  libjpeg-dev   \
  libgeoip-dev  \
  npm           \
  chromium-chromedriver \
  xvfb          \
  unzip         \
  libffi-dev    \
  libcairo2     \
  libpango1.0-0 \
  libgdk-pixbuf2.0-0 \
  shared-mime-info \
  postgresql-client \
  python-psycopg2 \
  libpq-dev     \
  libgeoip-dev  \

# that last one is pending testing for pip geoip install and response from Nija 11/22/16 JJW
