import urllib.request, json
from urllib.error import HTTPError
import sys
import json

def main():
    #take username as arg
    username = sys.argv[1]
    json_list = request(username)
    return_lists = data_sort(json_list)
    text_output(return_lists[0],return_lists[1],return_lists[2], username,return_lists[3])

def request(username):
    #read in the events from the github api and return to main
    url = f'https://api.github.com/users/{username}/events'
    try:
        with urllib.request.urlopen(url) as url:
            json_list = json.load(url)
    #error handling for invalid username
    except HTTPError:
        print('Invalid username')

    return json_list

def data_sort(json_list):
    #receive data and process it into 4 variables to be returned to main
    i = 0
    entries = len(json_list)
    repo_list = []
    commit_num = 0
    issues_closed_num = 0

    while i < entries:
        #the api is read in as a list of dictionaries, we use this while loop to run through each dictionary
        json_dict = json_list[i]
        if json_dict['type'] == 'PushEvent':
            commit_num += 1
            repo_list.insert(i, json_dict['repo']['name'])
        elif json_dict['type'] == 'IssuesEvent' and json_dict['payload']['action'] == 'closed':
            issues_closed_num += 1
        i +=1
    #convert the list into a set, sets do not display duplicate values
    repo_set = set(repo_list)

    return commit_num, issues_closed_num, repo_set, entries

def text_output(commit_num, issues_closed_num, repo_set, username, entries):
    #displaying statistics gathered
    print(f'\nThe user {username} has the following statistics for the last {entries} events')
    print(f'They have commited {commit_num} times to the following repos: {repo_set}')
    print(f'They have closed {issues_closed_num} issues')

if __name__ == "__main__":
    main()