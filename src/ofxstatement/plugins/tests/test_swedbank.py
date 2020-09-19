import os
import re
import datetime
from decimal import Decimal

from ofxstatement.plugins.swedbank import SwedbankCsvStatementParser


def test_SwedbankCsvStatementParser() -> None:
    # Open sample csv to parse
    csvfile = os.path.join(os.path.dirname(__file__), "samples", "swedbank.csv")

    fin = open(csvfile, "r", encoding="utf-8")
    parser = SwedbankCsvStatementParser(fin)
    parser.statement.currency = "LTL"
    statement = parser.parse()

    # Check what we've got:
    assert statement.account_id == "LT797300010XXXXXXXXX-LTL"
    assert len(statement.lines) == 5
    assert statement.start_balance == Decimal("2123.82")
    assert statement.start_date == datetime.datetime(2012, 1, 1, 0, 0)
    assert statement.end_balance == Decimal("3917.30")
    assert statement.end_date == datetime.datetime(2012, 1, 31, 0, 0)
    assert statement.currency == "LTL"

    # Check first line
    line = statement.lines[0]
    assert line.amount == Decimal("-14.34")
    assert line.payee == "McDonald's restoranas AKR Vilnius"
    assert line.memo is not None
    assert re.match(r"PIRKINYS .* 00000", line.memo)
    assert line.id == "2012010200041787"
    assert line.check_no == "059553"
    assert line.date == datetime.datetime(2012, 1, 2, 0, 0)
    assert line.date_user == datetime.datetime(2011, 12, 30, 0, 0)

    # Check line with awkward quotation marks:
    line = statement.lines[2]
    assert line.id == "2012012600096815"
    assert line.amount == Decimal("-12.20")
    assert line.payee == 'UAB "Naktida"'
    assert line.memo is not None
    assert re.match(r'PIRKINYS 0000000000000000 .* UAB "Naktida" .* 00000', line.memo)

    # Check income line:
    line = statement.lines[3]
    assert line.id == "2012011000673562"
    assert line.amount == Decimal("1600.00")
    assert line.payee == "Company"
    assert line.memo == "Salary"

    # Check line with empty payee:
    line = statement.lines[4]
    assert line.id == "2012022900875660"
    assert line.payee == ""
