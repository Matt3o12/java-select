#!/bin/bash

set -e
start=`date +%s`

verbos=false
for i in "$@"; do
  [ "$i" = -v ] && verbose=true
done

txtred='\033[0;31m' 	# red color
txtblu='\033[0;34m' 	# blue color
txtrst='\033[0m'    	# Text Reset

info() {
    echo "${txtblu} > ${1}${txtrst}"
}

fail() {
	echo ${txtred}${1}${txtrst}
	exit 1
}

success() {
	if [ $verbose ]; then
		echo $1
	else
		printf "."
	fi
		
}

testVersion() {
	regex="^Version: ([0-9]\.){1,3}[0-9]( \(dev\))?$"
	if [[ $(java-select -v | grep -E "$regex") ]]; then
		success "Passed: testVersion"
	else
		fail "Didn't pass: testVersion"
	fi
}

testJavaHome_noHome() {
	export JAVA_HOME=""
	
	expected="No Java version could be found.
Use 'java-select change' to change Java."
	if [[ `java-select show` == "$expected" ]]; then
		success "Passed: testJavaHome_noHome"
	else
		fail "Didn't pass: testJavaHome_noHome"
	fi
}

testJavaHome() {
	mockedJavaHome="${TMPDIR}java-select_tests`date +%s`/Home"
	mockedJavaFile="${mockedJavaHome}/bin/java"
	
	mkdir -p "$mockedJavaHome/bin"
	
	touch $mockedJavaFile
	chmod +x $mockedJavaFile
	
	echo "#!/bin/sh
echo \"java version \"1.6.0_65\"\"" > $mockedJavaFile
	export JAVA_HOME="$mockedJavaHome"
	
	expected="Java 1.6.0_65 at $mockedJavaHome"
	if [[ `java-select show` == $expected ]]; then
		success "Passed: testJavaHome"
	else
		fail "Didn't pass: testJavaHome"
	fi
	
	rm -r $mockedJavaHome	
}

os="`sw_vers -productName` `sw_vers -productVersion` (`sw_vers -buildVersion`)"
echo "Running on $os"

info "Starting tests"

# tests
testVersion
testJavaHome_noHome
testJavaHome

echo

end=`date +%s`
info "Done in $((`date +%s`-$start)) second(s)"



