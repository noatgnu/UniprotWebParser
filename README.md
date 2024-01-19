UniProt Database Web Parser Project
--
[![Downloads](https://static.pepy.tech/personalized-badge/uniprotparser?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/uniprotparser)


TLDR: This parser can be used to parse UniProt accession id and obtain related data from the UniProt web database.

To use:

```bash
python -m pip install uniprotparser
```
or 

```bash
python3 -m pip install uniprotparser
```
With version 1.2.0, we have exposed `to` and `from` mapping parameters for UniProt API where you can indicate which database you want to map to and from.


```python
from uniprotparser import get_from_fields, get_to_fields

#to get all available fields to map from

from_fields = get_from_fields()
print(from_fields)

#to get all available fields to map to
to_fields = get_to_fields()
print(to_fields)
```

These parameters can be passed to the `parse` method of the `UniprotParser` class as follow

```python
from uniprotparser.betaparser import UniprotParser

parser = UniprotParser()
for p in parser.parse(ids=["P06493"], to_key="UniProtKB", from_key="UniProtKB_AC-ID"):
    print(p)
```


With version 1.1.0, a simple CLI interface has been added to the package.

```bash
Usage: uniprotparser [OPTIONS]

Options:
  -i, --input FILENAME   Input file containing a list of accession ids
  -o, --output FILENAME  Output file
  --help                 Show this message and exit.
```

With version 1.0.5, support for asyncio through `aiohttp` has been added to `betaparser`. Usage can be seen as follow

```python
from uniprotparser.betaparser import UniprotParser
from io import StringIO
import asyncio
import pandas as pd

async def main():
    example_acc_list = ["Q99490", "Q8NEJ0", "Q13322", "P05019", "P35568", "Q15323"]
    parser = UniprotParser()
    df = []
    #Yield result for 500 accession ids at a time
    async for r in parser.parse_async(ids=example_acc_list):
        df.append(pd.read_csv(StringIO(r), sep="\t"))
    
    #Check if there were more than one result and consolidate them into one dataframe
    if len(df) > 0:
        df = pd.concat(df, ignore_index=True)
    else:
        df = df[0]

asyncio.run(main())
```

With version 1.0.2, support for the new UniProt REST API have been added under `betaparser` module of the package.

In order to utilize this new module, you can follow the example bellow

```python
from uniprotparser.betaparser import UniprotParser
from io import StringIO

import pandas as pd
example_acc_list = ["Q99490", "Q8NEJ0", "Q13322", "P05019", "P35568", "Q15323"]
parser = UniprotParser()
df = []
#Yield result for 500 accession ids at a time
for r in parser.parse(ids=example_acc_list):
    df.append(pd.read_csv(StringIO(r), sep="\t"))

#Check if there were more than one result and consolidate them into one dataframe
if len(df) > 0:
    df = pd.concat(df, ignore_index=True)
else:
    df = df[0]


```

---
To parse UniProt accession with legacy API

```python
from uniprotparser.parser import UniprotSequence

protein_id = "seq|P06493|swiss"

acc_id = UniprotSequence(protein_id, parse_acc=True)

#Access ACCID
acc_id.accession

#Access isoform id
acc_id.isoform
```

To get additional data from UniProt online database

```python
from uniprotparser.parser import UniprotParser
from io import StringIO
#Install pandas first to handle tabulated data
import pandas as pd

protein_accession = "P06493"

parser = UniprotParser([protein_accession])

#To get tabulated data
result = []
for i in parser.parse("tab"):
    tab_data = pd.read_csv(i, sep="\t")
    last_column_name = tab_data.columns[-1]
    tab_data.rename(columns={last_column_name: "query"}, inplace=True)
    result.append(tab_data)
fin = pd.concat(result, ignore_index=True)

#To get fasta sequence
with open("fasta_output.fasta", "wt") as fasta_output:
    for i in parser.parse():
        fasta_output.write(i)
```

