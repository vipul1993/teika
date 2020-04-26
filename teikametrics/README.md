Teikametrics is a project used to fetch data from github Api's.

Section (i):

It supports 3 functionalities:

1.) To fetch your 10 most recent commits through the url http://localhost:8000/get_recent_commits/
2.) To fetch the five most frequently used words in your commit messages, in descending order http://localhost:8000/most_frequent_words
3.) To fetch the the hour of day with the most commits http://localhost:8000/most_common_hour

Section (ii):

To set up the project, follow the following steps:

1.) Make sure to have python3 installed on your machine. You can achieve the same by running the following 			command in the terminal.
	i.) sudo add-apt-repository ppa:jonathonf/python-3.6
	ii.) sudo apt-get update
	iii.) sudo apt-get install python3.6

2.) Make sure you have the reuired python version by running over the command:
	python3 -v

3.) Install pip3 by using the following command:
	sudo apt-get install python3-pip

4.) Install virtualenv by using the command:
	sudo apt install virtualenv

5.) Now cd to the desired directory and set up an local environment by running the command: 
	virtualenv <virtual-environment-name> (In this case we can name <virtual-environment-name> to teika-venv).
		If the above command throws some error, then try running the below command.
	virtualenv <virtual-environment-name> -p python3	

6.) Now enter the virtualenv by running the command in your terminal: 
	source <virtual-environment-name>/bin/activate 	

7.) Now cd to the desired directory where you want to clone the repo and then run the following command: 
	git clone <repo_name> (In this it will be: https://github.com/vipul1993/teika.git )

8.) A new folder will be created in the current directory. cd to the directory by running the command:
	cd teikametrics

9.) Now run the command:
	pip install -r requirements.txt

10.) Open the file startup.sh in the current folder. 
	i.) Change the "****your_client_id****" to your_client_id
	ii.) Change the "****your_client_secret****" to your_client_secret
	iii.) Now open your terminal and run the following command:
		. ./startup.sh 
	NOTE: make sure your client_secret, client_id and an empty string gets printed in the terminal.	  	

11.) Now run the following command in the browser:
	i.) python manage.py makemigrations.
	ii.) python manage.py migrate
	iii.) python manage.py runserver	

12.) Now make sure your django server is running properly.	

13.) Now go to your browser and type the following url:
	https://github.com/login/oauth/authorize?client_id=****your-client-id****&scope=repo
	NOTE: Replace ****your-client-id**** in above url with your client_id.

14.) On hitting the above Url you need to enter your github username and password in the prompt (if you are not 	logged in github earlier) and then authorize the app to use your credentials.

15.) Now hit any of the above urls (mentioned in Section (i)) and get the desired result.