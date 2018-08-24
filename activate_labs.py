#!/usr/bin/env python

import yaml
import json
import subprocess
from subprocess import PIPE
import pdb
import re
import os

with open("labs_state.yml", 'r') as stream:
    try:
        labs_state=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)




process = subprocess.Popen("ls ./labs", shell=True, stdin=PIPE, stdout=PIPE)

stdout, stderr = process.communicate()

if not process.returncode:
    lab_list = stdout.split() 


for lab in lab_list:

    process = subprocess.Popen("ls ./labs/"+lab+"/*.json", shell=True, stdin=PIPE, stdout=PIPE)
    stdout, stderr = process.communicate()

    if not process.returncode:
        lab_json_filename = os.path.basename(stdout).strip()
        lab_identifier = re.search('(^[0-9][0-9]-iosxr-[0-9][0-9])-',lab_json_filename).group(1)

    process = subprocess.Popen("cat ./labs/"+lab+"/*.json", shell=True, stdin=PIPE, stdout=PIPE)
    stdout, stderr = process.communicate()

    if not process.returncode:
        lab_json = yaml.safe_load(json.dumps(json.loads(stdout)))
        print "Current:  "
        print lab_json["active"]

        if lab_identifier in labs_state:
            print "Intended: "
            print labs_state[lab_identifier]["active"]
            lab_json["active"] = labs_state[lab_identifier]["active"]

            print "##################################################"
            print lab_json
            print "##################################################"
 
    with open("./labs/"+lab+"/"+lab_json_filename, 'w') as outfile:
        json.dump(lab_json, outfile, indent=4)
