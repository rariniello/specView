import os.path
from subprocess import call
import zipfile
from packaging.version import Version
#import yaml


# TODO load the version from the yml file
#with open("version.yml", 'r') as file:
#    data = yaml.load(file, Loader=yaml.SafeLoader)
#    version = data['version']

version = "0.1.0"

os.environ["SPECVIEW_DIST_DIR"] = os.path.join(os.getcwd(), "dist")

os.environ["SPECVIEW_VERSION"] = version
iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

source = os.path.join(os.environ["SPECVIEW_DIST_DIR"], "specView")

fileName = "specView-{}-win".format(os.environ["SPECVIEW_VERSION"])

print("Creating installer")

v = Version(version)

print(v)

call([
    iscc,
    os.path.join(os.getcwd(), "dist_assets", "win", "specView_setup.iss"),
    "/dMyAppVersion=%s" % v,
    "/dMyAppDir=%s" % source,
    "/dMyOutputDir=%s" % os.path.join(os.getcwd()),
    "/dMyOutputFile=%s" % fileName])

print("Done")