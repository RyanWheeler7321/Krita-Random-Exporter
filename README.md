<img src="icon.svg" alt="Krita Random Exporter icon" width="96">

# Krita Random Exporter

A python script for exporting large amounts of varying images from Krita. Includes functionality for rarity and as many random traits as desired.

It's basically the scaffolding from a script I used in 2021 to generate a bunch of random images and gifs, so it's meant as a starting point to modify, not something to run as is.

Use the randomMassExporter script in Krita's built-in Scripter plugin. I recommend saving the script locally and modifying, and then loading it into Scripter. 

Modify the attributes in the script to whatever you want (color is set up as an example), and set rarity_counts to the total count of each rarity. Layer hierarchy must be set up to match attributes in the file, with names representing traits and variations with an underscore (traitName_variationName). Trait layers can be inside groups, and everything inside a trait layer gets turned on with it.

If you want to render animations (this takes longer) then set up the animation timeline in Krita, and set the path for your ffmpeg location. (Get it here: https://www.ffmpeg.org/download.html) Otherwise set generate_animation to False.
