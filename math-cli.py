#!/usr/bin/env python3
"""
Math API CLI Tool
A Python CLI for load testing the math API endpoint
"""

import argparse
import requests
import time
import statistics
from typing import List, Tuple
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

class MathAPIClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def make_request(self, a: int, b: int) -> Tuple[bool, float, int]:
        """
        Make a single API request
        Returns: (success, response_time, result)
        """
        url = f"{self.base_url}/api/math/add"
        params = {'a': a, 'b': b}
        
        start_time = time.time()
        try:
            response = self.session.get(url, params=params, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = int(response.text.strip())
                return True, response_time, result
            else:
                print(f"HTTP {response.status_code}: {response.text}")
                return False, response_time, 0
                
        except requests.RequestException as e:
            response_time = time.time() - start_time
            print(f"Request failed: {e}")
            return False, response_time, 0

def sequential_load_test(client: MathAPIClient, iterations: int, delay: float, 
                        a_formula: str, b_formula: str, verbose: bool) -> dict:
    """Run sequential load test"""
    results = []
    response_times = []
    
    print(f"Running {iterations} sequential requests...")
    
    for i in range(1, iterations + 1):
        # Calculate a and b using formulas
        a = eval(a_formula.replace('i', str(i)))
        b = eval(b_formula.replace('i', str(i)))
        
        success, response_time, result = client.make_request(a, b)
        response_times.append(response_time)
        
        if verbose:
            status = "✓" if success else "✗"
            print(f"Request {i:3d}: a={a:2d}, b={b:2d}, result={result:3d}, time={response_time*1000:.1f}ms {status}")
        
        results.append(success)
        
        if delay > 0 and i < iterations:
            time.sleep(delay)
    
    return {
        'results': results,
        'response_times': response_times,
        'success_count': sum(results),
        'total_count': len(results)
    }

def concurrent_load_test(client: MathAPIClient, iterations: int, max_workers: int,
                        a_formula: str, b_formula: str, verbose: bool) -> dict:
    """Run concurrent load test"""
    results = []
    response_times = []
    
    print(f"Running {iterations} concurrent requests with {max_workers} workers...")
    
    def make_concurrent_request(i: int):
        a = eval(a_formula.replace('i', str(i)))
        b = eval(b_formula.replace('i', str(i)))
        success, response_time, result = client.make_request(a, b)
        
        if verbose:
            status = "✓" if success else "✗"
            print(f"Request {i:3d}: a={a:2d}, b={b:2d}, result={result:3d}, time={response_time*1000:.1f}ms {status}")
        
        return success, response_time
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(make_concurrent_request, i): i 
                          for i in range(1, iterations + 1)}
        
        for future in as_completed(future_to_index):
            success, response_time = future.result()
            results.append(success)
            response_times.append(response_time)
    
    return {
        'results': results,
        'response_times': response_times,
        'success_count': sum(results),
        'total_count': len(results)
    }

def print_statistics(stats: dict, execution_time: float):
    """Print detailed statistics"""
    response_times = stats['response_times']
    success_rate = stats['success_count'] / stats['total_count'] * 100
    
    print("\n" + "="*50)
    print("STATISTICS")
    print("="*50)
    print(f"Total requests:      {stats['total_count']}")
    print(f"Successful:          {stats['success_count']}")
    print(f"Failed:              {stats['total_count'] - stats['success_count']}")
    print(f"Success rate:        {success_rate:.1f}%")
    print(f"Total time:          {execution_time:.2f}s")
    print(f"Requests per second: {stats['total_count'] / execution_time:.2f}")
    
    if response_times:
        print(f"\nResponse Times:")
        print(f"  Average:           {statistics.mean(response_times)*1000:.1f}ms")
        print(f"  Median:            {statistics.median(response_times)*1000:.1f}ms")
        print(f"  Min:               {min(response_times)*1000:.1f}ms")
        print(f"  Max:               {max(response_times)*1000:.1f}ms")
        if len(response_times) > 1:
            print(f"  Std deviation:     {statistics.stdev(response_times)*1000:.1f}ms")

def main():
    parser = argparse.ArgumentParser(
        description='Math API Load Testing CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 10                          # 10 requests, a=i, b=i*2
  %(prog)s 20 --delay 0.5              # 20 requests with 0.5s delay
  %(prog)s 50 --concurrent 5           # 50 requests, 5 concurrent workers
  %(prog)s 10 --a-formula 'i*3' --b-formula 'i+5'  # Custom formulas
  %(prog)s 100 --url http://prod:8080  # Different server
        """
    )
    
    parser.add_argument('iterations', type=int, help='Number of requests to make')
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='Base URL (default: http://localhost:8080)')
    parser.add_argument('--delay', type=float, default=0, 
                       help='Delay between requests in seconds (default: 0)')
    parser.add_argument('--concurrent', type=int, default=0, metavar='WORKERS',
                       help='Number of concurrent workers (default: sequential)')
    parser.add_argument('--a-formula', default='i', 
                       help='Formula for parameter a (default: i)')
    parser.add_argument('--b-formula', default='i*2', 
                       help='Formula for parameter b (default: i*2)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show individual request details')
    
    args = parser.parse_args()
    
    if args.iterations <= 0:
        print("Error: iterations must be a positive integer")
        sys.exit(1)
    
    # Create client
    client = MathAPIClient(args.url)
    
    print("Math API Load Tester")
    print("=" * 50)
    print(f"URL:         {args.url}/api/math/add")
    print(f"Iterations:  {args.iterations}")
    print(f"A formula:   {args.a_formula}")
    print(f"B formula:   {args.b_formula}")
    
    if args.concurrent:
        print(f"Mode:        Concurrent ({args.concurrent} workers)")
    else:
        print(f"Mode:        Sequential (delay: {args.delay}s)")
    print()
    
    # Run load test
    start_time = time.time()
    
    try:
        if args.concurrent:
            stats = concurrent_load_test(client, args.iterations, args.concurrent,
                                       args.a_formula, args.b_formula, args.verbose)
        else:
            stats = sequential_load_test(client, args.iterations, args.delay,
                                       args.a_formula, args.b_formula, args.verbose)
        
        execution_time = time.time() - start_time
        print_statistics(stats, execution_time)
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()