# instagram page getting post

get and save a spacial instagram page's posts and showing in the website page and manage data in admin panel

<hr />

## getting start
* **migrate database** : running code for create database
> python manage.py makemigrations <br />
> python manage.py migrate
* **create superuser**: <br/>
create super user and login to admin panel with this comment
> python manage.py createsuperuser
* **adding instagram page address**: <br />
going to ***instagram pages*** section and create new instagram page model.
* **getting pages data**: now click on update post in posts list view and wait to done
* **view page data**: going to this routes to review data
> / <span style="color:grey">#view user list</span> <br />
> /posts <span style="color:grey">#posts list</span> <br />


### access to api
for view and use the api, you can going to this route and review api address.
> /api <span style="color:grey">#showing api endpoint</span> <br />
<hr> 

## installing package list
`pip install django`<br />
`pip install django-debug-toolbar`<br />
`pip install djangorestframework`<br />
`pip install instagrapi`<br />

### config
* **python version:** 3.8.9