Mediusware Task
# Tools
### Back-end
#### Language
	Python (3.9.0)

#### Frameworks:
	Django(4.0.6)
	django rest framework (3.13.1 )
	
#### Other libraries / tools:
	asgiref             3.5.2
	backports.zoneinfo  0.2.1
	django-cors-headers 3.13.0
	django-dotenv       1.4.2
	django-extensions   3.2.0
	drf-writable-nested 0.7.0
	pytz                2022.1
	setuptools          49.2.1
	sqlparse            0.4.2	

### Front-end
#### Language
	node (16.15.1)
	npm (8.11.0 )

####  Frameworks
	React (18.2.0)

# Setup
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/MahmudJewel/Simple-calculator.git
```
### Back-end
Create a virtual environment to install dependencies in and activate it:
```sh
$ cd src
$ python -m venv venv
$ source venv/bin/activate
```
Then install the dependencies:
```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver 8000
```

