import requests
import string
import itertools
import json
import time
from datetime import datetime

# Global rate control
REQUEST_COUNT = 0
LAST_REQUEST_TIME = 0
MIN_REQUEST_INTERVAL = 0.6  # 60 seconds / 100 requests = 0.6 seconds per request

def enforce_rate_limit():
    """Ensure we don't exceed 100 requests/minute"""
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    LAST_REQUEST_TIME = time.time()

def generate_queries():
    """Generate all aa-zz combinations"""
    return [''.join(c) for c in itertools.product(string.ascii_lowercase, repeat=2)]

def fetch_recursive(query):
    """Recursive fetcher with strict rate control"""
    global REQUEST_COUNT
    
    try:
        # Enforce rate limit before each request
        enforce_rate_limit()
        REQUEST_COUNT += 1
        
        response = requests.get(
            "http://35.200.185.69:8000/v1/autocomplete",
            params={"query": query, "max_results": 5000},
            timeout=15
        )
        
        response.raise_for_status()
        data = response.json()
        
        if data["count"] < 50:
            return data["results"]
            
        return [item for c in string.ascii_lowercase 
               for item in fetch_recursive(query + c)]
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            backoff = max(MIN_REQUEST_INTERVAL, 5)  # Minimum 5 second backoff
            print(f"Rate limited. Cooling down for {backoff}s (Total requests: {REQUEST_COUNT})")
            time.sleep(backoff)
            return fetch_recursive(query)
        return []
        
    except Exception as e:
        print(f"Error on {query}: {str(e)} (Total requests: {REQUEST_COUNT})")
        return []

def main():
    global REQUEST_COUNT
    queries = generate_queries()
    all_results = []
    start_time = time.time()
    
    try:
        for i, query in enumerate(queries, 1):
            print(f"Processing {i}/{len(queries)}: {query} | Requests: {REQUEST_COUNT}")
            results = fetch_recursive(query)
            all_results.extend(results)
            
            # Save progress every 50 queries
            if i % 50 == 0:
                with open("partial_results.json", "w") as f:
                    json.dump({
                        "requests": REQUEST_COUNT,
                        "progress": f"{i/len(queries):.1%}",
                        "results": all_results
                    }, f, indent=2)
                
    except KeyboardInterrupt:
        print("\nInterrupted. Saving partial results...")
    
    # Final save with deduplication
    with open("final_results_v1.json", "w") as f:
        json.dump({
            "total_requests": REQUEST_COUNT,
            "unique_results": len(set(all_results)),
            "execution_time": round(time.time() - start_time, 2),
            "generated_at": datetime.now().isoformat(),
            "results": sorted(list(set(all_results)))
        }, f, indent=2)
        
    print(f"Completed! Total API requests: {REQUEST_COUNT}")

if __name__ == "__main__":
    main()
