import subprocess,glob,wave,os
from PIL import Image,ImageDraw,ImageFont
fs=glob.glob('/usr/share/fonts/**/*Bold*.ttf',recursive=True)[0]
fr=[f for f in glob.glob('/usr/share/fonts/**/*.ttf',recursive=True) if 'Bold' not in f][0]
B=lambda s:ImageFont.truetype(fs,s); R=lambda s:ImageFont.truetype(fr,s)
W,H=1080,1350; BG=(16,24,20); G=(120,220,160); WH=(255,255,255)
def base(): 
    im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)
def wrap(d,t,f,x,y,w,fill=WH,gap=14):
    line="";
    for wd in t.split():
        if d.textlength(line+" "+wd,font=f)>w: d.text((x,y),line,font=f,fill=fill); y+=f.size+gap; line=wd
        else: line=(line+" "+wd).strip()
    d.text((x,y),line,font=f,fill=fill); return y+f.size+gap
scenes=[]
# 1 title
im,d=base(); d.text((80,120),"TENDA - EARLY DEMO",font=B(40),fill=G); wrap(d,"How a chat becomes an order you approve",B(96),80,300,920); scenes.append(("Selling in DMs means the same questions all day. Here is how Tenda handles one sale, in an early demo.",im))
# 2 real screen
im,d=base(); d.text((80,100),"The seller control center",font=B(50),fill=G)
s=Image.open('/downloads/proof-browser-use-tenda-2.png').convert('RGB').crop((int(.24*Image.open('/downloads/proof-browser-use-tenda-2.png').width),int(.06*Image.open('/downloads/proof-browser-use-tenda-2.png').height),int(.875*Image.open('/downloads/proof-browser-use-tenda-2.png').width),int(.78*Image.open('/downloads/proof-browser-use-tenda-2.png').height))); s=s.resize((920,int(920*s.height/s.width))); im.paste(s,(80,300)); d.text((80,1240),"Real screen from the live demo",font=R(34),fill=(170,170,170)); scenes.append(("This is the seller control center. One inbox, and four sample workers that each do one job.",im))
# 3 flow
im,d=base(); d.text((80,100),"One sample sale",font=B(50),fill=G)
steps=["1  Buyer asks a question","2  Tenda drafts the order","3  You review and approve","4  Payment (simulated MoMo)","5  Delivery (phase 2)"]
y=260
for i,t in enumerate(steps):
    d.rounded_rectangle((80,y,1000,y+150),24,outline=G if i<4 else (110,110,110),width=5); d.text((120,y+45),t,font=B(48) if i<4 else R(48),fill=WH if i<4 else (150,150,150)); y+=190
scenes.append(("A buyer asks a question. Tenda drafts the order. You review it and approve it. Payment is simulated in this demo. Delivery comes later.",im))
# 4 control
im,d=base(); d.text((80,120),"YOU DECIDE",font=B(44),fill=G); wrap(d,"Every order waits for your yes.",B(110),80,300,920); wrap(d,"Tenda drafts. You approve.",R(60),80,820,920,fill=(200,200,200)); scenes.append(("Every order waits for your yes. Tenda drafts. You decide.",im))
# 5 limits
im,d=base(); d.text((80,120),"WHAT IS NOT LIVE YET",font=B(44),fill=G)
y=300
for t in ["No live WhatsApp","No real MoMo payments","No sign-in or waitlist yet","Sample catalog only"]:
    d.text((80,y),"-  "+t,font=R(62),fill=WH); y+=130
scenes.append(("This is an early demo. WhatsApp, real payments, sign-in and the waitlist are not live yet. The catalog is a sample.",im))
# 6 close
im,d=base(); wrap(d,"Try the demo. Tell us what is missing.",B(100),80,380,920); d.text((80,1000),"tendaapp.onrender.com",font=B(56),fill=G); scenes.append(("Try the demo, and tell us what is missing.",im))
parts=[]
for i,(txt,im) in enumerate(scenes):
    im.save(f"s{i}.png"); open(f"s{i}.txt","w").write(txt)
    subprocess.run(["../m10/bin/python","-m","piper","-m","en_US-lessac-medium","-f",f"s{i}.wav","--",txt],check=True,capture_output=True)
    w=wave.open(f"s{i}.wav"); dur=w.getnframes()/w.getframerate()+0.9
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",f"s{i}.png","-i",f"s{i}.wav","-af","apad=pad_dur=1","-t",f"{dur:.2f}","-vf","scale=1080:1350,format=yuv420p,fade=in:0:8,fade=out:st=%.2f:d=0.3"%(dur-0.3),"-r","24","-c:v","libx264","-c:a","aac","-ar","44100",f"p{i}.mp4"],check=True)
    parts.append(f"p{i}.mp4")
open("list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","list.txt","-c","copy","/downloads/tenda-explainer-sample.mp4"],check=True)
