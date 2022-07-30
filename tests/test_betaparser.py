import io
from unittest import TestCase
import pandas as pd
import pytest

from uniprotparser.betaparser import UniprotParser, UniprotSequence


class TestBetaUniprotParser(TestCase):
    def test_parse(self):
        d = pd.read_csv(r"C:\Users\Toan Phung\Downloads\test_Copies_02.txt", sep="\t")
        acc = set()
        for a in d["PG.ProteinGroups"]:
            if pd.notnull(a):
                for i in a.split(";"):
                    accession = UniprotSequence(i.strip(), parse_acc=True)
                    if accession.accession:
                        acc.add(accession.accession)
        parser = UniprotParser()
        df = []
        for r in parser.parse(ids=acc):
            df.append(pd.read_csv(io.StringIO(r), sep="\t"))
        if len(df) > 0:
            df = pd.concat(df, ignore_index=True)
        else:
            df = df[0]
        df.to_csv("test.csv", index=False)


@pytest.mark.asyncio
async def test_parse():
    d = pd.read_csv(r"C:\Users\Toan Phung\Downloads\test_Copies_02.txt", sep="\t")
    acc = set()
    for a in d["PG.ProteinGroups"]:
        if pd.notnull(a):
            for i in a.split(";"):
                accession = UniprotSequence(i.strip(), parse_acc=True)
                if accession.accession:
                    acc.add(accession.accession)
    parser = UniprotParser()
    df = []
    async for r in parser.parse_async(ids=acc):
        df.append(pd.read_csv(io.StringIO(r), sep="\t"))

    if len(df) > 0:
        df = pd.concat(df, ignore_index=True)
    else:
        df = df[0]
    df.to_csv("test.csv", index=False)