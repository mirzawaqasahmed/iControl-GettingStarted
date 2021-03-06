#!/usr/bin/python
'''
# The contents of this file are subject to the "END USER LICENSE AGREEMENT FOR F5
# Software Development Kit for iControl"; you may not use this file except in
# compliance with the License. The License is included in the iControl
# Software Development Kit.
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is iControl Code and related documentation
# distributed by F5.
#
# The Initial Developer of the Original Code is F5 Networks,
# Inc. Seattle, WA, USA. Portions created by F5 are Copyright (C) 1996-2004 F5 Networks,
# Inc. All Rights Reserved.  iControl (TM) is a registered trademark of F5 Networks, Inc.
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public License (the "GPL"), in which case the
# provisions of GPL are applicable instead of those above.  If you wish
# to allow use of your version of this file only under the terms of the
# GPL and not to allow others to use your version of this file under the
# License, indicate your decision by deleting the provisions above and
# replace them with the notice and other provisions required by the GPL.
# If you do not delete the provisions above, a recipient may use your
# version of this file under either the License or the GPL.
'''


def get_pool_list(bigip):
    try:
        poollist = bigip.LocalLB.Pool.get_list()
        print "POOL LIST"
        print " ---------"
        for pool in poollist:
            print "   %s" % pool

    except Exception, e:
        print e


def create_pool(bigip, pool):
    try:
        bigip.LocalLB.Pool.create_v2([pool], ['LB_METHOD_ROUND_ROBIN'], [[]])
    except Exception, e:
        print e


if __name__ == "__main__":
    import bigsuds, argparse, getpass, ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    parser = argparse.ArgumentParser(description='Create Pool')

    parser.add_argument("host", help='BIG-IP IP or Hostname' )
    parser.add_argument("username", help='BIG-IP Username')
    parser.add_argument("-p", "--poolname", help='Name of pool you wish to create')
    parser.add_argument("-f", "--folder", help='Partition/Folder you want the pool to reside in')
    args = vars(parser.parse_args())

    hostname = args['host']
    username = args['username']
    poolname = None if args['poolname'] is None else args['poolname']
    partition = None if args['folder'] is None else args['folder']

    print "%s, enter your password: " % args['username'],
    password = getpass.getpass()

    b = bigsuds.BIGIP(hostname, username, password)

    if poolname is None:
        get_pool_list(b)
    else:
        if partition is None:
            poolname = '/Common/%s' % poolname
        else:
            poolname = '/%s/%s' % (partition, poolname)
        create_pool(b, poolname)