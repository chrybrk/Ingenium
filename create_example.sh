t=$1
f=$(date +".%d.%m.%Y")
n=$t
n+=$f

mkdir ./example/$n
cp $2 ./example/$n
