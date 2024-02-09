import os
import sys
import django
import json

def setup_django_environment():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the parent directory of the script's directory to the Python path
    sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))

    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')
    django.setup()

    # Import Django models after setting up the environment
    from auctions.models import User

    # Construct the path to the data file relative to the script directory
    users_file_path = os.path.join(script_dir, 'seed_data', 'users.json')
    return User, users_file_path

def json_reader(file_path):
    # Read JSON data from file
    with open(file_path, 'r') as stream:
        data = json.load(stream)
    return data

def insert_users(User, data):
    try:
        for item in data:
            username = item['username']
            email = item['email']
            password = item['password']
            User.objects.create_user(username, email, password)
            print(f"Created: {item}")
        print("Data inserted successfully!")
    except Exception as err:
        print("An error occurred:", err)

def main():
    User, users_file_path = setup_django_environment()
    data = json_reader(users_file_path)
    insert_users(User, data)

if __name__ == "__main__":
    main()