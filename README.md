### INF601 - Advanced Programming in Python
### Daniel Terreros
### Final Project

'''
INF601 - Programming in Python
Assignment Final Project
I,     Daniel Terreros    , affirm that the work submitted for this assignment is entirely my own. I have not engaged in 
any form of academic dishonesty, including but not limited to cheating, plagiarism, or the use of unauthorized materials.
I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence to academic
standards. I understand that failing to comply with this integrity statement may result in consequences,
including disciplinary actions as determined by my course instructor and outlined in institutional policies.
By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.
'''


## Description

This project uses Django to look up the user's location and display the weather. It also includes a login system, a profile page
for the user, and a pages that will help the user decide what to wear based on the weather/what to do based on the weather.

## Getting Started

# There is a file named API_KEY2 that is currently blank. I have attached my API for openweathermap in my submission to blackboard.
## You will need to copy that string as is and paste it into the API_KEY2 file.

### Dependencies

```
pip install -r requirements.txt
```

### Initializing the Database

Before running the project, you need to set up the database:

1. **Create migration files**  
   This command creates SQL entries for any changes in your models:
```
python manage.py makemigrations
```

2. **Apply the migrations**  
This command applies the generated migrations to your database:
```
python manage.py migrate
```
3. **Create a superuser**  
This command sets up an administrator account for the Django admin site:
```
python manage.py createsuperuser
```

Follow the prompts to create your admin user.

### Running the Development Server

Once the database is set up, you can run the development server with:
```
python manage.py runserver
```



Then, open your browser and navigate to:
http://127.0.0.1:8000

# WHEN CREATING A USER YOU MUST HAVE A NINE CHARACTER LONG PASSWORD MINIMUM

### Notable additions
*Sign up and registrations using Django's built-in auth.
*Fully responsive design
*Daisy UI for some components.
*Tailwind CSS for styling; using tailwind components for UI
*Zipcode lookup using the OpenWeatherMap API
*Fully responsive design
*Based on weather conditions, temperature, and uv index, the user will be given suggestions on what to wear and what to do.
*A basic user profile
*Fair Use Images
*Pytz Library for timezone conversion
*A dynamic favicon that changes based on the weather



## Author

Daniel Terreros

## Acknowledgements
* [Daisy UI with TailwindCLI](https://https://daisyui.com/docs/install/django/)
* [Three Column Bento Grid From Tailwind CSS](https://tailwindcss.com/plus/ui-blocks/preview)
* [Tailwind Sign up and Registration inspiration](https://tailwindcss.com/plus/ui-blocks/application-ui/forms/sign-in-forms)
* [Stacked lists with Tailwind that were used for clothing and activity suggestions](https://tailwindcss.com/plus/ui-blocks/application-ui/lists/stacked-lists)
* [How to install Pytz in Python](https://www.geeksforgeeks.org/how-to-install-pytz-in-python/)
* [More help with Pytz](https://www.youtube.com/watch?v=3B5oInYNb5c)
* [Double underscores and Djangos ORM](https://stackoverflow.com/questions/21319832/what-do-double-underscores-indicate)
* [The origin of the dynamic favicon](https://www.geeksforgeeks.org/how-to-change-favicon-dynamically/)
* [Inspiration for initial development with open weather api](https://www.youtube.com/watch?v=lyeK0aE_qRg)
* [Claude helping me identify that tailwind was blocking using default form rendering.](https://claude.ai/share/4f41c908-c901-4efe-ad79-fbe7b50b716f)
* [Claude identifying why "What to do" wasn't showing anything to do and issues with a photo](https://claude.ai/share/da423f6d-539a-473f-b43e-54ea72d4fdc3)
* [Previous django project from a while ago that helped me remember how to do some of this stuff!](https://github.com/DanielTKC/current_club)
* For reference, there is a php file that I also used from a previous project that I used to help me with the API calls.
