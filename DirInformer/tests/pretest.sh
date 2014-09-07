#!/bin/sh
#
# pretest.sh
# erstellt ein direktory mit files und dirs zum testen.
# dieser file wird nur einmal aufgerufen.

mkdir testdir
mkdir testdir/d1
mkdir testdir/d2
mkdir testdir/d3
echo "..." > testdir/d1/d1f1
echo "..." > testdir/d1/d1f2
echo "..." > testdir/d2/d2f1
echo "..." > testdir/d3/d3f1

echo "..." > testdir/f1
echo "..." > testdir/f2
echo "..." > testdir/f3
echo "..." > testdir/f4


