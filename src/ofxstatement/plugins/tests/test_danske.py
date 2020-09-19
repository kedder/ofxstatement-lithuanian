import os
import re
import datetime
from decimal import Decimal

from ofxstatement.plugins.danske import DanskeCsvStatementParser


def test_DanskeCsvStatementParser() -> None:
    # Test DanskeCsvStatementParser

    # Open sample csv to parse
    csvfile = os.path.join(os.path.dirname(__file__), "samples", "danske.csv")

    # Create parser and parse
    fin = open(csvfile, "r", encoding="cp1257")
    parser = DanskeCsvStatementParser(fin)
    statement = parser.parse()

    # Check what we've got:
    assert len(statement.lines) == 4
    assert statement.start_balance == Decimal("0")
    assert statement.end_balance == Decimal("0.00")
    assert statement.start_date == datetime.datetime(2012, 3, 1, 0, 0)
    assert statement.end_date == datetime.datetime(2012, 3, 7, 0, 0)

    # First line is a payment for incoming transaction:
    line = statement.lines[0]
    assert line.amount == Decimal("-7.8")
    assert line.memo == (
        "Paslaugų ir komisinių pajamos už gaunamus tarptautinius pervedimus USD"
    )
    assert line.date == datetime.datetime(2012, 3, 1, 0, 0)
    assert line.id == "bef3396a4c86263e911f11a3b10bcc5558064116"

    # Second line is incoming money
    line = statement.lines[1]
    assert line.amount == Decimal("889.81")
    assert line.memo == "ACME LLC"
    assert line.date == datetime.datetime(2012, 3, 1, 0, 0)

    # Third line is a pament with amount less than 1 USD
    line = statement.lines[2]
    assert line.amount == Decimal("-0.46")
    assert line.memo is not None
    assert re.match(
        r"Mokestis už lėšų, gautų iš kitų LR registruotų bankų, .* 2012\.03\.06",
        line.memo,
    )

    # Fourth is a transfer to other account
    line = statement.lines[3]
    assert line.memo == "John Doe"
    assert line.amount == Decimal("-881.55")
