for image in *.png
do
    file=$image
    #identify -verbose $file
    minimumsize=10
    actualsize=$(du -k "$file" | cut -f 1)
    if [ $actualsize -ge $minimumsize ]; then
        echo "\n"
        echo "+++++++++++++++"
        identify -format "%wx%h" $file
        echo " "
        echo $file : size is over $minimumsize kilobytes :size
        nomFichier=${image%.*}
        convert -quality 80 $nomFichier.png $nomFichier.jpg
        #convert $file -resize 50%  $file
        #convert $file -resize 800x600  new_$file
    else
        echo "\n"
        echo "---------------"
        identify -format "%wx%h" $file
        echo " "
        echo $file : size is under $minimumsize kilobytes :size

    fi
done


# https://www.maketecheasier.com/convert-images-linux-command-line/


#convertir une capture PNG en JPEG et la compresser à 20 %. Cela est fort utile pour ne pas alourdir inutilement vos demandes d'aide sur le forum :
#https://doc.ubuntu-fr.org/imagemagick
#convert -quality 20 image.png image.jpg

# https://imagemagick.org/script/convert.php
