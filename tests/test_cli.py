import os

from click.testing import CliRunner
from uniprotparser.cli import main
from uuid import uuid4

class TestCli:
    def test_main(self):
        runner = CliRunner()
        filename = f"{uuid4()}.dat"
        output = f"{uuid4()}.dat"
        with open(filename, "wt") as f:
            f.write("P04637")
        result = runner.invoke(main, ["-i",filename,
                                      "-o", output])
        with open(output, "rt") as f:
            print(f.read())
        os.remove(filename)
        os.remove(output)
        assert result.exit_code == 0

