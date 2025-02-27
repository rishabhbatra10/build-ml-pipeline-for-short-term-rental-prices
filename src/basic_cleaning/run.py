#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    data = pd.read_csv(artifact_local_path)
    df = data.copy()
    logger.info(f"Reading {artifact_local_path}")
    ######################
    # YOUR CODE HERE     #
    ######################
    min_price = float(args.min_price)
    max_price = float(args.max_price)
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Changes to the longitude and latitude
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("Cleaned the dataset and removed outliers")
    df.to_csv(args.output_artifact, index=False)

    # Uploading to W&B
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    logger.info("Saving the artifact")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price value",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price",
        required=True
    )

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Cleaning dataset",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the artifact.",
        required=True
    )


    args = parser.parse_args()

    go(args)
