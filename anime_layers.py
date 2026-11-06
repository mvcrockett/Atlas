"""Original layered anime-inspired animation: Pillow + FFmpeg; no external artwork."""
import math, random, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=640,360
random.seed(18)
stars=[(random.randrange(850),random.randrange(240)) for _ in range(95)]
petals=[(random.randrange(850),random.randrange(390),random.randrange(2,6)) for _ in range(26)]
def sky():
 im=Image.new('RGBA',(850,450));p=im.load()
 for y in range(450):
  t=y/450;c=(int(16+116*t),int(21+61*t),int(65+74*t),255)
  for x in range(850):p[x,y]=c
 d=ImageDraw.Draw(im)
 for x,y in stars:d.ellipse((x,y,x+2,y+2),fill=(250,225,211,190))
 d.ellipse((580,62,686,168),fill=(255,218,169,75))
 d.ellipse((601,83,665,147),fill=(255,231,191,255))
 return im
def city():
 im=Image.new('RGBA',(850,450));d=ImageDraw.Draw(im)
 for j in range(23):
  x=j*43-15;top=170+(j*29)%90
  d.rectangle((x,top,x+38,360),fill=(41,40,82,255))
  for yy in range(top+12,345,15):
   for xx in range(x+7,x+35,13):
    if (xx+yy+j)%4:d.rectangle((xx,yy,xx+4,yy+6),fill=(255,183,143,165))
 d.polygon([(0,350),(140,298),(290,333),(420,287),(550,335),(710,284),(850,345),(850,450),(0,450)],fill=(29,33,64,255))
 return im
def girl():
 im=Image.new('RGBA',(370,400));d=ImageDraw.Draw(im)
 d.ellipse((66,39,295,327),fill=(54,39,91,255))
 for k in range(8):
  x=75+k*25;d.polygon([(x,180),(x-16,320+(k%3)*20),(x+21,270)],fill=(77+3*k,52,127,255))
 d.polygon([(105,245),(248,244),(324,397),(42,397)],fill=(39,42,92,255))
 d.polygon([(146,250),(190,335),(227,252)],fill=(174,91,151,255))
 d.line([(108,268),(90,391)],fill=(110,102,177),width=5)
 d.line([(248,265),(278,390)],fill=(110,102,177),width=5)
 d.rounded_rectangle((152,214,211,278),radius=19,fill=(241,172,160,255))
 d.ellipse((101,83,262,259),fill=(252,200,181,255))
 d.ellipse((104,143,121,173),fill=(239,164,155,255))
 d.ellipse((248,143,266,173),fill=(239,164,155,255))
 for x in (136,207):
  d.ellipse((x-18,158,x+14,184),fill=(255,250,246,255))
  d.ellipse((x-7,159,x+9,181),fill=(106,66,177,255))
  d.ellipse((x-2,160,x+6,176),fill=(40,29,91,255))
  d.ellipse((x,162,x+4,166),fill='white')
  d.arc((x-21,151,x+17,170),185,348,fill=(43,30,70,255),width=4)
 d.arc((164,194,202,214),5,155,fill=(170,81,106,255),width=3)
 d.ellipse((132,189,151,195),fill=(241,129,146,90))
 d.ellipse((214,189,233,195),fill=(241,129,146,90))
 d.pieslice((91,49,268,170),177,353,fill=(70,46,116,255))
 d.polygon([(99,96),(136,44),(149,169),(124,150)],fill=(94,62,151,255))
 d.polygon([(153,64),(193,38),(187,160),(166,132)],fill=(86,52,142,255))
 d.polygon([(215,67),(263,93),(236,169),(221,128)],fill=(103,66,158,255))
 for x in (93,259):d.arc((x-20,105,x+20,285),75,260,fill=(154,103,194,255),width=4)
 d.ellipse((259,182,268,192),fill=(255,226,143,255))
 return im
SKY,CITY,GIRL=sky(),city(),girl()
def frame(i,total):
 t=i/total;phase=2*math.pi*t;camera=14*math.sin(phase*.55)
 im=Image.new('RGBA',(W,H))
 im.alpha_composite(SKY,(-110+int(camera*.18),-38))
 im.alpha_composite(CITY,(-105+int(camera*.5),-23))
 glow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(glow)
 d.ellipse((340,80,650,350),fill=(243,82,157,47))
 im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(48)))
 im.alpha_composite(GIRL,(140+int(camera*1.1),7+round(3*math.sin(phase*1.3))))
 d=ImageDraw.Draw(im)
 for j,(px,py,r) in enumerate(petals):
  x=(px+int(34*t*(j%3+1)))%700-25;y=(py+int(24*t*(j%2+1)))%420-20
  d.ellipse((x,y,x+r*2,y+r),fill=(255,169,213,185))
 d.rectangle((0,0,W,20),fill=(12,13,30,255))
 d.rectangle((0,H-24,W,H),fill=(12,13,30,255))
 d.text((28,28),'NO PANTS  /  NEW HORIZONS',fill=(255,224,223,255))
 return im.convert('RGB')
def main():
 root=Path('output/anime_layers');root.mkdir(parents=True,exist_ok=True)
 frames=root/'frames';frames.mkdir(exist_ok=True)
 fps=12;count=48;images=[]
 for i in range(count):
  im=frame(i,count);im.save(frames/f'frame_{i:04d}.png');images.append(im)
 delays=[10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(count)]
 images[0].save(root/'anime_layers.gif',save_all=True,append_images=images[1:],duration=delays,loop=0,disposal=2,optimize=False)
 if not shutil.which('ffmpeg'):raise RuntimeError('FFmpeg missing')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(fps),'-i',str(frames/'frame_%04d.png'),'-c:v','libx264','-profile:v','baseline','-level','3.1','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'anime_layers.mp4')],check=True)
 print('Anime layers showcase:',count,'frames',fps,'fps')
if __name__=='__main__':main()
