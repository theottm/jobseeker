import os
from configparser import ConfigParser, DuplicateSectionError

from programms.utils.utils import get_project_root

project_root = get_project_root()

# define config file
config = ConfigParser()
config_path = os.path.join(project_root, "config.ini")
config.read(config_path)
try:
    config.add_section("general")
    config_status = "Creating config file"
except DuplicateSectionError:
    config_status = "Updating config file"

# Add project root 
config.set("general", "project_root", project_root)
print(f"Root : {project_root}")

# Add user
try:
    user = config["general"]["user"]
    print(f"User : {user}")
except KeyError:
    user = input("Please enter a user name : ")
    config.set("general", "user", user)
    print("Creating your profile ...")
    try:
        os.mkdir(os.path.join(project_root, "data", config["general"]["user"]))
    except FileExistsError:
        pass
    print(f"Welcome on board, {user} !")

print(f"{config_status}...")
with open(config_path, 'w') as config_file:
    config.write(config_file)
print(f"Done.")
    
# 
programms = []
exclude_dirs = set(["indeed", "utils"])
exclude_files = ["__init__.py", __file__, "status.py"]
for root, dirs, files in os.walk(get_project_root()):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith(".py") and not any(x in file for x in exclude_files):
            programms.append(file)

print("Programms : {}".format(", ".join([programm for programm in programms])))
