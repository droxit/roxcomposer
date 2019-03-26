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
		echo -n "${VERSION}.dev${revdiff}+${BRANCH}${headdev}"
		;;
esac
