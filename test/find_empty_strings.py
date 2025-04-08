#!/usr/bin/python
"""
Debug script to find empty strings in the dataset that might be causing
the ZeroDivisionError in dedupe.
"""

import csv
import os
from collections import defaultdict


def find_empty_fields(filename):
    """
    Read the CSV file and identify which fields have empty strings
    and in which records they occur
    """
    empty_fields = defaultdict(list)
    row_count = 0

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_count += 1
            row_id = (
                f"{row.get('b_pubid', 'unknown')}.{row.get('b_sourceid', 'unknown')}"
            )

            # Check each field for empty string
            for field, value in row.items():
                if value == "":
                    empty_fields[field].append(row_id)

    return empty_fields, row_count


def main():
    input_file = "2025-04-08_mi_person.csv"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return

    print(f"Analyzing file: {input_file}")
    empty_fields, total_rows = find_empty_fields(input_file)

    print(f"Total records processed: {total_rows}")

    if not empty_fields:
        print("No empty fields found in any records.")
        return

    print("\nFields with empty values:")
    for field, row_ids in sorted(
        empty_fields.items(), key=lambda x: len(x[1]), reverse=True
    ):
        count = len(row_ids)
        percent = (count / total_rows) * 100
        print(f"  {field}: {count} records ({percent:.2f}%)")

    # Print some sample record IDs for fields with many empty values
    print("\nSample record IDs with empty values:")
    for field, row_ids in empty_fields.items():
        if len(row_ids) > 0:
            print(f"  {field}: {row_ids[:5]}")
            if len(row_ids) > 5:
                print(f"    ... and {len(row_ids) - 5} more")

    # Specifically check the string fields used in the deduper
    string_fields = [
        "normalized_first_name",
        "normalized_last_name",
        "normalized_street",
        "normalized_city",
        "normalized_state",
        "addpostal_code",
        "addcountry",
        "cleansed_email",
        "standardized_phone",
    ]

    print("\nString fields used in dedupe:")
    for field in string_fields:
        if field in empty_fields:
            count = len(empty_fields[field])
            percent = (count / total_rows) * 100
            print(f"  {field}: {count} empty values ({percent:.2f}%)")
        else:
            print(f"  {field}: No empty values")


if __name__ == "__main__":
    main()
