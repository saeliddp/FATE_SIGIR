# Modifying and Hosting the Web Experiment
This is a Django web application. See https://docs.djangoproject.com/en/3.2/ for more information.

### Using your own data
1. Follow Workflow:2:c/d in README.md from the root directory.  
2. Open algorithms.txt. Line 1 is the algorithm deemed 'correct' for the first 10 queries. Line 2 is the algorithm deemed 'incorrect' for the first 10 queries. Line 3 is the algorithm deemed 'correct' for the last 10 queries. Line 4 is the algorithm deemed 'incorrect' for the last 10 queries. Replace these accordingly with your algorithm names (as reflected in names of txtdata files).  

### First time local setup
Steps 1-4 set up a local database. Steps 5-6 allow you to view the website locally.  
1. Run "python3 manage.py makemigrations"  
2. Run "python3 manage.py migrate"  
3. Run "python manage.py shell"  
4. In this shell prompt, type "import dbsetup" then "dbsetup.setup()" then "quit()"  
5. Run "python3 manage.py runserver"  
6. Navigate to your browser and enter localhost:8000 in your URL bar. If you HAVEN'T altered the .pickle file or anything in version2/txtdata, you will see google or not in your browser.  

### Creating a live version with Heroku
1. Create Heroku account and download Heroku CLI https://devcenter.heroku.com/articles/heroku-cli  
2. If you haven't already, create a git repository in the website directory ("git init"). Commit everything and push.  
3. While in website directory, run "heroku create <<name of your app>>"  
4. Open webapp2/settings.py. Add your new app URL to ALLOWED_HOSTS list. Commit this change and push to github. You can also turn off debug mode in settings.py if you wish.  
4. While in website directory, run "git push heroku"  
5. While in website directory, run "heroku run bash"--this will let you ssh into the server holding your live webapp.  
6. While in heroku bash, follow steps 1-3 from First time local setup above  

### Downloading user/response data
1. Simply type <<heroku url>>/export-users/ into your URL bar to download user data.  
2. Similarly, type <<heroku url>>/export-responses/ to download response data.  
3. You can replace <<heroku url>> with localhost:8000 to download from your local database.  
3. If you modify this system to store any sort of sensitive user information, please DISABLE these endpoints.
