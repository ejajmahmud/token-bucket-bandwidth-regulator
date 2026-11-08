"""CLI for token-bucket-bandwidth-regulator."""
import sys
import argparse
from .regulator import TokenBucketBandwidthRegulator


def main():
    parser = argparse.ArgumentParser(description="Token Bucket Bandwidth Regulator CLI")
    parser.add_argument("--demo", action="store_true", help="Run token bucket bandwidth regulation demo")
    args = parser.parse_args()

    if args.demo:
        reg = TokenBucketBandwidthRegulator(capacity=1000, refill_rate_per_sec=200)
        print(f"[*] Initial Tokens: {reg.tokens}")
        print(f"[*] Acquiring 800 tokens: {reg.try_acquire(800)}")
        print(f"[*] Remaining Tokens: {reg.tokens:.1f}")
        print(f"[*] Acquiring another 500 tokens: {reg.try_acquire(500)} (Wait needed: {reg.get_wait_time(500):.2f}s)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
