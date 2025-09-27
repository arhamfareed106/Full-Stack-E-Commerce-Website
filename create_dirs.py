# Create static directories
import os

# Create directory structure
directories = [
    'app/static/images/products',
    'app/static/images',
    'app/static/js',
    'app/static/uploads',
    'app/templates/admin',
    'app/templates/checkout',
    'app/templates/custom',
    'app/templates/errors',
    'migrations'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("Directory structure created successfully!")