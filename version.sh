#!/bin/bash
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

BRANCH=`git branch | grep \* | cut -d ' ' -f2 | tr -d '_-'`
VERSION=`cat VERSION`

# on CircleCI the BRANCH variable is not set correctly
if [ ! $BRANCH ]; then BRANCH=$CIRCLE_BRANCH; fi

case $BRANCH in
	"master")
		echo -n $VERSION
		;;
	"dev")
		echo -n "${VERSION}.dev$(git rev-list dev...origin/master | wc -l)"
		;;
	*)
		headmaster=`git rev-list HEAD...origin/master | wc -l`
		headdev=`git rev-list HEAD...origin/dev | wc -l`
		revdiff=$((headdev - headmaster))
		echo -n "${VERSION}.dev${revdiff#-}+${BRANCH}${headdev}"
		;;
esac
