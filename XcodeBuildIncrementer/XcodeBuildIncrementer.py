import os, plistlib

PROJECT_DIR, INFOPLIST_FILE = None, None

try:
    PROJECT_DIR = os.environ['PROJECT_DIR']
    INFOPLIST_FILE = os.environ['INFOPLIST_FILE']
    BUILD_CONFIGURATION = os.environ['CONFIGURATION']
    BUILD_CONFIGURATION_DIR = os.environ['CONFIGURATION_BUILD_DIR']
    IS_RELEASE = BUILD_CONFIGURATION == "Release"
    IS_ARCHIVE = "ArchiveIntermediates" in BUILD_CONFIGURATION_DIR and IS_RELEASE
except:
    print "Could not find the required environment variables: PROJECT_DIR, INFOPLIST_FILE\nIf this is being run in Xcode, then this is an error! Trying command line args..."
    # TODO: Add command line option

def get_new_bundle_version(CFBundleShortVersionString, CFBundleVersion):
    """
    Get a new bundle version using
    :param CFBundleShortVersionString: str - The current version of the app
    :param CFBundleVersion: - The current bundle version of the app

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.3.2",CFBundleVersion="4325")
    4326

    >>> print get_new_bundle_version(CFBundleShortVersionString="5",CFBundleVersion="7000")
    7001

    >>> print get_new_bundle_version(CFBundleShortVersionString="1",CFBundleVersion="1.1")
    1.2

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.3.2",CFBundleVersion="1.3.2.1")
    1.3.2.2

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.3.2.4",CFBundleVersion="1.3.2.5")
    1.3.2.4.1

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.2",CFBundleVersion="1.2.1")
    1.2.2

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.3.1",CFBundleVersion="1.3.1")
    1.3.1.1

    >>> print get_new_bundle_version(CFBundleShortVersionString="1.3.2",CFBundleVersion="1.2.2.1")
    1.3.2.1

    """

    if IS_ARCHIVE:
        return CFBundleShortVersionString
    elif IS_RELEASE:

        if "." not in CFBundleVersion:
            return str(int(CFBundleVersion)+1)

        version_string_split = CFBundleShortVersionString.split('.')
        old_bundle_version_split = CFBundleVersion.split('.')

        version_string_sigfigs = len(version_string_split)
        old_bundle_version_sigfigs = len(old_bundle_version_split)

        if version_string_sigfigs == old_bundle_version_sigfigs-1:

            def sig_figs_match(version_string_split, old_bundle_version_split):
                new_bundle_list_split = list(old_bundle_version_split)
                del new_bundle_list_split[-1]
                ziped_list = zip(version_string_split,  new_bundle_list_split)
                true_false = all(i == y for i, y in ziped_list)
                return true_false

            sig_figs_match = sig_figs_match(version_string_split, old_bundle_version_split)

            if sig_figs_match:
                old_bundle_version_split[old_bundle_version_sigfigs-1] = str(int(old_bundle_version_split[old_bundle_version_sigfigs-1]) + 1)
                return ".".join(old_bundle_version_split)


        return CFBundleShortVersionString + ".1"

    return CFBundleVersion

def run_and_change_build():
    plist_filename = "{project_dir}/{infoplist_file}".format(project_dir=PROJECT_DIR, infoplist_file=INFOPLIST_FILE)
    plist = plistlib.readPlist(plist_filename)
    new_bundle_version = get_new_bundle_version(plist["CFBundleShortVersionString"], plist["CFBundleVersion"])
    plist["CFBundleVersion"] = new_bundle_version
    plistlib.writePlist(plist, plist_filename)

if PROJECT_DIR and INFOPLIST_FILE:
    run_and_change_build()