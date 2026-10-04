"""Public-only Pillar search identity audit. No account access or writes."""
import concurrent.futures,json,re,urllib.request,xml.etree.ElementTree as ET
HOSTS=['pillar-fabric.onrender.com','pillar-agent-fabric.onrender.com','tendaapp.onrender.com','strata-real-estate.onrender.com','pillar-clips.onrender.com','pillar-ai-monitoring.onrender.com']
def fetch(u):
 try:
  with urllib.request.urlopen(u,timeout=30) as r:return r.status,r.read().decode(),None
 except Exception as e:return None,'',str(e)
def page(u):
 status,s,error=fetch(u);issues=[];schemas=[]
 if status!=200:issues.append('not_200')
 title=re.findall(r'<title[^>]*>(.*?)</title>',s,re.S|re.I)
 canon=re.findall(r'<link[^>]*rel=[\"\']canonical[\"\'][^>]*href=[\"\']([^\"\']+)',s,re.I)
 if not title:issues.append('missing_title')
 if not canon:issues.append('missing_canonical')
 if len(re.findall(r'<h1(?:\s|>)',s,re.I))!=1:issues.append('h1_count')
 if not re.search(r'<meta[^>]*name=[\"\']description[\"\']',s,re.I):issues.append('missing_description')
 for v in re.findall(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',s,re.S|re.I):
  try:schemas.append(json.loads(v))
  except:issues.append('invalid_jsonld')
 if not schemas:issues.append('missing_jsonld')
 return {'url':u,'status':status,'title':title,'canonical':canon,'issues':issues,'error':error}
def main():
 urls=set();assets=[]
 for h in HOSTS:
  for p in ['/robots.txt','/llms.txt','/sitemap.xml']:
   u='https://'+h+p;status,s,error=fetch(u);assets.append({'url':u,'status':status,'bytes':len(s),'error':error})
   if p=='/sitemap.xml' and status==200:
    try:
     root=ET.fromstring(s)
     urls.update(e.text for e in root.iter() if e.tag.endswith('}loc'))
    except:assets[-1]['error']='invalid_xml'
 urls.add('https://pillar-fabric.onrender.com/static/brand-facts.html')
 pages=list(concurrent.futures.ThreadPoolExecutor(6).map(page,sorted(urls)))
 print(json.dumps({'assets':assets,'pages':pages,'page_count':len(pages),'issue_count':sum(len(p['issues']) for p in pages)},indent=2))
if __name__=='__main__':main()
