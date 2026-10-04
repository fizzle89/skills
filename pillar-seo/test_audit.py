import importlib.util,unittest
spec=importlib.util.spec_from_file_location('audit','/tmp/pillar_seo_audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
class AuditTests(unittest.TestCase):
 def test_valid_page(self):
  a.fetch=lambda u:(200,'<title>X</title><meta name="description" content="Y"><link rel="canonical" href="https://x/"><h1>Hello</h1><script type="application/ld+json">{"@type":"WebPage"}</script>',None)
  self.assertEqual(a.page('https://x/')['issues'],[])
 def test_missing_fields(self):
  a.fetch=lambda u:(200,'<p>empty</p>',None)
  self.assertEqual(set(a.page('https://x/')['issues']),{'missing_title','missing_description','missing_canonical','h1_count','missing_jsonld'})
 def test_bad_schema(self):
  a.fetch=lambda u:(200,'<script type="application/ld+json">oops</script>',None)
  self.assertIn('invalid_jsonld',a.page('https://x/')['issues'])
 def test_error(self):
  a.fetch=lambda u:(None,'','down')
  self.assertIn('not_200',a.page('https://x/')['issues'])
if __name__=='__main__':unittest.main()
