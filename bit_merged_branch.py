#!/usr/bin/env python
import requests
import json
import sys

try:
    username = sys.argv[1]
    password = sys.argv[2]
    bitbucket_url = sys.argv[3]
    project_key = sys.argv[4]
    headers = {'Content-Type': 'application/json'}
except:
    print("usage: ./bit_merged_branch.py username password bitbucket_url project_key")
    sys.exit(1)

def search_branches():
    branch_list = []
    # Search all repositories in project
    repos_url = '{}/rest/api/1.0/projects/{}/repos'.format(bitbucket_url,project_key)
    repos_requests = requests.get(repos_url, auth=(username, password), headers=headers)
    repos_json = repos_requests.json()
    for repos in repos_json['values']:
        repo = repos['slug']
        # Search all merged pull requests
        pull_requests_url = '{}/rest/api/1.0/projects/{}/repos/{}/pull-requests?state=MERGED'.format(bitbucket_url, project_key, repo)
        # Search all existed branches
        branch_url = '{}/rest/api/1.0/projects/{}/repos/{}/branches'.format(bitbucket_url, project_key, repo)
        pull_requests = requests.get(pull_requests_url, auth=(username, password), headers=headers)
        branch_requests = requests.get(branch_url, auth=(username, password), headers=headers)
        pull_requests_json = pull_requests.json()
        branch_requests_json = branch_requests.json()
        for values in pull_requests_json['values']:
            branch = (values['fromRef']['id'])
            repository = (values['fromRef']['repository']['slug'])
            for branches in branch_requests_json['values']:
                branches_exist = branches['id']
                # Check exsiting branch
                if branch == branches_exist:
                    url_branch_dict = dict()
                    url_branch_dict['url'] = '{}/rest/branch-utils/1.0/projects/{}/repos/{}/branches/'.format(bitbucket_url, project_key, repository)
                    url_branch_dict['branch_name'] = {"name": branches['id']}
                    branch_list.append(url_branch_dict)
    return branch_list

def main():
    branch_list = search_branches()
    branch_for_del = []
    # Check list of branches is not empty
    if not branch_list:
        print("No branches")
    # Show merged branches and delete if you choose it
    else:
        print('Names all merged branches')
        for branch in branch_list:
            branch_for_del.append(branch['branch_name'])
        print(branch_for_del)
        sys.stdout.write("Delete merged branches?")
        choice = input().lower()
        if choice == 'yes' or choice == 'y':
            for url_branch in branch_list:
                requests.delete(url_branch['url'], data=json.dumps(url_branch['branch_name']), auth=(username, password), headers=headers)
            print("All branches was deleted")
        elif choice == 'no' or choice == 'n':
            print('Ok! Bye!')
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' ""(or 'y' or 'n').\n")


if __name__ == '__main__':
    main()