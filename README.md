# DITry
## A picture-sharing website

DITry is a web application that allows the user to upload pictures of his own creation, save ideas by other users in folders and follow other users. Its features are specified below.


## Features

- Users can login/ logout and depending on whether they are logged in or not, their access rights change
- Users can reset their password and receive an email with the link to reset it
- Users can upload a picture as a posts, upload attempts of other posts and save other posts to folders
- They can follow users and categories
- Users can like a post
- Users can view posts in one of the three predefined categories (food, DIY, crafts)
- Users can view the top ten liked posts by clicking on 'trending'


## Run DITry
After installing everything needed, you can now run the project by doing the following:
Navigate to the folder, where the project is saved at:

````
cd <your_path>/ditry_project
````
The correct order of the following steps is crucial!

````
python manage.py migrate

python manage.py makemigrations

python manage.py migrate

````
The following steps are not mandatory, but the order they need to be ran is still crucial. (that means you can choose to run both commands, one-one command, or neither only the order matters):
````
python population_script.py

python manage.py createsuperuser
````
Finally:
````

python manage.py runserver
````
Now, copy the link into the link into your browser to start the server.
(The link should look like this:)
```
http://127.0.0.1:8000/
```

## Notes
- To register on the page, creating a superuser does not work as it does not create a user profile. Instead, you need to use the register functionality on the website

## External sources
- https://stackoverflow.com/questions/38006125/how-to-implement-search-function-in-django (last accessed: 16.03.2022)
- https://github.com/Jebaseelanravi/instagram-clone/blob/main/insta/views.py   (last accessed: 16.03.2022, used to create like_post view)
- https://stackoverflow.com/questions/28764571/display-image-from-imagefield-by-means-of-for (last accessed: 24.03.2022)
- https://stackoverflow.com/questions/524992/how-to-implement-a-back-link-on-django-templates (last accessed: 24.03.2022)

##
Web Application development project repo - team 9D

