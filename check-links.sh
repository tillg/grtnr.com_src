#!/bin/bash

# Check links and output errors in compact format
OUTPUT_FILE="linkcheck-errors.txt"

echo "Running linkchecker on ./output..."

# Run linkchecker and format output
linkchecker ./output 2>&1 | awk '
/^Result.*Error:/ {
    gsub(/.*No such file or directory: /, "MISSING: ");
    gsub(/.*URLError.*/, "ERROR:");
    print;
}
/^Result.*Warning:/ {
    gsub(/^Result.*Warning:.*/, "WARNING:");
    print;
}
/^That/ {
    summary = $0;
    getline;
    print summary;
    exit;
}' > "$OUTPUT_FILE"

echo "Results written to $OUTPUT_FILE"

# Count issues (excluding summary line)
ISSUE_COUNT=$(grep -c "MISSING:\|WARNING:\|ERROR:" "$OUTPUT_FILE")
echo "$ISSUE_COUNT issues found"

# Exit with error code if issues found
if [ "$ISSUE_COUNT" -gt 0 ]; then
    exit 1
fi