import PIL.ImageShow
from swf.movie import SWF
from swf.export import SVGExporter
from os import listdir, path
import PIL

# create a file object
# spell_directorie =r"C:\Users\apeir\AppData\Local\Ankama\Retro\resources\app\retroclient\clips\spells\icons\up"
spell_directorie =r"C:\Users\apeir\AppData\Local\Ankama\Retro\resources\app\retroclient\data\maps"
spell_readed = r"C:\Users\apeir\Documents\code\dofus\Spellls"
file = open(path.join(spell_directorie,"10121_0907091136X.swf"), 'rb')

# load and parse the SWF
swf = SWF(file)
print(swf)
# create the SVG exporter
svg_exporter = SVGExporter()

# export!
svg = swf.export(svg_exporter)

# save the SVG
# open(path.joint(spell_readed,"1.svg"), 'wb').write(svg.read())

PIL.ImageShow(svg.read())