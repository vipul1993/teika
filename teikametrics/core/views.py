import requests 
import datetime
import os
import json
import subprocess

#library import for using multithreading
import concurrent.futures

from django.http import HttpResponse

# library import for parsing callback url
from urllib.parse import urlparse

# Function for doing remote Github API calls.

def api_call(url, method="get", params=None, header=None):

	if method == 'get':
		try:
			response = requests.get(url = url, params = params, headers = header)
		except Exception as exc:
			return ({
			'success': False,
			'error': exc})
		return ({
			'success': True,
			'data': response,
		})	

	elif method == "post":
		try:
			response = requests.post(url = url, data = params, headers = header)
		except Exception as exc:
			return ({
			'success': False,
			'error': exc})
		return ({
			'success': True,
			'data': response,
		})	

# Function to get the access token. 

def get_access_token(code):

	url_access_token = "https://github.com/login/oauth/access_token"

	params = {
		"client_id" : os.environ.get('teika_client_id'),
		"client_secret" : os.environ.get('teika_client_secret'),
		"code" : code,
	}

	header = {
		"Accept": "application/json",
	}

	response = api_call(url_access_token, method="post", params=params, header=header)
	if response['success'] == True:
		response_access_token = response['data'].json()
		access_token = response_access_token["access_token"]
		# print (access_token)
		env = dict(os.environ)
		ansrun='/share/ansa/NOT_RELEASED/14.2.2/ansa64.sh'
		env['teika_access_token'] = str(access_token)
		subprocess.Popen(ansrun, shell=True, env=env)
		print ("******************", os.environ.get('teika_client_id'))

		header['Authorization'] = 'token {}'.format(access_token)
		return ({
			'success':True,
			'data': access_token
			})
	else:
		return ({
			'success': False,
			'error': response['error']
			})
		

# Function to get the authorizatin code.

def get_auth_code(request):
	# import pdb; pdb.set_trace()
	url_authorization = "https://github.com/login/oauth/authorize"
	params = dict()
	params['client_id'] = client_id_test
	params['scope'] = "repo"
	# params['redirect_uri'] = "https://localhost:8000/path"
	try:
		response_auth_code = api_call(url_authorization, params=params)
	except Exception as e:
		return e
	else:	
		return HttpResponse()

# Function to get all the commits from a repo for a particular user.

def get_commit_from_repo(repo):

	owner = str(repo["owner"]["login"])
	repo = str(repo["name"])
	commits = list()

	url_user_repo_commits = "https://api.github.com/repos/{}/{}/commits".format(owner, repo)

	params = dict()
	url_user_username = "https://api.github.com/user"
	response_user_username = api_call(url_user_username, header={'Authorization': 'token {}'.format(os.environ.get('teika_access_token'))})
	params["author"] = response_user_username['login']

	response_commits = api_call(url_user_repo_commits, params=params, header=global_header).json()
	len_response_commits = len(response_commits)

	if len_response_commits != 0:

		for j in range(len_response_commits):
			time = datetime.datetime.strptime(response_commits[j][u'commit'][u'author'][u'date'], '%Y-%m-%dT%H:%M:%SZ')
			message = str(response_commits[j][u'commit'][u'message'])
			commits.append((time, message))
	return commits

# Function to hit the api from github to fetch all the repos of a user.

def main():

	url_user_repos = "https://api.github.com/user/repos"

	header = dict()

	access_token = os.environ.get('teika_access_token')

	header['Authorization'] = "token {}".format(access_token)

	try:
		all_commits = list()
		i = 0 
		len_response_repos = 0
		no_of_commits = 0

		response_repos = api_call(url_user_repos, header=header).json()
		len_response_repos = len(response_repos)

		# Multithreading to hit the github API's concurrently for time optimization. 

		while len_response_repos > 0:
			if len_response_repos < 5:
				with concurrent.futures.ThreadPoolExecutor(max_workers=len_response_repos) as executor:
					# Start the load operations and mark each future with its URL
					future_to_url = {executor.submit(get_commit_from_repo, repo): repo for repo in response_repos[i:]}
					for future in concurrent.futures.as_completed(future_to_url):
						url = future_to_url[future]
						try:
							data = future.result()
							all_commits.extend(data)
						except Exception as exc:
							print('%r generated an exception: %s' % (url, exc))
						else:
							print('%r page is %d bytes' % (url, len(data)))
				len_response_repos = 0
				i += len_response_repos


			else:
				with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
					# Start the load operations and mark each future with its URL
					future_to_url = {executor.submit(get_commit_from_repo, repo): repo for repo in response_repos[i:i+5]}
					for future in concurrent.futures.as_completed(future_to_url):
						url = future_to_url[future]
						try:

							data = future.result()
							all_commits.extend(data)
						except Exception as exc:
							print('%r generated an exception: %s' % (url, exc))
						else:
							print('%r page is %d bytes' % (url, len(data)))
				len_response_repos -= 5
				i += 5
	except Exception as exc:
		return ({
			"success":False,
			"error": exc
			})

	all_commits.sort(reverse=True)
	no_of_commits = len(all_commits)

	return ({
		'success': True,
		'all_commits': all_commits,
		'no_of_commits': no_of_commits
		})

