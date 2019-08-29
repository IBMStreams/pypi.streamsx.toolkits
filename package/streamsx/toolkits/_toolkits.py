# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

# imports
import requests
import json
import re

# GitHub repos of product toolkits
tkprodList = ['com.ibm.streamsx.avro',
              'com.ibm.streamsx.datetime',
              'com.ibm.streamsx.dps',
              'com.ibm.streamsx.elasticsearch',
              'com.ibm.streamsx.eventstore',
              'com.ibm.streamsx.hbase',
              'com.ibm.streamsx.hdfs',
              'com.ibm.streamsx.inet',
              'com.ibm.streamsx.inetserver',
              'com.ibm.streamsx.iot',
              'com.ibm.streamsx.jdbc',
              'com.ibm.streamsx.jms',
              'com.ibm.streamsx.json',
              'com.ibm.streamsx.kafka',
              'com.ibm.streamsx.mail',
              'com.ibm.streamsx.messagehub',
              'com.ibm.streamsx.messaging',
              'com.ibm.streamsx.mqtt',
              'com.ibm.streamsx.network',
              'com.ibm.streamsx.objectstorage',
              'com.ibm.streamsx.rabbitmq',
              'com.ibm.streamsx.sparkmllib',
              'com.ibm.streamsx.topology'
            ]

pypackagelist = ['streamsx',
                 'streamsx.avro',
                 'streamsx.database',
                 'streamsx.elasticsearch',
                 'streamsx.eventstore',
                 'streamsx.eventstreams',
                 'streamsx.hbase', 
                 'streamsx.hdfs',
                 'streamsx.inet',
                 'streamsx.kafka',
                 'streamsx.objectstorage',
                 'streamsx.pmml',
                ]



def _sorted_version(an_iterable):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    an_iterable -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(an_iterable, key = alphanum_key)


def get_pypi_packages():
    """ Discover streamsx python packages on pypi.org
    
    Requires Internet connection

    """
    pypi_packages = {}
    for package_name in pypackagelist:
        r = requests.get('https://pypi.python.org/pypi/'+package_name+'/json')
        if r.status_code==200:
            data_json = r.json()
            releases = list(data_json["releases"].keys())
            latest_version = _sorted_version(releases)[-1]
            print(package_name + ' - ' + latest_version)
            pypi_packages[package_name]=latest_version
    return pypi_packages

def get_installed_packages():
    """ Discover installed `streamsx` python packages
    """
    installed_packages = {}
    for pkg_name in pypackagelist:
        try:
            import importlib
            i = importlib.import_module(pkg_name)
            if pkg_name is 'streamsx':
                import streamsx.topology.context
                print(pkg_name+' - ' + i.topology.context.__version__)
                installed_packages[pkg_name] = i.topology.context.__version__
            else:
                print(pkg_name+' - ' + i.__version__)
                installed_packages[pkg_name] = i.__version__
        except ImportError as error:
            print(pkg_name + ' NOT INSTALLED')
    return installed_packages


def get_build_service_toolkits(streams_cfg):
    """ Discover toolkits on IBM Streams build service.   
    """
    build_service_toolkits = {}
    token = streams_cfg['service_token']
    build_endpoint = streams_cfg['connection_info']['serviceBuildEndpoint']
    toolkits_url = build_endpoint.replace('/builds', '/toolkits', 1)
    #print (toolkits_url)
    r = requests.get(toolkits_url, headers={"Authorization": "Bearer " + token}, verify=False)
    if r.status_code==200:
        sr = r.json()
        #print(sr)
        for x in sr['toolkits']:
            print (x['name'] + ' - ' + x['version'])
            build_service_toolkits[x['name']]=x['version']
    else:
        print(str(r))
    return build_service_toolkits
        

def get_github_toolkits():
    """ Discover product toolkits from public GitHub.
    
    Requires Internet connection
    
    """
    github_toolkits = {}
    for tk_name in tkprodList:
        repo_name = tk_name[8::]
        r = requests.get('https://github.com/IBMStreams/'+repo_name+'/releases/latest')
        #print (r.url)
        if r.status_code==200:
            urlstr = r.url
            tk_version = None
            idx = urlstr.find('tag/v')
            if idx > -1:
                tk_version = urlstr[idx+5:]
            else:
                idx = urlstr.find('tag/')
                if idx > -1:
                    tk_version = urlstr[idx+4:]
            if tk_version is not None:
                print (tk_name + ' - ' + tk_version)
                github_toolkits[tk_name]=tk_version
    return github_toolkits

