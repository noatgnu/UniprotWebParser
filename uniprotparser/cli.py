import pandas as pd

from uniprotparser.betaparser import UniprotParser, UniprotSequence
import click
import io
# Command line function for parsing Uniprot data from a list of accession ids provided using click.

@click.command()
@click.option("--input", "-i", help="Input file containing a list of accession ids", type=click.File("rt"))
@click.option("--output", "-o", help="Output file", type=click.File("wb"))
def main(input, output):
    # Read the input file
    acc_list = [i.strip() for i in input if i.strip()]
    acc_list = set(acc_list)

    # Create a UniprotParser object
    parser = UniprotParser()
    # Parse the accession ids
    results = [pd.read_csv(io.StringIO(r), sep="\t") for r in parser.parse(ids=acc_list)]
    # Concatenate the results into a single dataframe
    if len(results) > 1:
        results = pd.concat(results, ignore_index=True)
    else:
        results = results[0]
    # Write the results to the output file
    results.to_csv(output, index=False)
