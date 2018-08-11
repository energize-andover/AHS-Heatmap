import cairosvg
import os

cairosvg.svg2png(url=os.path.join('svg', 'Andover HS level 3.svg'),
                 write_to=os.path.join('converted svgs', 'Andover HS level 3.png'))
