# IVY Homes API Exploration
#### I have added documentation pdf for my whole process of thorigh and exploration.
## Overview
This project focuses on exploring and analyzing the IVY Homes API, including different versions, rate limits, and methods to extract name data efficiently. The process involved API enumeration, request handling, and adaptive querying strategies.

## API Exploration Process
### Initial Observations
- Started with **v1** API and observed that it returned names starting with the query string, limited to **10 results per request**.
- Identified **v2** and **v3** versions by analyzing the URL structure.
- Used **Nmap scan** to find open ports:
  - **Port 22 (SSH)** required a private key.
  - **Port 8000 (API)** ran **Uvicorn**.
- Used **SQLMap** to check for SQL injection vulnerabilities but found none.
- Attempted **reverse engineering** to reconstruct the backend function but found no conclusive patterns.

### Exploring Endpoints
- Used **dirb** to enumerate endpoints and discovered:
  - `/hint`
  - `/help`
  - `/solution`

### Requesting a Hint
- A **POST request** to `/hint` provided a clue about increasing the number of results.

### Finding the Query Parameter for Increasing Results
- Identified `max_requests` as the correct parameter to increase results.

### Extracting Names from Different API Versions
- Identified character sets:
  - **v1:** `a-z`
  - **v2:** `a-z, 0-9`
  - **v3:** `a-z, 0-9, space, +, -, .`
- Used **recursive querying** with increasing character combinations to handle result limits.

### Adapting to API Version Differences
- **v1 & v2:** Returned names between **2-10 characters**.
- **v3:** Included **1-character names**.
- Adjusted approach for each version accordingly.

### Rate Limiting Challenges
| API Version | Request Limit |
|-------------|--------------|
| v1         | 100 requests  |
| v2         | 50 requests   |
| v3         | 80 requests   |

- Implemented **request throttling** using Python’s `time` module.
- Tested **IP rotation** techniques but optimized for efficiency.

### Verification & Comparison
- Used the `/solution` endpoint to validate extracted results.
- Compared official sizes vs. extracted sizes:
  - **v1:** 18,632 (official) vs. 18,609 (extracted)
  - **v2:** 13,730 (official) vs. 13,701 (extracted)
  - **v3:** 12,517 (official) vs. 11,275 (extracted)
- Minor discrepancies due to potential edge cases.

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/help` | `POST` | Provides guidance on API exploration. |
| `/hint` | `POST` | Returns a hint when accessed with a POST request. |
| `/solution` | `PUT` | Returns encoded statistics about the solution. |
| `/v1/autocomplete?query=a` | `GET` | Returns up to 50 results (default: 10). |
| `/v2/autocomplete?query=a` | `GET` | Returns up to 75 results (default: 12). |
| `/v3/autocomplete?query=a` | `GET` | Returns up to 100 results (default: 15). |

## Final Thoughts
- The project involved **API enumeration, adaptive querying, and rate-limit handling**.
- Learned about **query parameter manipulation** and **efficient data extraction**.
- Discovered minor inconsistencies that may indicate **undocumented constraints**.



