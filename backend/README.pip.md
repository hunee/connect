#
# https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
#

# Use pip for Installing

pip is the recommended installer. Below, we’ll cover the most common usage scenarios. For more detail, see the pip docs, which includes a complete Reference Guide.

# Installing from PyPI
The most common usage of pip is to install from the Python Package Index using a requirement specifier. Generally speaking, a requirement specifier is composed of a project name followed by an optional version specifier. PEP 440 contains a full specification of the currently supported specifiers. Below are some examples.

To install the latest version of “SomeProject”:

$ python3 -m pip install "SomeProject"


To install a specific version:

$ python3 -m pip install "SomeProject==1.4"


To install greater than or equal to one version and less than another:

$ python3 -m pip install "SomeProject>=1,<2"


To install a version that’s “compatible” with a certain version: 4

$ python3 -m pip install "SomeProject~=1.4.2"


In this case, this means to install any version “==1.4.*” version that’s also “>=1.4.2”.

# Source Distributions vs Wheels
pip can install from either Source Distributions (sdist) or Wheels, but if both are present on PyPI, pip will prefer a compatible wheel. You can override pip`s default behavior by e.g. using its –no-binary option.

Wheels are a pre-built distribution format that provides faster installation compared to Source Distributions (sdist), especially when a project contains compiled extensions.

If pip does not find a wheel to install, it will locally build a wheel and cache it for future installs, instead of rebuilding the source distribution in the future.

# Upgrading packages
Upgrade an already installed SomeProject to the latest from PyPI.

$ python3 -m pip install --upgrade SomeProject

# Installing to the User Site
To install packages that are isolated to the current user, use the --user flag:

$ python3 -m pip install --user SomeProject

For more information see the User Installs section from the pip docs.

Note that the --user flag has no effect when inside a virtual environment - all installation commands will affect the virtual environment.

If SomeProject defines any command-line scripts or console entry points, --user will cause them to be installed inside the user base’s binary directory, which may or may not already be present in your shell’s PATH. (Starting in version 10, pip displays a warning when installing any scripts to a directory outside PATH.) If the scripts are not available in your shell after installation, you’ll need to add the directory to your PATH:

On Linux and macOS you can find the user base binary directory by running python -m site --user-base and adding bin to the end. For example, this will typically print ~/.local (with ~ expanded to the absolute path to your home directory) so you’ll need to add ~/.local/bin to your PATH. You can set your PATH permanently by modifying ~/.profile.
On Windows you can find the user base binary directory by running py -m site --user-site and replacing site-packages with Scripts. For example, this could return C:\Users\Username\AppData\Roaming\Python36\site-packages so you would need to set your PATH to include C:\Users\Username\AppData\Roaming\Python36\Scripts. You can set your user PATH permanently in the Control Panel. You may need to log out for the PATH changes to take effect.

# Requirements files
Install a list of requirements specified in a Requirements File.

$ python3 -m pip install -r requirements.txt

#Installing from VCS
Install a project from VCS in “editable” mode. For a full breakdown of the syntax, see pip’s section on VCS Support.

$ python3 -m pip install -e git+https://git.repo/some_pkg.git#egg=SomeProject          # from git
$ python3 -m pip install -e hg+https://hg.repo/some_pkg#egg=SomeProject                # from mercurial
$ python3 -m pip install -e svn+svn://svn.repo/some_pkg/trunk/#egg=SomeProject         # from svn
$ python3 -m pip install -e git+https://git.repo/some_pkg.git@feature#egg=SomeProject  # from a branch


# Installing from other Indexes
Install from an alternate index

$ python3 -m pip install --index-url http://my.package.repo/simple/ SomeProject


Search an additional index during install, in addition to PyPI

$ python3 -m pip install --extra-index-url http://my.package.repo/simple SomeProject


# Installing from a local src tree
Installing from local src in Development Mode, i.e. in such a way that the project appears to be installed, but yet is still editable from the src tree.

$ python3 -m pip install -e <path>


You can also install normally from src

$ python3 -m pip install <path>


# Installing from local archives
Install a particular source archive file.

$ python3 -m pip install ./downloads/SomeProject-1.0.4.tar.gz


# Install from a local directory containing archives (and don’t check PyPI)

$ python3 -m pip install --no-index --find-links=file:///local/dir/ SomeProject
$ python3 -m pip install --no-index --find-links=/local/dir/ SomeProject
$ python3 -m pip install --no-index --find-links=relative/dir/ SomeProject


# Installing from other sources
To install from other data sources (for example Amazon S3 storage) you can create a helper application that presents the data in a PEP 503 compliant index format, and use the --extra-index-url flag to direct pip to use that index.

./s3helper --port=7777
$ python -m pip install --extra-index-url http://localhost:7777 SomeProject

# Installing Prereleases
Find pre-release and development versions, in addition to stable versions. By default, pip only finds stable versions.

$ python3 -m pip install --pre SomeProject


# Installing Setuptools “Extras”
Install setuptools extras.

$ python3 -m pip install SomePackage[PDF]
$ python3 -m pip install SomePackage[PDF]==3.0
$ python3 -m pip install -e .[PDF]==3.0  # editable project in current directory
