import hashlib,json,pathlib,re,unittest,wave
R=pathlib.Path(__file__).resolve().parents[2]
class WorkshopTests(unittest.TestCase):
 def setUp(self):
  self.timeline=json.loads((R/'workshop/timeline.json').read_text())
 def test_delivery_package(self):
  for f in ['final_video.mp4','thumbnail.jpg','script.md','subtitles.srt','description.md','sources.md','asset-credits.md','storyboard.md','production-report.md']:
   self.assertGreater((R/'output'/f).stat().st_size,0,f)
 def test_actual_export(self):
  q=json.loads((R/'output/qa/validation.json').read_text());self.assertTrue(q['passed'])
  self.assertEqual(q['sha256'],hashlib.sha256((R/'output/final_video.mp4').read_bytes()).hexdigest())
  self.assertEqual((q['resolution'],q['fps'],q['videoCodec'],q['audioCodec']),([1080,1920],'30/1','h264','aac'))
  self.assertTrue(50<=q['duration']<=60);self.assertLess(q['fileBytes'],100_000_000)
 def test_scene_continuity(self):
  scenes=self.timeline['scenes'];self.assertEqual(scenes[0]['start'],0)
  for a,b in zip(scenes,scenes[1:]):self.assertAlmostEqual(a['end'],b['start'],places=6)
  self.assertEqual(scenes[-1]['end'],self.timeline['duration'])
  for s in scenes:self.assertTrue((R/f'film/compositions/{s["id"]}.html').exists())
 def test_audio_caption_sample_clock(self):
  sections=self.timeline['sections'];self.assertEqual(len(sections),24)
  for s in sections:
   with wave.open(str(R/'film'/s['audio'])) as w: duration=w.getnframes()/w.getframerate()
   self.assertAlmostEqual(s['end']-s['start'],duration,places=5)
  self.assertEqual(len(re.findall(r' --> ',(R/'output/subtitles.srt').read_text())),len(sections))
 def test_take_metadata_matches_script(self):
  e=json.loads((R/'workshop/episode.json').read_text());v=json.loads((R/'workshop/voice-takes.json').read_text())
  self.assertEqual(e['voice'],v['voice'])
  for a,b in zip(e['sections'],v['sections']):
   self.assertEqual((a['text'],a['speed']),(b['text'],b['speed']))
 def test_licensed_assets_and_native_images(self):
  for f in ['sun-earth.jpg','daylight-city.jpg','frozen-world.jpg','vent-life.jpg']:
   self.assertGreater((R/'film/assets'/f).stat().st_size,1000)
  description=(R/'output/description.md').read_text()
  self.assertIn('Music: Space Ambience by Alexander Nakarada',description)
  self.assertIn('https://creativecommons.org/licenses/by/4.0/',description)
  self.assertEqual((R/'lol.md').read_text(),'this is a sample file/\n')
if __name__=='__main__':unittest.main()
