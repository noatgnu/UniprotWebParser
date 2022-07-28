import re
import time

import requests
import json

default_columns = "accession,id,gene_names,protein_name,organism_name,organism_id,length,xref_refseq," \
                                   "go_id,go_p,go_c,go_f,cc_subcellular_location," \
                                   "ft_topo_dom,ft_carbohyd,mass,cc_mass_spectrometry," \
                                   "sequence,ft_var_seq,cc_alternative_products"
# regex pattern for matching UniProt accession that can be used with the search object groupdict method to retrieve accession and isotype information separately
acc_regex = re.compile("(?P<accession>[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})(?P<isotype>-\d+)?")

# sequence object for storing and presenting uniprot id.
class UniprotSequence:
    def __init__(self, acc, parse_acc=False):
        """
        :type parse_acc: bool
        whether or not for the script to parse the accession id from the input
        :type acc: str
        a string containing the Uniprot accession ID of the sequence
        """
        self.raw_acc = acc
        self.accession = None
        self.isoform = None
        if parse_acc:
            match = acc_regex.search(self.raw_acc)
            if match:
                self.accession = match.groupdict(default="")["accession"]
                self.isoform = match.groupdict(default="")["isotype"]

    def __str__(self):
        return self.accession + self.isoform

    def __repr__(self):
        return self.accession + self.isoform

class UniprotResultLink:
    def __init__(self, url, poll_interval=5):
        self.url = url
        self.poll_interval = poll_interval
        self.completed = False

    def check_status(self):
        res = requests.get(self.url, allow_redirects=False)
        return res


# UniProt parser object for new UniProt REST API
class UniprotParser:
    result_url: list[UniprotResultLink]
    base_url = "https://rest.uniprot.org/idmapping/run"
    check_status_url = "https://rest.uniprot.org/idmapping/status/"

    def __init__(self, poll_interval: int = 5, format: str = "tsv", columns: str = ""):
        """

        :type columns: str
        string of all the fields represented in the final result delimited by ','
        for a full list of all field names available visit this link https://www.uniprot.org/help/return_fields
        :type poll_interval: int
        long polling interval between each round of checking whether or not the mapping operation has finished
        :type format: str
        format for the final output, by default, it is tabulated or 'tsv'. 'json' or 'xlsx' can be used.
        """
        self.poll_interval = poll_interval
        self.format = format
        if columns == "":
            self.columns = default_columns
        else:
            self.columns = columns

        # storing all result url object for checking
        self.result_url = []

    # get jobid from post submission
    def get_job_id(self):
        return json.loads(self.res.content.decode())["jobId"]

    # parse iterator for obtaining the result. If the result is over 500 accs, the data would be submitted in separate
    # jobs with 500 accs max for each
    def parse(self, ids):
        ids = list(ids)
        total_input = len(ids)
        # submitting all jobs and obtain unique url with jobid for checking status then append to
        # self.result_url attribute
        for i in range(0, total_input, 500):

            if (i + 500) <= total_input:
                print("Submitting {}/{}".format(i+500, total_input))
                self.res = requests.post(self.base_url, data={
                    "ids": ",".join(ids[i: i + 500]),
                    "from": "UniProtKB_AC-ID",
                    "to": "UniProtKB"
                })
                self.result_url.append(UniprotResultLink(self.check_status_url+self.get_job_id(), self.poll_interval))
            else:
                print("Submitting {}/{}".format(total_input, total_input))
                self.res = requests.post(self.base_url, data={
                    "ids": ",".join(ids[i: total_input]),
                    "from": "UniProtKB_AC-ID",
                    "to": "UniProtKB"
                })
                self.result_url.append(UniprotResultLink(self.check_status_url + self.get_job_id(), self.poll_interval))
        # iterate through result_url and check for result, if result is done, retrieve and yield
        # the text data of the content
        for r in self.get_result():
            yield r.text

    # create params using format, and field names supplied at the start to get result when they are ready
    def get_result(self):
        for res in self.get_result_url():
            base_dict = {
                "format": self.format,
                "size": 500,
                "fields": self.columns,
                "includeIsoform": "true"
            }
            yield requests.get(res+"/", params=base_dict)

    # iterate through the result_url check if a redirection status is given by the url indicating that the result has
    # finished, then yield the finished link and set status of the link as finished. if not, after going through all urls,
    # sleep for the indicated polling time then recheck the urls again until all url has yielded.
    def get_result_url(self):
        complete = len(self.result_url)
        while complete > 0:
            for r in self.result_url:
                if not r.completed:
                    res = r.check_status()
                    if res.status_code == 303:
                        r.completed = True
                        complete = complete - 1
                        yield res.headers["Location"]
                    elif res.status_code == 400:
                        raise "Incorrect URL"
                    else:
                        print("Polling again after {}".format(self.poll_interval))
            time.sleep(self.poll_interval)






