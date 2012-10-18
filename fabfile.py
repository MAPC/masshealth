"""
This is a fabric script file that allows for remote deployment of
GeoNode and a GeoNode project via ssh. 

To install GeoNode:
    fab -H user@hostname geonode_install
To install a GeoNode project:
    fab -H user@hostname project_install

This file currently gets GeoNode from GitHub, but should install
from repo or debian package
"""
# Usage:
#     fab -H user@hostname 

import os
import datetime
from fabric.api import env, sudo, run, cd, local, put, prefix
from fabric.contrib.project import rsync_project
from urlparse import urlparse

# GeoNode Project info
#BRANCH = 'develop'
#GIT_URL = 'git://github.com/MAPC/masshealth.git' 
PROJECT = 'masshealth'

INSTALLDIR = '/var/lib'
GEONODE_BRANCH = 'dev'
GEONODE_GIT_URL = 'git://github.com/GeoNode/geonode.git'

# Derived variables
GEONODEDIR = INSTALLDIR + '/geonode'
PYLIBS = GEONODEDIR + '/lib/python2.7/site-packages'
ACT = 'source ' + GEONODEDIR + '/bin/activate'

# Install GeoNode dependencies
def install_depend():
    #sudo('apt-get install python-dev sun-java6-jre libxml2-dev libxslt1-dev libapache2-mod-wsgi python-pastescript gettext postgres-9.1-postgis apache2')
    sudo('apt-get install -y python-virtualenv')
    sudo('cd %s; virtualenv geonode;' % INSTALLDIR)
    sudo('apt-get install -y gcc python-pastescript python-dev libxml2-dev libxslt1-dev maven2 tomcat6 apache2')
    # Database
    sudo('apt-get install -y postgresql-9.1-postgis postgresql-server-dev-9.1')

# Fetch GeoNode from GitHub
def get_geonode():
    with cd(GEONODEDIR):
        sudo('apt-get install -y git')
        sudo('rm -rf setup')
        sudo('git clone -b %s %s setup' % (GEONODE_BRANCH, GEONODE_GIT_URL))

# Install GeoNode
def setup_geonode():
    get_geonode()
    with cd(GEONODEDIR), prefix(ACT):
        sudo('pip install -e setup')
        sudo('cd setup; paver setup')
        sudo('cp -r setup/geonode %s' % PYLIBS )
        sudo('cp setup/geoserver-geonode-ext/target/geoserver.war /var/lib/tomcat6/webapps/')
        # Use debian package instead
        #sudo('git branch deb;paver deb')
        #sudo('dpkg -i geonode/geonode*.deb')

def setup_project():
    #run('git clone -b %s %s %S' % (BRANCH, GIT_URL, PROJECT))
    # Put apps....change settings to get project apps automagically
    put('accounts',PYLIBS,use_sudo=True)
    put('datastories',PYLIBS,use_sudo=True)
    put('heroes',PYLIBS,use_sudo=True)
    put('monkey_patches',PYLIBS,use_sudo=True)
    put('places',PYLIBS,use_sudo=True)
    put('programs',PYLIBS,use_sudo=True)
    put('visualizations',PYLIBS,use_sudo=True)
    put('masshealth',PYLIBS,use_sudo=True)
    put('requirements.txt',GEONODEDIR,use_sudo=True)
    with cd(GEONODEDIR), prefix(ACT):
        sudo('pip install -r requirements.txt')

def setup_apache():
    with prefix(ACT):
        run("perl -pi -e 's/REPLACE_WITH_PYLIBS/%s/g' %s/%s.apache" % (PYLIBS, PROJECT, PROJECT))
        run("perl -pi -e 's/REPLACE_WITH_PYLIBS/%s/g' %s/%s.apache" % (PYLIBS, PROJECT, PROJECT))
        sudo('cp %s/%s.apache /etc/sites-available/%s' % (PROJECT, PROJECT, PROJECT))
        #sudo("a2enmod proxy_http")
        sudo('a2dissite default; a2ensite %s; service apache2 reload' % PROJECT)

def setup_pgsql():
    sudo("createuser -SDR %s" % PROJECT, user="postgres")
    sudo("createdb -O %s %s" %(PROJECT,PROJECT), user="postgres")
    sudo("psql -c \"alter user %s with encrypted password '%s'\" " % (PROJECT,PROJECT), user="postgres")
    # Need to restore database and GeoServer data
    
def install():
    install_depend()
    get_geonode()
    setup_geonode()
    setup_project() 
    setup_apache()
    setup_pgsql()
