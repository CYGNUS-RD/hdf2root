#!/usr/bin/env python
# coding: utf-8

import os,sys
import h5py
import numpy as np 
import ROOT
from root_numpy import array2hist

from readerHIS import openHIS

def swift_auth():
    # https://docs.openstack.org/python-swiftclient/latest/service-api.html
    # https://docs.openstack.org/python-swiftclient/

    import swiftclient
    from keystoneauth1 import session
    from keystoneauth1.identity import v3

    
    # Read Write account
    OS_REGION_NAME='cnaf'
    OS_USER_DOMAIN_NAME='default'
    OS_PROJECT_DOMAIN_NAME='default'
    OS_PROJECT_NAME='cygnus-default'
    OS_IDENTITY_API_VERSION='3'
    OS_PASSWORD='BLAH_BLAH'
    OS_AUTH_TYPE='password'
    OS_AUTH_STRATEGY='keystone'
    OS_AUTH_URL='https://keystone.cloud.infn.it:5000/v3/'
    OS_USERNAME='CHANGE_ME'
    OS_STORAGE_URL='https://swift.cloud.infn.it:8080/v1/AUTH_1e60fe39fba04701aa5ffc0b97871ed8'


    _auth = v3.Password(
        user_domain_name    = OS_USER_DOMAIN_NAME,
        project_domain_name = OS_PROJECT_DOMAIN_NAME,
        project_name        = OS_PROJECT_NAME,
        username            = OS_USERNAME,
        password            = OS_PASSWORD,
        auth_url            = OS_AUTH_URL
    )
    _os_options={
        'region_name' : OS_REGION_NAME, 
        'object_storage_url': OS_STORAGE_URL
    }
    # Create session
    keystone_session = session.Session(auth = _auth)

    # Create swiftclient Connection
    swift = swiftclient.Connection(session      = keystone_session, 
                                    auth_version = OS_IDENTITY_API_VERSION,
                                    os_options   = _os_options
                                    )
    return swift

def swift_put(file_name):
    container_name = 'Cygnus'
    with open(file_name, 'rb') as data:
        swift = swift_auth()
        swift.put_object(container_name, file_name, data)
    return 
def mv_file(filein, fileout):
    command = '/bin/mv ' + filein + ' ' + fileout
    return os.system(command)

def rm_file(filein):
    command = '/bin/rm '+ filein
    return os.system(command)

def grep_file(what, filein):
    command = '/usr/bin/grep ' + what +' '+filein
    status, output = commands.getstatusoutput(command)
    return output
def append2file(line, filein):
    command = 'echo '+ line + ' >> '+filein
    return os.system(command)


def ruttalo(his_file):
    stem, _ = os.path.splitext(his_file)
    his = openHIS(his_file)
    outname = stem+'.root' 
    rf = ROOT.TFile(outname,'recreate')

    runN = stem.split('run')[-1]
    run = runN if len(runN) else 'XXXX'

    for idx, section in enumerate(his):
        if idx % 5 == 0: print("transferring image ",idx)
        (nx,ny) = section.shape 
        title = stem + ('_%04d' % idx)
        postfix = 'run{run}_ev{ev}'.format(run=run,ev=idx)
        title = 'pic_{pfx}'.format(pfx=postfix)
        h2 = ROOT.TH2S(title,title,nx,0,nx,ny,0,ny)
        h2.GetXaxis().SetTitle('x')
        h2.GetYaxis().SetTitle('y')
        _ = array2hist(np.fliplr(np.transpose(section)),h2)
        h2.Write()
    rf.Close()
    return outname, run

if __name__ == '__main__':

    path = '/Users/mazzitel/lime/'
    subdir = 'Data/MAN/'
    for file in os.listdir(path):
        if file.endswith(".HIS") and file.startswith("run"):
            his_file = path+file
            print (his_file)
            filein, run = ruttalo(his_file)
            fileout = 'histograms_Run{run}.root'.format(run=run)
            append2file(fileout, path+'/daq_rooted.log')
            print ("file {} done".format(fileout))
            mv_file(filein, path+subdir+fileout)
            os.chdir(path)
            swift_put(subdir+fileout)
            append2file(fileout, path+'/daq_copyed.log')
            print ("file {} copied".format(fileout))
            rm_file(his_file)
            print ("file {} removed".format(his_file))
            rm_file(subdir+fileout)
            print ("file {} removed".format(fileout))

    print("ALL DONE")

