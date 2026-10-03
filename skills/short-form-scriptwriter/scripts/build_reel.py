import subprocess, wave, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1920
BG=(16,24,20); G=(120,220,160); WH=(255,255,255)
QB="/usr/share/fonts/truetype/quicksand/Quicksand-Bold.ttf"; QR="/usr/share/fonts/truetype/quicksand/Quicksand-Regular.ttf"
F=lambda p,s: ImageFont.truetype(p,s)
def bg():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    for y in range(H):
        c=int(10*y/H); d.line([(0,y),(W,y)],fill=(BG[0]+c//2,BG[1]+c,BG[2]+c//2))
    return im
def wrap(d,t,f,w):
    lines=[];cur=""
    for wd in t.split():
        if d.textlength((cur+" "+wd).strip(),font=f)>w: lines.append(cur);cur=wd
        else: cur=(cur+" "+wd).strip()
    lines.append(cur); return lines
def card(im,src,box,width,y=620):
    s=Image.open(src).convert("RGB").crop(box); s=s.resize((width,int(width*s.height/s.width)),Image.LANCZOS)
    m=Image.new("L",s.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,s.width,s.height),28,fill=255)
    sh=Image.new("RGBA",(s.width+80,s.height+80),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((40,48,s.width+40,s.height+48),28,fill=(0,0,0,150)); sh=sh.filter(ImageFilter.GaussianBlur(22))
    x=(W-s.width)//2
    im.paste(sh,(x-40,y-40),sh); im.paste(s,(x,y),m); return im
def headline(text,sub=None,color=WH,size=96):
    t=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(t); f=F(QB,size); y=200
    for ln in wrap(d,text,f,W-160): d.text((80,y),ln,font=f,fill=color); y+=size+16
    if sub: d.text((80,y+10),sub,font=F(QB,44),fill=G)
    return t
def caption(text):
    t=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(t); f=F(QB,50)
    lines=wrap(d,text,f,W-220); h=len(lines)*66+50; y0=1620
    d.rounded_rectangle((60,y0,W-60,y0+h),32,fill=(0,0,0,170))
    y=y0+25
    for ln in lines: d.text((110,y),ln,font=f,fill=WH); y+=66
    return t
scenes=[
 dict(head="A buyer DMs your shop.",sub="Do you reply from memory?",vo="A buyer asks if the wig comes in 18 inch.",img=("m_inbox.png",(30,1440,1140,2330),1000),zoom=("0.0004",0.5,1.045)),
 dict(head="Tenda drafts the reply from your catalog.",sub="Price, size, add-on.",vo="Tenda drafts the answer from your sample catalog. Price, size, and a bonnet add-on.",img=("m_inbox.png",(150,1940,1140,2310),1000,720),zoom=("0.0004",0.5,1.04)),
 dict(head="Tenda stops before money moves.",sub="You decide.",vo="Before any payment request goes out, it waits for your yes.",img=("m_approve.png",(30,1440,1140,2330),1000),zoom=("0.0004",0.5,1.045)),
 dict(head="Early demo.",sub=None,vo="This is an early demo. The catalog is a sample, and the payment is simulated.",img=None,list=["Sample catalog","Simulated MoMo","No live payments yet"]),
 dict(head="Try it. Tell us what is missing.",sub=None,vo="Try the demo, and tell us what is missing.",img=None,url="tendaapp.onrender.com"),
]
parts=[]
for i,s in enumerate(scenes):
    base=bg()
    if s["img"]: base=card(base,*s["img"])
    d0=ImageDraw.Draw(base)
    if s.get("list"):
        y=720
        for t in s["list"]:
            d0.rounded_rectangle((80,y,W-80,y+170),36,outline=G,width=5); d0.text((130,y+52),t,font=F(QB,56),fill=WH); y+=230
    if s.get("url"):
        d0.text((80,760),"tenda.",font=F(QB,150),fill=G); d0.text((80,960),s["url"],font=F(QB,64),fill=WH)
    base.save(f"b{i}.png"); headline(s["head"],s["sub"]).save(f"h{i}.png"); caption(s["vo"]).save(f"c{i}.png")
    subprocess.run(["/home/sandbox/tools/m10/bin/python","-m","piper","-m","/home/sandbox/tools/vid/en_US-lessac-medium.onnx","-f",f"v{i}.wav","--",s["vo"].replace("Tenda","Ten-dah").replace("18 inch","eighteen inch")],check=True,capture_output=True)
    w=wave.open(f"v{i}.wav"); dur=w.getnframes()/w.getframerate()+ (1.0 if i<4 else 1.4)
    n=int(dur*30)
    zr,fy,zm=s.get("zoom",("0.0005",0.5,1.05))
    vf=("[0:v]zoompan=z='min(zoom+"+zr+","+str(zm)+")':x='iw/2-(iw/zoom/2)':y='min(max(ih*"+str(fy)+"-(ih/zoom/2),0),ih-ih/zoom)':d=%d:s=1080x1920:fps=30[bg];"
        "[1:v]format=rgba,fade=in:st=0.1:d=0.45:alpha=1[hd];"
        "[2:v]format=rgba,fade=in:st=0.5:d=0.4:alpha=1[cp];"
        "[bg][hd]overlay=x=0:y='if(lt(t,0.55),70*(1-(t-0.1)/0.45),0)':shortest=1[a];[a][cp]overlay=0:0:shortest=1,format=yuv420p,fade=out:st=%.2f:d=0.25[v]")%(n,dur-0.25)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","30","-t",f"{dur:.2f}","-i",f"b{i}.png","-loop","1","-framerate","30","-t",f"{dur:.2f}","-i",f"h{i}.png","-loop","1","-framerate","30","-t",f"{dur:.2f}","-i",f"c{i}.png","-i",f"v{i}.wav",
        "-filter_complex",vf,"-map","[v]","-map","3:a","-af","adelay=250|250,apad","-t",f"{dur:.2f}","-r","30","-c:v","libx264","-preset","veryfast","-crf","20","-c:a","aac","-ar","44100",f"p{i}.mp4"],check=True)
    parts.append(f"p{i}.mp4")
open("list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","list.txt","-c","copy","noMusic.mp4"],check=True)
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","noMusic.mp4"]))
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","noMusic.mp4","-ss","6","-i","music.mp3","-filter_complex",f"[1:a]volume=0.16,afade=in:d=1.2,afade=out:st={dur-1.8:.2f}:d=1.8,atrim=0:{dur:.2f}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","/downloads/tenda-reel-v1.mp4"],check=True)
print("dur",dur)
