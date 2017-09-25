
Vagrant.configure("2") do |config|
config.vm.box = "ubuntu/trusty64"
config.vm.network "private_network", ip: "192.168.33.10"
config.vm.provision "shell", inline: <<-SHELL
#Install Postgresql 9.4
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y postgresql-9.4
sudo apt-get install -y postgresql-server-dev-9.4
#Install GIT
sudo apt-get install -y git
#Install Python and lib
sudo apt-get install -y libtiff5-dev
sudo apt-get install -y libjpeg8-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y liblcms2-dev
sudo apt-get install -y libwebp-dev
sudo apt-get install -y libharfbuzz-dev
sudo apt-get install -y libfribidi-dev
sudo apt-get install -y tcl8.6-dev
sudo apt-get install -y tk8.6-dev
sudo apt-get install -y python-tk
sudo apt-get -y install python-pip
sudo apt-get install -y python-dev python-setuptools
#Clone project
git clone https://github.com/Stebluyk/config.git
cd config/
sudo cp -rf pg_hba.conf /etc/postgresql/9.4/main/pg_hba.conf
sudo cp -rf postgresql.conf /etc/postgresql/9.4/main/postgresql.conf
cd ../
git clone https://github.com/Stebluyk/Blog.git
cd Blog/
pip install -r requirements.txt
sudo service postgresql restart
psql -U postgres -c "ALTER USER postgres with ENCRYPTED password 'admin';"
psql -U postgres -c "CREATE DATABASE blog;"
python manage.py makemigrations
python manage.py migrate
echo "from blog.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminadmin')" | python manage.py shell
#python manage.py runserver
SHELL
end
