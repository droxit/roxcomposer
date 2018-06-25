BRANCH=`git branch | grep \* | cut -d ' ' -f2 | tr -d '_-'`
VERSION=`cat VERSION`

case $BRANCH in
	"master")
		echo -n $VERSION
		;;
	"dev")
		echo -n "${VERSION}.dev$(git rev-list dev...master | wc -l)"
		;;
	*)
		headmaster=`git rev-list HEAD...master | wc -l`
		headdev=`git rev-list HEAD...dev | wc -l`
		revdiff=$((headmaster - headdev))
		echo -n "${VERSION}.dev${revdiff}+${BRANCH}${headdev}"
		;;
esac
