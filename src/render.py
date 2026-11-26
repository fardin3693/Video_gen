import os,sys,subprocess,time
from scenes import render
from captions import draw
import imageio_ffmpeg
F=imageio_ffmpeg.get_ffmpeg_exe()
if len(sys.argv)>1 and sys.argv[1]=='stills':
 for t in [0,2.4,4,7,10,13.5,17,21,25,28.5,32,35.5,39,43,47,51,55,57,59.9667]:
  im=render(t); draw(im,t); im.save('build/frame_%05.1f.jpg'%t,quality=90)
 print('saved stills'); quit()
cmd=[F,'-y','-loglevel','warning','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','-','-i','build/master.wav','-t','60','-c:v','libx264','-preset','veryfast','-crf','20','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','out/preview.mp4']
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); st=time.time()
try:
 for i in range(1800):
  t=i/30; im=render(t); draw(im,t); p.stdin.write(im.tobytes())
  if i%300==0: print(f'{i}/1800 frames, {time.time()-st:.1f}s',flush=True)
finally:
 p.stdin.close()
code=p.wait(); print('preview status',code,flush=True); sys.exit(code)
