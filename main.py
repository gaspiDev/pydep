import argparse
import os
import toml


# Let's parse the arguments given in the command line.
parser = argparse.ArgumentParser(description="pydep.")
parser.add_argument("--path", type=str, default=".", help="Path of your Pipfile.")
parser.add_argument("--list", action="store_true", help="List all packages.")
parser.add_argument("--versionof", type=str, help="Version of the specified package.")
args = parser.parse_args() # Stores the args given as booleans.

# Check if a path of the pipfile was given otherwise try again.
if not args.path:
  print("You fool! Use the --path flag to navigate to your Pipfile directory.")
  exit()

# Store the directory of the app, so at the end we get back.
original_dir = os.getcwd()

# Now the main logic.
try:
  os.chdir(args.path) # Changes the directory to the path given in the arguments.

  if not os.path.exists("Pipfile"): # Search the Pipfile.
    print("Pipfile not found.")
    exit()

  with open("Pipfile", 'r') as file:
    config = toml.load(file)
    dependencies = config.get("packages", {}) # Read the dependencies.

  if args.list:
    print(dependencies)

  if args.versionof:
    version: str = dependencies[args.versionof]
    if version == "*":
      print(f"Version of {args.versionof} is not pinned.")
    else:
      print(f"{version[2:]}")

except toml.TomlDecodeError as e:
  print(f"Error decoding Pipfile: {e}")

except Exception as e:
  print(f"An unexcepted error occurred: {e}")

finally:
  os.chdir(original_dir)