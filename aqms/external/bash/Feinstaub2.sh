#!/bin/bash
WDIR=/usr/local/shellscripts/airquality
stty -F /dev/ttyUSB0  9600 raw

#Rohdaten erfassen
INPUT=$(od --endian=big -x -N10 < \/dev/ttyUSB0|head -n 1|cut -f2-10 -d" ");

FIRST4BYTES=$(echo $INPUT|cut -b1-4);
PPM25LOW=$(echo $INPUT|cut -f2 -d " "|cut -b1-2);
PPM25HIGH=$(echo $INPUT|cut -f2 -d " "|cut -b3-4);
PPM10LOW=$(echo $INPUT|cut -f3 -d " "|cut -b1-2);
PPM10HIGH=$(echo $INPUT|cut -f3 -d " "|cut -b3-4);

#In Dezimalzahlen umwandeln
PPM25LOWDEC=$(echo      $((0X$PPM25LOW)) );
PPM25HIGHDEC=$(echo     $((0X$PPM25HIGH)) );
PPM10LOWDEC=$(echo      $((0X$PPM10LOW)) );
PPM10HIGHDEC=$(echo     $((0X$PPM10HIGH)) );

#Berechnungsformel
PPM25=$(echo "scale=1;((($PPM25HIGHDEC * 256) +  $PPM25LOWDEC) /10 ) "|bc -l );
PPM10=$(echo "scale=1;((($PPM10HIGHDEC * 256)  +  $PPM10LOWDEC) /10 ) "|bc -l );

#Dezimalwerte ausgeben
echo $PPM25
