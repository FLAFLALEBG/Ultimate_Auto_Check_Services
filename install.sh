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
  printf "Must be run as root. Try 'sudo'\n"
  exit 1
}

echo "Installing dependencies"
apt-get update
apt-get install --no-install-recommends -y wget ca-certificates sudo systemd

echo "Creating temp folder on $TMPDIR"
mkdir $TMPDIR
cd $TMPDIR || exit

# get install code
echo "Getting build code..."
wget -qO- --content-disposition https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services/archive/$BRANCH/latest.tar.gz \
  | tar -xzv \
  || exit 1

cd - && cd "$TMPDIR"/Ultimate_Auto_Check_Services-"$BRANCH" || exit

echo "Installing code..."

# shellcheck disable=SC2225
cp -v uacs/ /usr/bin
chmod +x /usr/bin/uacs/*

echo "Cleaning of the installation"
curl -X PURGE raw.githubusercontent.com
# shellcheck disable=SC2153
rm -rf "$TEMPDIR"

echo "Done."

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
