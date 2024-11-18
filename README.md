# KritaRandomExporter

A python script for exporting large amounts of varying images from Krita. Includes functionality for rarity and as many random traits as desired.

Use the massExporter script in Krita's built-in Scripter plugin. I recommend saving the script locally and modifying, and then loading it into Scripter. 

Modify the attributes in the script to whatever you want (color is set up as an example), and set rarity_counts to the total count of each rarity. Layer hierarchy must be set up to match attributes in the file, with names representing traits and variations with an underscore (traitName_variationName).

If you want to render animations (This will take longer) then set up the animation timeline in Krita, and set the path for your ffmpeg location. (Get it here: https://www.ffmpeg.org/download.html) Otherwise set generate_animation to false.
