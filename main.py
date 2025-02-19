import argparse
import os
import sys
import toml
import subprocess


# Parse the arguments given.
parser = argparse.ArgumentParser(description="pydep.")
parser.add_argument("--path", "-p", type=str, help="Path of your Pipfile.")
group = parser.add_mutually_exclusive_group()
group.add_argument("--list", "-l", action="store_true", help="List all packages.")
group.add_argument(
    "--versionof", "-vo", type=str, help="Version of the specified package."
)
group.add_argument("--add", "-a", type=str, help="Name of the package to install.")
group.add_argument(
    "--update_all",
    "-ua",
    action="store_true",
    help="Update all packages to the last version.",
)
group.add_argument("--remove", "-r", type=str, help="Name of the package to uninstall.")
group.add_argument(
    "--check_outdated",
    "-co",
    action="store_true",
    help="Check fpr new updates on dependencies packages.",
)
group.add_argument(
    "--graph", "-g", action="store_true", help="Shows dependencies tree."
)


args = parser.parse_args()  # Stores the args given as booleans.

# Check if a path of the pipfile was given otherwise try again.
if not args.path:
    print("Must use the --path flag to navigate to your Pipfile directory.")
    sys.exit()

# Check of any option was given...
elif (
    not args.list
    and not args.versionof
    and not args.add
    and not args.update_all
    and not args.remove
    and not args.check_outdated
    and not args.graph
):
    print("At least one flag must be used besides --path/-p")
    sys.exit()
# Store the directory of the app, so at the end we get back.
original_dir = os.getcwd()

# Changes the directory to the path given in the arguments.
try:
    os.chdir(path=args.path)
except FileNotFoundError:
    print(f"The path {args.path} doesn't exist.")
    sys.exit()

# Now the main logic.
try:
    with open("Pipfile", "r") as file:
        config = toml.load(file)
        dependencies = config.get("packages", {})  # Read the dependencies.

    # List all packages.
    if args.list:
        print(dependencies)

    # Print version of specified package
    elif args.versionof:
        version = dependencies[args.versionof]
        if version == "*":
            print(f"Version of {args.versionof} is not pinned.")
            print(f"Version of {args.versionof} is not pinned.")
        elif isinstance(version, dict):
            print(version["version"][2:])
        else:
            print(f"{version[2:]}")

    # Add a package to the dependencies.
    elif args.add:
        subprocess.run(args=["pipenv", "install", args.add], cwd=args.path)

    # Update all packages to last stabel version.
    elif args.update_all:
        subprocess.run(args=["pipenv", "update"], cwd=args.path, check=True)

    # Remove a package from the dependencies.
    elif args.remove:
        subprocess.run(args=["pipenv", "uninstall", args.remove], cwd=args.path)

    elif args.check_outdated:
        subprocess.run(args=["pipenv", "update", "--outdated"], cwd=args.path)

    elif args.graph:
        subprocess.run(args=["pipenv", "graph"], cwd=args.path)

except toml.TomlDecodeError as e:
    print(f"Error decoding Pipfile: {e}")

except FileNotFoundError as e:
    print(
        """Pipfile not found.
        \nIf you want to activate a Pipenv do the following:
        \n1. Deactivate any active virtual enviorment.
        \n2. Change directory with cd to the desired directory.
        \n3. Run pipenv shell for creating the virtual enviorment."""
    )

except Exception as e:
    print(f"An unexcepted error occurred: {e}")

finally:
    os.chdir(original_dir)
    sys.exit()
