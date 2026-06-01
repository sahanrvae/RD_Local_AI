import os

def process_user_orders(key, value, command, pattern):
    # bug fixes and type hints here
    pass

# generate files in the /src directory
os.makedirs(os.path.join('src', 'file1.txt'), exist_ok=True)
with open(os.path.join('src', 'file2.txt'), 'w') as f:
    f.write('')