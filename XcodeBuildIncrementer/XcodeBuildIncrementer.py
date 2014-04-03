import os, plistlib

PROJECT_DIR, INFOPLIST_FILE = None, None

try:
    PROJECT_DIR = os.environ['PROJECT_DIR']
    INFOPLIST_FILE = os.environ['INFOPLIST_FILE']
    BUILD_CONFIGURATION = os.environ['CONFIGURATION']
    BUILD_CONFIGURATION_DIR = os.environ['CONFIGURATION_BUILD_DIR']
    IS_RELEASE = BUILD_CONFIGURATION == "Release"
    IS_ARCHIVE = "ArchiveIntermediates" in BUILD_CONFIGURATION_DIR

except:
    print "Could not find the required environment variables: PROJECT_DIR, INFOPLIST_FILE\nIf this is being run in Xcode, then this is an error! Trying command line args..."
    # TODO: Add command line option


def get_new_version(version, IS_ARCHIVE, IS_RELEASE):
    """
    Get a new bundle version using
    :param CFBundleShortVersionString: str - The current version of the app
    :param CFBundleVersion: - The current bundle version of the app

    >>> print get_new_version(version="1.3.2.5", IS_ARCHIVE=False, IS_RELEASE=False)
    1.3.2.5

    >>> print get_new_version(version="1.3.2.5", IS_ARCHIVE=True, IS_RELEASE=False)
    1.3.2

    >>> print get_new_version(version="1.3.2.5", IS_ARCHIVE=False, IS_RELEASE=True)
    1.3.2.6

    >>> print get_new_version(version="1.3.2", IS_ARCHIVE=False, IS_RELEASE=False)
    1.3.2

    >>> print get_new_version(version="1.3.2", IS_ARCHIVE=True, IS_RELEASE=False)
    1.3

    >>> print get_new_version(version="1.3.2", IS_ARCHIVE=False, IS_RELEASE=True)
    1.3.3

    >>> print get_new_version(version="1.3", IS_ARCHIVE=False, IS_RELEASE=False)
    1.3

    >>> print get_new_version(version="1.3", IS_ARCHIVE=True, IS_RELEASE=False)
    1.0

    >>> print get_new_version(version="1.3", IS_ARCHIVE=False, IS_RELEASE=True)
    1.4

    """

    if not IS_ARCHIVE and not IS_RELEASE:
        return version

    version_split = version.split('.')
    version_split_sigfigs = len(version_split)

    # ARCHIVE
    if IS_ARCHIVE:
        if version_split_sigfigs == 2:
            version_split[1] = str(0)
        else:
            del version_split[-1]
        version = ".".join(version_split)
        return version

    # Release
    else:
        version_split[version_split_sigfigs-1] = str(int(version_split[version_split_sigfigs-1]) + 1)
        return ".".join(version_split)

def get_new_build(old_version, new_version, build):
    """
    Get a new bundle version using
    :param CFBundleShortVersionString: str - The current version of the app
    :param CFBundleVersion: - The current bundle version of the app

    >>> print get_new_build(old_version="1.3.2", new_version="1.3.2", build="4325")
    4326

    >>> print get_new_build(old_version="1.3.2", new_version="1.3.3", build="4325")
    1

    """

    # Version did not change, increment the current build number
    if old_version == new_version:
        return str(int(build) + 1)

    # Version changed, start over at 1
    else:
        return str(1)


def run_and_change_build():
    plist_filename = "{project_dir}/{infoplist_file}".format(project_dir=PROJECT_DIR, infoplist_file=INFOPLIST_FILE)
    plist = plistlib.readPlist(plist_filename)
    new_short_version = get_new_version(version=plist["CFBundleShortVersionString"], IS_ARCHIVE=IS_ARCHIVE, IS_RELEASE=IS_RELEASE)
    new_bundle_version = get_new_build(old_version=plist["CFBundleShortVersionString"], new_version=new_short_version, build=plist["CFBundleVersion"])
    plist["CFBundleShortVersionString"] = new_short_version
    plist["CFBundleVersion"] = new_bundle_version
    plistlib.writePlist(plist, plist_filename)

if PROJECT_DIR and INFOPLIST_FILE:
    run_and_change_build()