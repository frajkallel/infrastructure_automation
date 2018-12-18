#!/usr/bin/python

DDOCUMENTATION = '''
---
Author: Fraj KALLEL
module: mongo_replicaset
short_description: Manage members in replicaset add or remove member.
options:
  state:
    required: false
    default: present
    choices: [ "absent", "present" ]
    description: if state is absent, the script remove member from replset else the script add member to replset
  login_host:
    required: false
    description: The host running the database
    default: localhost
  login_port:
    required: false
    description: The port to connect to.
    default: 27017
  login_user:
    required: true
    description: The username used to authenticate with
  login_password:
    required: true
    description: The password used to authenticate with
  member:
    required: true
    description: The host[:port] to add/remove from a replica set
  arbiter_only:
    required: false
    description: Should a new member be added as arbiter
    default: false
'''
from ansible.module_utils.basic import *
import subprocess

def replicaset_member_present(data):

    # check if the host is already a member in the replicaset
    # if true nothing to do is_error=flase, has_changed=false, result=host is already a member in the replicaset
    # else add member to replicaser is_error=false, has_changed=true, result=host added

    master_host  = data['login_host']
    master_login = data['login_user']
    master_pwd   = data['login_password']
    master_port  = data['login_port'] 
     
    host_to_add = data['member']
    is_arbiter = "false"
    if data['arbiter_only'] == True:
        is_arbiter = "true"
    else:
        is_arbiter = "false"

    out = subprocess.Popen(["mongo", master_host + ":" + str(master_port), "-u", master_login, "-p", master_pwd ,"--authenticationDatabase", "admin",   "--quiet", "--eval", "rs.status().members"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    value = stdout

    if value.find(host_to_add) >= 0:
        return False, False, {"status": "SUCCESS"}
    else:
        out_present = subprocess.Popen(["mongo", master_host +":"+ str(master_port), "-u", master_login, "-p", master_pwd ,"--authenticationDatabase", "admin",   "--quiet", "--eval", "rs.add('" + host_to_add + "', "+ is_arbiter +")"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout_present,stderr_present = out_present.communicate()
        value_present = stdout_present
        if value_present.find('"ok" : 0,') >= 0:
            return True, False, {"status": "FAILED"}
        else:
            return False, True, {"status": "SUCCESS"}
        return True, False, {"status": "Something goes wrong"}
   
def replicaset_member_absent(data):

    # check if the host is already a member in the replicaset
    # if flase nothing to do is_error=flase, has_changed=false, result=host is not a member in the replicaset
    # else remove member from replicaset is_error=false, has_changed=true, result=host removed

    master_host  = data['login_host']
    master_login = data['login_user']
    master_pwd   = data['login_password']
    master_port  = data['login_port']

    host_to_remove=data['member']

    out = subprocess.Popen(["mongo", master_host +":" + str(master_port), "-u", master_login, "-p", master_pwd ,"--authenticationDatabase", "admin",   "--quiet", "--eval", "rs.status().members"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    value = stdout

    if value.find(host_to_remove) >= 0:
        out_absent = subprocess.Popen(["mongo", master_host + ":" + str(master_port), "-u", master_login, "-p", master_pwd ,"--authenticationDatabase", "admin",   "--quiet", "--eval", "rs.remove('" + host_to_remove + "')"], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout_absent,stderr_absent = out_absent.communicate()
        value_absent = stdout_absent
        if value_absent.find('"ok" : 0,') >= 0:
            return True, False, {"status": "FAILED"}
        else:
            return False, True, {"status": "SUCCESS"}
        return True, False, {"status": "Something goes wrong"}
        
    else:
        return False, False, {"status": "SUCCESS"} 
    
def main():

    fields = {
        "login_host": {"required": False, "type": "str", "default": "localhost"},
        "login_port": {"required": False, "type": "int", "default": 27017},
        "login_user": {"required": True, "type": "str"},
        "login_password": {"required": True, "type": "str"},
        "member": {"required": True, "type": "str"},
        "arbiter_only": {"default": False, "type": "bool"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
        "present": replicaset_member_present,
        "absent":  replicaset_member_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error deleting repo", meta=result)


if __name__ == '__main__':
    main()