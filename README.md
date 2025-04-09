# Building a Bookmarks Application

This repository contains the 2nd project from the "Django 5 by Example" book, along with my enhancements.

## Enhancements

1. **Best Practices & Custom User Model:**  
   Adheres to strict naming conventions and best coding practices. The `CustomUser` model extends `AbstractUser`, integrating profile fields directly.

2. **Image Bookmarking & Access Control:**  
   Image titles and alt attributes are automatically extracted and editable when bookmarking. Users can only view images from accounts they follow and can only edit their own bookmarked images.

3. **User Restrictions & Cleanup:**  
   Users can't follow themselves, and their own images are excluded from other users' profiles. When a user deletes their account, all associated images and folders are automatically removed.

4. **SEO, Security, & URL Structure:**  
   User URLs combine slugs (based on usernames) with UUIDs for improved SEO and security.

## Future Enhancements

1. **Authentication & Bookmarking Improvements:**  
   Plans to expand authentication methods and enhance the image bookmarking experience with new features.

2. **View Tracking & API Development:**  
   Image view counts will be tracked for better engagement analytics, while a robust API will provide flexibility for future integrations.

3. **Responsive Design & Error Handling:**  
   The UI will be optimized for responsiveness, with custom error pages for an improved user experience.

4. **Commenting System & Social Media Sharing:**  
   Users will be able to comment on images (with permissions) and share images on social media to boost engagement.

5. **Testing & Dockerization:**  
   Unit and integration tests will ensure stability, and the project will be containerized using Docker to streamline deployment and enhance scalability.

## Project Setup

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/muhammadgalhoum/bookmarks
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
On macOS/Linux:
python3 -m venv env
On Windows:
python -m venv env
```

### 3. Activate the Virtual Environment

```bash
On macOS/Linux:
source env/bin/activate
On Windows:
.\env\Scripts\activate
```

### 4. Install the Required Dependencies

Install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

Run migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)

Create a superuser to access the Django Admin interface:

```bash
python manage.py createsuperuser
You will be prompted to enter a username, email, and password for the superuser account.
```

### 7. Run the Redis Server

Start the Redis server after make sure that you have docker on your machine:

```bash
docker run -it --rm --name redis -p 6379:6379 redis
```

### 7. Run the Development Server

There two cases:

-1 Run the server using runserver_plus so you can sign in using Google account and before that you should locate the hosts file of your machine. If you are using Linux or macOS, the hosts file is located at /etc/hosts. If you are using Windows, the hosts file is located at C:\Windows\System32\Drivers\etc\hosts.
Edit the hosts file of your machine and add the following line to it:
127.0.0.1 mysite.com
This will tell your computer to point the mysite.com hostname to your own machine.

```bash
python manage.py runserver_plus mysite.com:8000 --cert-file cert.crt
```

-2 Run the server using runserver but you will not be able to sign in using Google account.

```bash
python manage.py runserver
```

### Important Note

Create a .env file in the main directory of the project and add the following variables with their respective values:

```bash
GOOGLE_OAUTH2_KEY=
GOOGLE_OAUTH2_SECRET=
```
