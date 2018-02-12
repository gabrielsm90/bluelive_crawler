# News Crawler


CONTINUOUS INTEGRATION SYSTEM

The Semaphore CI was used to run the application's tests on each push to Github
and also to keep track of what should be included on the requirements.txt file.

The Semaphore tool was picked mostly for its speed. The difference between building
and deploying with Semaphore and other popular tools sometimes is quite impressive.

On a scraping project that depends a lot on external facts such as internet speed,
these minutes can make real difference.

https://semaphoreci.com/

It is possible to include users on the project at Semaphore. If you already have
a user ou want to create one, don't hesitate on sending me the id so I can add
in the project.


LOCAL DEPLOYMENT OF THE APPLICATION

The application has two setup steps and two main processes:

1) Installing necessary python modules.
2) Setup. Cleaning the database.
3) Scraping Reddit page.
4) Running the web app that exposes the REST Services.

The commands for those three steps, assuming that the current
directory is the root of the project (bluelive_crawler) are:

1)
	ANY OPERATIONAL SYSTEM: pip install -r requirements.txt
	
2) 
	LINUX: python news_crawler/clean_database.py
	WINDOWS: python news_crawler\clean_database.py
	
3)
	LINUX: python news_crawler/scrape_data.py N (NUMBER OF PAGES THAT WILL BE SCRAPPED)
	WINDOWS: python news_crawler/scrape_data.py n (NUMBER OF PAGES THAT WILL BE SCRAPPED)
	
4)
	LINUX: python news_crawler/app.py
	WINDOWS: python news_crawler\app.py
	
	After this step, the application will be accessible at http://localhost:5000/
	

CLOUD DEPLOYMENT

Using semaphore, after each push to master branch on this repository and passing all the
tests, the application is deployed on a Heroku server.

The app is accessible in the following url:

https://blueliv-crawler.herokuapp.com/


APPLICATION DETAILS

For this project, I used Python 3.5 and the following main tools:

1) Scrapy framework to deal with the crawling. 
2) MongoDB as database, stored on Amazon Cloud, and pymongo framework to deal with it.
3) Flask framework to deal with REST Services.

The structure of the project is quite simple:

bluelive_crawler/
	
	README.md
	
	requirements.txt
	
	news_crawler/
	
		dao/
			mongo.py --> Responsible for reading and writing to the database
		
		scraper/ --> They see me scraping... They hating! Package following the Scrapy framework structure but on a simpler way, without using unnecessary configuration.
			item.py
			pipeline.py
			spider.py
			
		templates/
			index.html --> Just to expose the REST Services without having to necesarily build a client. The package follow Flask framework structure.
			
		test/ --> Test suit. Framework used for tests: pytest
			crawler_test.py
			mongo_test.py
		
		app.py --> Deployment of web app on local host.
		clean_database.py --> Auxiliar script that cleans the database on Amazon.
		scrape_data.py --> Scraping module. Invoked on command line with the number of pages that should be scraped as argument.
		
		
EVOLUTION OF THE WORK AND COMMIT HISTORY

Step by step. At start, the scraping was focus of development and to facilitate my tests and 
debugs, I used the whole Scrapy structure with it's configuration files, settings, fires and guns.

When the scraping was more mature, I started getting rid of unnecessary power and, with a 
easier to read structure, isolated the database access on one module (classic DAO pattern).

With Flask, the REST Services and welcome page.

The last part was just to complete the bonus queries.


GOALS

1) Every data is being scraped.
2) Results being persisted on MongoDB and REST API exposed. Top 10 submissions, by points and comments and classified in thre categories. All done.


BONUS

1) The information is updated. The application, before inserting data into the database tries to update an existing record. For that, it is considered
that if the submission has the same title and the author has the same name... Is the same one and will be updated.

2) Top submitters, top commenters and most active users are being retrieved and it is exposed as REST Service.

3) All posts by a user and all posts that a user commented are being brought. Just type the username on the welcome page and be happy.

4) I could not do this one. My complete failure on this project. Spent a few of the last hours analysing the pages and came to find out
that some of them ran out of pattern (example: Tafkas). This is definitely a case that I would be talking to my fellow coleagues to seek solutions.

5) Continuous Integration used to test and make sure the requirements.txt had all the necessary. With the scraping, helped me a lot
since the environment is amazingly fast. The Semaphore is yet small compared to it's similar tools (such as Jenkins or Hint) but I 
definitely suggest keeping an eye on that. Has been with me for a few months and I'm very pleased with that.
