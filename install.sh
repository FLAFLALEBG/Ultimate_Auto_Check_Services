#!/bin/bash
# Ultimate Auto Check Services installation script
#
# curl -sSL https://raw.githubusercontent.com/FLAFLALEBG/Ultimate_Auto_Check_Services/origin/install.sh | bash
#
# Usage: ./install.sh
#
# more details at https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services

BRANCH=origin

TMPDIR="/tmp/uacs"


[[ ${EUID} -ne 0 ]] && {
  # shellcheck disable=SC2059
  printf "Must be run as root. Try 'sudo $0'\n"
  exit 1
}
echo "Creating temp folder on $TMPDIR"
mkdir $TMPDIR

# get install code
echo "Getting build code..."

echo "Done.

First: Visit https://$IP/  https://nextcloudpi.local/ (also https://nextcloudpi.lan/ or https://nextcloudpi/ on windows and mac)
to activate your instance of NC, and save the auto generated passwords. You may review or reset them
anytime by using nc-admin and nc-passwd.
Second: Type 'sudo ncp-config' to further configure NCP, or access ncp-web on https://$IP:4443/
Note: You will have to add an exception, to bypass your browser warning when you
first load the activation and :4443 pages. You can run letsencrypt to get rid of
the warning if you have a (sub)domain available.
"

exit 0

# License
#
# This script is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA
