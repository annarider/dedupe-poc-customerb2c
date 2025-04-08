#!/usr/bin/python
"""
This code demonstrates how to use dedupe with a comma separated values
(CSV) file. All operations are performed in memory, so will run very
quickly on datasets up to ~10,000 rows.

We start with a CustomerB2C CSV file containing our data from the
MI table, which means it contains normalized fields. We are
skipping pre-processing in this file because standardizing data
 happens inside xDM using enrichers already.

The output will be a CSV with our clustered results.

Cite: https://github.com/dedupeio/dedupe-examples/blob/main/csv_example/csv_example.py
"""

import csv
import logging
import optparse
import os
import re
import time

import dedupe
import datetimetype
from unidecode import unidecode


def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean empty strings to be None instead
            clean_row = {}
            for k, v in row.items():
                # Replace empty strings with None to avoid ZeroDivisionError
                clean_row[k] = None if v == "" else v

            # Create a unique row_id
            row_id = (
                f"{row.get('b_pubid', 'unknown')}.{row.get('b_sourceid', 'unknown')}"
            )
            data_d[row_id] = clean_row

    return data_d


if __name__ == "__main__":

    start_time = time.time()

    # ## Logging

    # Dedupe uses Python logging to show or suppress verbose output. This
    # code block lets you change the level of loggin on the command
    # line. You don't need it if you don't want that. To enable verbose
    # logging, run `python examples/csv_example/csv_example.py -v`
    optp = optparse.OptionParser()
    optp.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        help="Increase verbosity (specify multiple times for more)",
    )
    (opts, args) = optp.parse_args()
    log_level = logging.WARNING
    if opts.verbose:
        if opts.verbose == 1:
            log_level = logging.INFO
        elif opts.verbose >= 2:
            log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    # ## Setup

    input_file = "2025-04-08_mi_person.csv"
    output_file = "2025-04-08_mi_person_clustered.csv"
    settings_file = "customerb2c_learned_settings"
    training_file = "customerb2c_training.json"

    print("importing data ...")
    data_d = readData(input_file)

    # If a settings file already exists, we'll just load that and skip training
    if os.path.exists(settings_file):
        print("reading from", settings_file)
        with open(settings_file, "rb") as f:
            deduper = dedupe.StaticDedupe(f)
    else:
        # ## Training

        # Define the fields dedupe will pay attention to
        fields = [
            dedupe.variables.String("normalized_first_name"),
            dedupe.variables.String("normalized_last_name"),
            dedupe.variables.Exact("member_id", has_missing=True),
            datetimetype.DateTime("date_of_birth", has_missing=True, yearfirst=True),
            dedupe.variables.String("normalized_street", has_missing=True),
            dedupe.variables.ShortString("normalized_city"),
            dedupe.variables.ShortString("normalized_state"),
            dedupe.variables.ShortString("addpostal_code", has_missing=True),
            dedupe.variables.ShortString("addcountry", has_missing=True),
            dedupe.variables.String("cleansed_email"),
            dedupe.variables.String("standardized_phone", has_missing=True),
        ]

        # Create a new deduper object and pass our data model to it.
        deduper = dedupe.Dedupe(fields)

        # If we have training data saved from a previous run of dedupe,
        # look for it and load it in.
        # __Note:__ if you want to train from scratch, delete the training_file
        if os.path.exists(training_file):
            print("reading labeled examples from ", training_file)
            with open(training_file, "rb") as f:
                deduper.prepare_training(data_d, f)
        else:
            deduper.prepare_training(data_d)

        # ## Active learning
        # Dedupe will find the next pair of records
        # it is least certain about and ask you to label them as duplicates
        # or not.
        # use 'y', 'n' and 'u' keys to flag duplicates
        # press 'f' when you are finished
        print("starting active labeling...")

        dedupe.console_label(deduper)

        # Using the examples we just labeled, train the deduper and learn
        # blocking predicates
        deduper.train()

        # When finished, save our training to disk
        with open(training_file, "w") as tf:
            deduper.write_training(tf)

        # Save our weights and predicates to disk.  If the settings file
        # exists, we will skip all the training and learning next time we run
        # this file.
        with open(settings_file, "wb") as sf:
            deduper.write_settings(sf)

    # ## Clustering

    # `partition` will return sets of records that dedupe
    # believes are all referring to the same entity.

    print("clustering...")
    clustered_dupes = deduper.partition(data_d, 0.5)

    print("# duplicate sets", len(clustered_dupes))

    # ## Writing Results

    # Write our original data back out to a CSV with a new column called
    # 'Cluster ID' which indicates which records refer to each other.

    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score,
            }

    with open(output_file, "w") as f_output, open(input_file) as f_input:

        reader = csv.DictReader(f_input)
        fieldnames = ["Cluster ID", "confidence_score"] + reader.fieldnames

        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row_id = int(row["Id"])
            row.update(cluster_membership[row_id])
            writer.writerow(row)

    # ## Calculate time dedupe took

    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processing completed in {processing_time:.2f} seconds")

    # Optionally, save to a file:
    with open("timing_results.txt", "w") as f:
        f.write(f"Dedupe processing time: {processing_time:.2f} seconds")
