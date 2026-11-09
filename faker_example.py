from faker import Faker

fake = Faker()

print(fake.name())         # Выведет: John Doe
print(fake.address())      # Выведет: 1234 Elm St, Springfield, IL
print(fake.email())        # Выведет: j.doe@example.com
