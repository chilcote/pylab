#!/usr/bin/python
#ref https://gist.github.com/bruienne/a66d26602d9b6eb76072

# pylint: disable=fixme, line-too-long, missing-docstring, C0103

# Many parts of this were taken from Greg Neagle's COSXIP (https://github.com/munki/createOSXinstallPkg)
# No parsing of 'BannedRegexMatchVersion' keys currently because regex is hard.
#
# Output prints a list of incompatible apps for each major OS X version
#   with its version and optional file listing of the target app.

import plistlib
import subprocess
import sys
import os
from xml.parsers.expat import ExpatError

LION_PKGNAME = 'MacOS_10_7_IncompatibleAppList.pkg'
LION_CATALOG_URL = ('http://swscan.apple.com/content/catalogs/others/'
                    'index-lion-snowleopard-leopard.merged-1.sucatalog')

MTN_LION_PKGNAME = 'OSX_10_8_IncompatibleAppList.pkg'
MTN_LION_CATALOG_URL = ('https://swscan.apple.com/content/catalogs/others/'
                        'index-mountainlion-lion-snowleopard-leopard'
                        '.merged-1.sucatalog')

MAVERICKS_PKGNAME = 'OSX_10_9_IncompatibleAppList.pkg'
MAVERICKS_CATALOG_URL = ('https://swscan.apple.com/content/catalogs/others/'
                         'index-10.9-mountainlion-lion-snowleopard-leopard'
                         '.merged-1.sucatalog')

YOSEMITE_PKGNAME = 'OSX_10_10_IncompatibleAppList.pkg'
YOSEMITE_CATALOG_URL = (
    'https://swscan.apple.com/content/catalogs/others/'
    'index-10.10-10.9-mountainlion-lion-snowleopard-leopard'
    '.merged-1.sucatalog')

EL_CAPITAN_PKGNAME = 'OSX_10_11_IncompatibleAppList.pkg'
EL_CAPITAN_CATALOG_URL = (
    'https://swscan.apple.com/content/catalogs/others/'
    'index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard'
    '.merged-1.sucatalog')


def downloadURL(URL, to_file=None):
    '''Downloads URL to the current directory or as string'''
    cmd = ['/usr/bin/curl', '--silent', '--show-error', '--url', URL]
    if to_file:
        cmd.extend(['-o', to_file])
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, err) = proc.communicate()
    if proc.returncode:
        print >> sys.stderr, 'Error %s retrieving %s' % (proc.returncode, URL)
        print >> sys.stderr, err
        return None
    if to_file:
        return to_file
    else:
        return output


def findIncompatibleAppListPkgURL(catalog, package):
    '''Searches SU catalog to find a download URL for
    package_name. If there's more than one, returns the
    one with the most recent PostDate.'''

    def sort_by_PostDate(a, b):
        """Internal comparison function for use with sorting"""
        return cmp(b['PostDate'], a['PostDate'])

    catalog_str = downloadURL(catalog_url)
    try:
        catalog = plistlib.readPlistFromString(catalog_str)
    except ExpatError:
        print >> sys.stderr, 'Could not parse catalog!'
        return None
    product_list = []
    if 'Products' in catalog:
        for product_key in catalog['Products'].keys():
            product = catalog['Products'][product_key]
            for package in product.get('Packages', []):
                url = package.get('URL', '')
                if url.endswith(package_name):
                    product_list.append({'PostDate': product['PostDate'],
                                         'URL': url})
        if product_list:
            product_list.sort(sort_by_PostDate)
            return product_list[0]['URL']
    return None


