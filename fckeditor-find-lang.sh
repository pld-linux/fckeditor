#!/bin/sh
dir=$RPM_BUILD_ROOT/usr/share/fckeditor
langfile=$1

> $langfile
find $dir -type d -name lang | while read dir; do
	echo "%dir ${dir#$RPM_BUILD_ROOT}" >> $langfile

	for f in $dir/??*.js; do
		lang=${f##*/}
		lang=${lang%.*}
		dir=${f#$RPM_BUILD_ROOT}
		case "$lang" in
		en-au)
			lang=en_AU
		;;
		en-ca)
			lang=en_CA
		;;
		en-uk)
			lang=en_UK
		;;
		fr-ca)
			lang=fr_CA
		;;
		pt-br)
			lang=pt_BR
		;;
		sr-latn)
			lang=sr@Latin
		;;
		zh-cn)
			lang=zh_CN
		;;
		*-*)
			echo >&2 "Need mapping for $lang!"
			exit 1
		;;
		esac
		echo "%lang($lang) ${dir#$RPM_BUILD_ROOT}" >> $langfile
	done
done
