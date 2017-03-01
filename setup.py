import os
import sys
import fnmatch
import subprocess
from setuptools import setup
from shutil import copytree, rmtree, copy


# Determine the absolute PATH of the CMarkEd folder
PATH = os.path.dirname(os.path.realpath(__file__))

# Make a copy of the src tree (temporary for naming reasons only)
if os.path.exists(os.path.join(PATH, "src")):
    print("Copying modules to cmarked directory: %s" % os.path.join(PATH, "cmarked"))
    # Only make a copy if the SRC directory is present (otherwise ignore this)
    copytree(os.path.join(PATH, "src"), os.path.join(PATH, "cmarked"))

if os.path.exists(os.path.join(PATH, "cmarked")):
    # Append path to system path
    sys.path.append(os.path.join(PATH, "cmarked"))
    print("Loaded modules from cmarked directory: %s" % os.path.join(PATH, "cmarked"))

from main import __version__

SETUP = {
    "name":  'CMarkEd',
    "version":  __version__,
    "description":  'A multi platform CommonMark (Markdown) editor',
    "author":  'Sergio de la Cruz, Armando Pereda',
    "author_email":  'sergiodlc@gmail.com, armando.p.labrador@gmail.com',
    "url":  'https://github.com/sergiodlc/cmarked',
    "license":  'MIT',
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Text Editors",
        "Topic :: Text Processing :: Markup",
    ],
}

# Boolean: running as root?
ROOT = os.geteuid() == 0
# For Debian packaging it could be a fakeroot so reset flag to prevent execution of
# system update services for Mime and Desktop registrations.
# The debian/cmarked.postinst script must do those.
if not os.getenv("FAKEROOTKEY") == None:
    print("NOTICE: Detected execution in a FakeRoot so disabling calls to system update services.")
    ROOT = False

os_files = [
    # XDG application description
    ('share/applications', ['xdg/cmarked.desktop']),
    # XDG application icon
    ('share/pixmaps', ['xdg/cmarked.svg']),
]

# Find files matching patterns
def find_files(directory, patterns):
    """ Recursively find all files in a folder tree """
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if ".pyc" not in basename and "__pycache__" not in basename:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename


package_data = {}

# Find all project files
src_files = []
for filename in find_files(os.path.join(PATH, "cmarked"), ["*"]):
    src_files.append(filename.replace(os.path.join(PATH, "cmarked"), ""))
package_data["cmarked"] = src_files

# Call the main Distutils setup command
# -------------------------------------
dist = setup(
    packages=['cmarked', 'cmarked.ui'],
    package_data=package_data,
    data_files=os_files,
    include_package_data=True,
    # Automatic launch script creation
    entry_points = {
        "gui_scripts": [
            "cmarked = cmarked.launch:main"
        ]
    },
    **SETUP
)
# -------------------------------------

# Remove temporary folder (if SRC folder present)
if os.path.exists(os.path.join(PATH, "src")):
    rmtree(os.path.join(PATH, "cmarked"), True)

FAILED = 'Failed to update.\n'

if ROOT and dist != None:
    # update the XDG .desktop file database
    try:
        sys.stdout.write('Updating the .desktop file database.\n')
        subprocess.call(["update-desktop-database"])
    except:
        sys.stderr.write(FAILED)
    sys.stdout.write("\n-----------------------------------------------")
    sys.stdout.write("\nInstallation Finished!")
    sys.stdout.write("\nRun CMarkEd by typing 'cmarked' or through the Applications menu.")
    sys.stdout.write("\n-----------------------------------------------\n")
