from django.core.management.base import BaseCommand
from auctions.models import User, Listing
import json
import os


def json_reader(file_path):
    # Read JSON data from file
    with open(file_path, "r") as stream:
        data = json.load(stream)
    return data


def insert_listings(self, data):
    try:
        for item in data:
            title = item["title"]
            description = item["description"]
            starting_bid = item["starting_bid"]
            image_url = item["image_url"]
            author = User.objects.get_by_natural_key(item["author"])
            listing = Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                author=author,
            )
            listing.save()
            self.stdout.write(self.style.SUCCESS(f"Created lisiting: '{title}'"))
        self.stdout.write(self.style.SUCCESS("LISTINGS seeding completed."))
    except Exception as err:
        self.stdout.write(self.style.ERROR("An error occurred:", err))


def insert_users(self, data):
    try:
        for item in data:
            username = item["username"]
            email = item["email"]
            password = item["password"]
            is_superuser = item.get(
                "is_superuser", False
            )  # second argument is the fallback value
            if is_superuser:
                User.objects.create_superuser(username, email, password)
                self.stdout.write(
                    self.style.SUCCESS(f"Created superuser: '{item['username']}'")
                )
            else:
                User.objects.create_user(username, email, password)
                self.stdout.write(
                    self.style.SUCCESS(f"Created user '{item['username']}'")
                )
        self.stdout.write(self.style.SUCCESS("USERS seeding completed."))
    except Exception as err:
        self.stdout.write(self.style.ERROR("An error occurred:", err))


integrator_switch = {"users.json": insert_users, "listings.json": insert_listings}


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the JSON file
        seed_data_dir = os.path.join(script_dir, "../seed_data")
        data_file_names = os.listdir(seed_data_dir)
        for data_file_name in data_file_names:
            if data_file_name not in integrator_switch:
                raise Exception(f"{data_file_name} file doesn't belong to seed data")
            integrator_func = integrator_switch[data_file_name]
            if not callable(integrator_func):
                raise Exception(
                    f"Integrator function for {data_file_name} is not callable"
                )
            json_file_path = os.path.join(seed_data_dir, f"{data_file_name}")
            data = json_reader(json_file_path)
            # Process and insert data into the database
            integrator_func(self, data)

        self.stdout.write(self.style.SUCCESS("DATABASE seeding completed."))
