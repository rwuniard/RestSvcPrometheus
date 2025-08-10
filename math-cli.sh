#!/bin/bash

# Math API CLI Tool
# Usage: ./math-cli.sh <iterations> [base_url] [delay_seconds]

# Default values
DEFAULT_URL="http://localhost:8080"
DEFAULT_DELAY=0.1

# Parse command line arguments
ITERATIONS=${1:-100}
BASE_URL=${2:-$DEFAULT_URL}
DELAY=${3:-$DEFAULT_DELAY}

# Validate iterations is a number
if ! [[ "$ITERATIONS" =~ ^[0-9]+$ ]]; then
    echo "Error: iterations must be a positive integer"
    echo "Usage: $0 <iterations> [base_url] [delay_seconds]"
    exit 1
fi

# Function to make API call
make_api_call() {
    local i=$1
    local a=$i
    local b=$((i * 2))  # b = i * 2, you can modify this formula
    
    local url="${BASE_URL}/api/math/add?a=${a}&b=${b}"
    local response=$(curl -s "$url")
    local status=$?
    
    if [ $status -eq 0 ]; then
        echo "Request $i: a=$a, b=$b, result=$response"
    else
        echo "Request $i: FAILED (a=$a, b=$b)"
    fi
    
    return $status
}

# Main execution
echo "Math API Load Tester"
echo "===================="
echo "URL: $BASE_URL/api/math/add"
echo "Iterations: $ITERATIONS"
echo "Delay between requests: ${DELAY}s"
echo ""

# Track statistics
success_count=0
error_count=0
start_time=$(date +%s.%N)

# Make the API calls
for i in $(seq 1 $ITERATIONS); do
    if make_api_call $i; then
        ((success_count++))
    else
        ((error_count++))
    fi
    
    # Add delay between requests (except for the last one)
    if [ $i -lt $ITERATIONS ] && [ $(echo "$DELAY > 0" | bc -l 2>/dev/null || echo "1") -eq 1 ]; then
        sleep $DELAY
    fi
done

# Calculate execution time
end_time=$(date +%s.%N)
execution_time=$(echo "$end_time - $start_time" | bc -l 2>/dev/null || echo "N/A")

# Print summary
echo ""
echo "Summary:"
echo "========"
echo "Total requests: $ITERATIONS"
echo "Successful: $success_count"
echo "Failed: $error_count"
echo "Success rate: $(echo "scale=2; $success_count * 100 / $ITERATIONS" | bc -l 2>/dev/null || echo "N/A")%"
if [ "$execution_time" != "N/A" ]; then
    echo "Execution time: ${execution_time}s"
    requests_per_second=$(echo "scale=2; $ITERATIONS / $execution_time" | bc -l 2>/dev/null || echo "N/A")
    echo "Requests per second: $requests_per_second"
fi