# Mediusware Task
## Tools
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

## API ROUTES
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *GET* | ```/product/api/all-products/``` | _Get all products_| _All users_|
| *PUT* | ```/product/api/edit/<id>/``` | _Update product_|_Admin users_|
| *POST* | ```/product/api/all-products/``` | _Create new product_|_Admin users_|
| *GET* | ```/product/api/edit/<id>/``` | _Get single product_|_Admin users_|



# Setup
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/MahmudJewel/MW/tree/dev.1.0.0
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

# Screenshot
### Product List
![ Product List](https://github.com/MahmudJewel/MW/blob/dev.1.0.0/screenshot/0-product%20list.jpg)

### Filter Page
![Filter Page](https://github.com/MahmudJewel/MW/blob/dev.1.0.0/screenshot/1-filter.jpg)

### Create Product
![Ceate Product](https://github.com/MahmudJewel/MW/blob/dev.1.0.0/screenshot/3-Create%20product.jpg)

### Edit Product
![ Edit Product](https://github.com/MahmudJewel/MW/blob/dev.1.0.0/screenshot/5-api-edit%20product.jpg)
