UniProt Database Web Parser Project
--

TLDR: This parser can be used to parse UniProt accession id and obtain related data from the UniProt web database.

To parse UniProt accession

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

