"""Unit tests for token-bucket-bandwidth-regulator."""
import unittest
from token_bucket_bandwidth_regulator.regulator import TokenBucketBandwidthRegulator


class TestTokenBucketBandwidthRegulator(unittest.TestCase):
    def test_acquire_success(self):
        reg = TokenBucketBandwidthRegulator(capacity=100, refill_rate_per_sec=10)
        self.assertTrue(reg.try_acquire(50))
        self.assertAlmostEqual(reg.tokens, 50.0, places=1)

    def test_acquire_deficit_and_wait(self):
        reg = TokenBucketBandwidthRegulator(capacity=100, refill_rate_per_sec=10)
        reg.try_acquire(90)
        self.assertFalse(reg.try_acquire(30))
        wait = reg.get_wait_time(30)
        self.assertGreater(wait, 0.0)

    def test_refill_over_time(self):
        reg = TokenBucketBandwidthRegulator(capacity=100, refill_rate_per_sec=10)
        reg.try_acquire(100)
        # Advance virtual time by 5 seconds -> adds 50 tokens
        future = reg.last_update + 5.0
        self.assertTrue(reg.try_acquire(40, now=future))