def pkgextract(pkg_source, destination):

    proc = subprocess.Popen(['/usr/sbin/pkgutil', '--expand', pkg_source, destination],
                            shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    (output, err) = proc.communicate()

    return output, err


def cpioextract(source, pattern):

    proc = subprocess.Popen(['/usr/bin/cpio', '-idmu', '--quiet', '-I', source, pattern],
                            shell=False, bufsize=-1, cwd=os.path.dirname(source),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    (output, err) = proc.communicate()

    return output, err


for os_vers in ['10.7', '10.8', '10.9', '10.10', '10.11']:

    print '\nChecking incompatible apps for OS X %s\n' % os_vers

    if os_vers.startswith('10.7'):
        catalog_url = LION_CATALOG_URL
        package_name = LION_PKGNAME
        os_vers = '10.7'
    elif os_vers.startswith('10.8'):
        catalog_url = MTN_LION_CATALOG_URL
        package_name = MTN_LION_PKGNAME
        os_vers = '10.8'
    elif os_vers.startswith('10.9'):
        catalog_url = MAVERICKS_CATALOG_URL
        package_name = MAVERICKS_PKGNAME
        os_vers = '10.9'
    elif os_vers.startswith('10.10'):
        catalog_url = YOSEMITE_CATALOG_URL
        package_name = YOSEMITE_PKGNAME
        os_vers = '10.10'
    elif os_vers.startswith('10.11'):
        catalog_url = EL_CAPITAN_CATALOG_URL
        package_name = EL_CAPITAN_PKGNAME
        os_vers = '10.11'

    url = findIncompatibleAppListPkgURL(catalog_url, package_name)

    package_path = os.path.join('/tmp', package_name)

    if not os.path.exists(package_path):
        print 'Downloading pkg %s\n' % package_name
        package_path = downloadURL(url, to_file=package_path)

    workdir = os.path.splitext(package_path)[0]

    if not os.path.exists(workdir):
        print('Expanding pkg %s to %s\n' % (package_name, workdir))
        pkgextract(package_path, workdir)

    if not os.path.exists(os.path.join(workdir, 'System/Library/PrivateFrameworks/SystemMigration.framework/Versions/A/Resources/MigrationIncompatibleApplicationsList.plist')):
        print 'Extracting Payload at %s\n' % workdir
        cpioextract(os.path.join(workdir, 'Payload'), "*MigrationIncompatibleApplicationsList.plist*")

    incompatiblesource = plistlib.readPlist(os.path.join(
        workdir, 'System/Library/PrivateFrameworks/SystemMigration.framework/Versions/A/Resources/MigrationIncompatibleApplicationsList.plist'))

    incompatibleapps = []

    for application in incompatiblesource['IncompatiblePaths']:

        if application.get('Application Name'):
            if next((item for item in incompatibleapps if item["app"] == application.get('Application Name')), None) is None and application.get('MaximumBundleVersion'):
                incompatapp = {'app': application.get('Application Name')}
                incompatapp['MaximumBundleVersion'] = application.get(
                    'MaximumBundleVersion') or None
                if application.get('Paths'):
                    incompatapp['paths'] = application.get('Paths')
                if application.get('DependentPaths'):
                    if incompatapp.get('paths'):
                        incompatapp['paths'].append(application.get('DependentPaths'))
                    else:
                        incompatapp['paths'] = application.get('DependentPaths')
                incompatibleapps.append(incompatapp)
            # else:
            #     print 'Not adding %s' % application.get('Application Name')

        elif application.get('Read Me Group'):
            if next((item for item in incompatibleapps if item["app"] == application.get('Read Me Group')), None) is None and application.get('MaximumBundleVersion'):
                incompatapp = {'app': application.get('Read Me Group')}
                incompatapp['MaximumBundleVersion'] = application.get(
                    'MaximumBundleVersion') or None
                if application.get('Paths'):
                    incompatapp['paths'] = application.get('Paths')
                if application.get('DependentPaths'):
                    if incompatapp.get('paths'):
                        incompatapp['paths'].append(application.get('DependentPaths'))
                    else:
                        incompatapp['paths'] = application.get('DependentPaths')
                incompatibleapps.append(incompatapp)
            # else:
            #     print 'Not adding %s' % application.get('Read Me Group')

    for app in incompatibleapps:
        print app['app'], app.get('MaximumBundleVersion') or '', app.get('paths') or ''
