from faker import Faker
import random
from datetime import datetime
import csv

# Initialize Faker
fake = Faker()

# Generate timestamp for filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"/data/data_gen/staging/{timestamp}.log"

cur_date = datetime.now().strftime("%Y%m%d")
cur_time = datetime.now().strftime("%H%M%S")


# Define number of records
num_records = 10000

# Define field names
fields = [
    "name", "address", "city", "country", "job",
    "passport_number", "date_of_birth", "date", "time", "random_number"
]

# Write data to file
with open(filename, "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(fields)  # Write header
    for _ in range(num_records):
        row = [
            fake.name(),
            fake.address().replace("\n", ", "),
            fake.city(),
            fake.country(),
            fake.job(),
            fake.passport_number(),
            fake.date_of_birth(),
            cur_date,
            cur_time,
            random.randint(1000, 9999)
        ]
        writer.writerow(row)

print(f"Generated {num_records} fake records and saved to {filename}.")
