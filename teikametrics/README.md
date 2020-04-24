Teikametrics is a project used to fetch data from github Api's.

Section (i):

It supports 3 functionalities:

1.) To fetch your 10 most recent commits through the url http://localhost:8000/get_recent_commits/
2.) To fetch the five most frequently used words in your commit messages, in descending order http://localhost:8000/most_frequent_words
3.) To fetch the the hour of day with the most commits http://localhost:8000/most_common_hour

Section (ii):

To set up the project, follow the following steps:

1.) Install virtualenv

2.) Set up an local environment by running the command: 
	virtualenv <virtual-environment-name>

3.) Now enter the virtualenv by running the commandin your terminal: 
	source <virtual-environment-name>/bin/activate 	

4.) Now clone the repo in the target folder and enter in the target folder directory.
	to clone the repo run the command: 
	git clone <repo_name>

5.) Now run the command: pip install -r requirements.txt

6.) Now go to your browser and type the following url:
	https://github.com/login/oauth/authorize?client_id=****your-client-id****&scope=repo
	NOTE: Replace ****your-client-id**** in above url with your client_id.

7.) On hitting the above Url you need to enter your github username and password in the prompt (if you are not logged in github earlier) and then authorize the app to use your credentials.

8.) Now hit the above urls(mentioned in Section (i)) and get the desired result.