# API for finding the top 10 recent commits.

def top_10_recent_commits(request):
	# import pdb; pdb.set_trace()
	print (os.environ.get('teika_access_token'))
	# access_token = str(os.environ._data[b'teika_access_token'])
	access_token = os.environ.get('teika_access_token')
	
	if access_token is not None and access_token is not '':
		result = main()
		if result['success'] is True:

			all_commits = result['all_commits']
			no_of_commits = result['no_of_commits'] 

			if no_of_commits < 10:
				top_ten_messages = all_commits
			else:	
				top_ten_messages = all_commits[:10]

			commit_messages = [message[1] for message in top_ten_messages]

			return HttpResponse(json.dumps({
				'success':True,
				'data': commit_messages
				}))
		else:
			
			return HttpResponse(json.dumps({
				'success': False,
				'error': result['error']
				}))	
	else:
		return HttpResponse(json.dumps({
			'success': False,
			'error': "Access token not present",
			}))		

# API for finding the 5 most frequently used words in decending order.

def most_frequently_used(request):	

	access_token = os.environ.get('teika_access_token')
	if access_token is not None and access_token is not '':
		result = main()
		if result['success'] == True:

			dic_words = dict()
			messages = list()

			all_commits = result['all_commits']
			no_of_commits = result['no_of_commits'] 

			for i in range(no_of_commits):
			 
				message = all_commits[i][1].split(" ")
				
								
				for word in message:
					if word in dic_words:
						dic_words[word] += 1
					else:
						dic_words[word] = 1

			sorted_dic_words = sorted(dic_words.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
				
			sorted_dic_words = sorted_dic_words[:5]

			return HttpResponse(json.dumps({
				'success': True, 
				'data': sorted_dic_words
				}))
		else:
			
			return HttpResponse(json.dumps({
				'success': False,
				'error': result['error']
				}))	
	else:
		return HttpResponse(json.dumps({
			'success': False,
			'error': "Access token not present",
			}))		

# API for finding the hour of day with the most commits.

def time_of_the_hour(request):

	access_token = os.environ.get('teika_access_token')
	if access_token is not None and access_token is not '':
		result = main()
		if result['success'] == True:

			dic_hour = dict()
			datetime_obj = list()
			
			all_commits = result['all_commits']
			no_of_commits = result['no_of_commits'] 

			for i in range(no_of_commits):

				datetime_obj = all_commits[i][0]

				if datetime_obj.hour in dic_hour:
					dic_hour[datetime_obj.hour] += 1
				else:
					dic_hour[datetime_obj.hour] = 1	

			max_hit_words = max(dic_hour, key=dic_hour.get)

			return HttpResponse(json.dumps({
				'success': True,
				'data': max_hit_words})
				)
		else:
			
			return HttpResponse(json.dumps({
				'success': False,
				'error': result['error']
				}))	
	else:
		return HttpResponse(json.dumps({
			'success': False,
			'error': "Access token not present",
			}))		

# Function for listenig to the callback urls.

def callback_url(request):
	
	parse = urlparse(request.get_full_path())
	code = parse.query.split("=")[1]
	response = get_access_token(code)
	if response['success'] == True:
		return HttpResponse(json.dumps({
			'success': True, 
			'access_token':response['data']
			}))
	else:
		return HttpResponse(json.dumps({
			'success': False,
			'error': response['error']
			})) 		