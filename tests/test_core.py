import unittest
from cache_stampede_replay import run
class DomainTests(unittest.TestCase):
 def test_singleflight_coalesces_cold_burst(self):
  r=run({'ttl_ms':100,'load_ms':20,'requests':[{'id':str(i),'key':'x','time_ms':i} for i in range(5)]})['policies'];self.assertEqual(r[0]['provider_loads'],5);self.assertEqual(r[1]['provider_loads'],1);self.assertEqual(r[1]['coalesced_requests'],4)
 def test_completion_processed_before_equal_time_request(self):
  p=run({'ttl_ms':100,'load_ms':20,'requests':[{'id':'a','key':'x','time_ms':0},{'id':'b','key':'x','time_ms':20}]})['policies'][1];self.assertEqual(p['responses'][1]['route'],'hit')
 def test_expiry_is_not_fresh(self):
  p=run({'ttl_ms':10,'load_ms':5,'requests':[{'id':'a','key':'x','time_ms':0},{'id':'b','key':'x','time_ms':15}]})['policies'][1];self.assertEqual(p['provider_loads'],2)
 def test_early_refresh_reduces_post_expiry_wait(self):
  ps=run({'ttl_ms':100,'load_ms':20,'early_refresh_ms':30,'requests':[{'id':'a','key':'x','time_ms':0},{'id':'b','key':'x','time_ms':95},{'id':'c','key':'x','time_ms':125}]})['policies'];self.assertEqual(ps[1]['responses'][2]['latency_ms'],20);self.assertEqual(ps[2]['responses'][2]['latency_ms'],0)
 def test_different_keys_not_coalesced(self):self.assertEqual(run({'ttl_ms':10,'load_ms':5,'requests':[{'id':x,'key':x,'time_ms':0} for x in 'ab']})['policies'][1]['provider_loads'],2)
