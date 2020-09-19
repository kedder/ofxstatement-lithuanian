import os
import datetime
from decimal import Decimal

from ofxstatement.plugins.litas_esis import LitasEsisCsvStatementParser


def test_LitasEsisCsvStatementParser() -> None:

    # Open sample csv to parse
    csvfile = os.path.join(os.path.dirname(__file__), "samples", "litas_esis.acc")

    # Create parser object and parse:
    fin = open(csvfile, "r", encoding="cp1257")
    parser = LitasEsisCsvStatementParser(fin)
    statement = parser.parse()

    # Check what we've got:
    assert statement.account_id == "LT000000000000000000LTL"
    assert len(statement.lines) == 7
    assert statement.start_balance == Decimal("251.75")
    assert statement.start_date == datetime.datetime(2012, 1, 1, 0, 0)
    assert statement.end_balance == Decimal("74.83")
    assert statement.end_date == datetime.datetime(2012, 3, 4, 0, 0)
    assert statement.currency == "LTL"

    # Check first line:
    line = statement.lines[0]
    assert line.amount == Decimal("-1")
    assert line.payee == "AB DNB BANKAS"
    assert line.memo == "Mokestis už sąskaitos aptarnavimą"
    assert line.id == "1987555498"

    # Check credit line:
    line = statement.lines[3]
    assert line.amount == Decimal("300")
    assert line.payee == "LINUS TORVALDS"
    assert line.memo == "Hello World"
    assert line.id == "2003969289"


def test_LitasEsisCsvStatementParser_swap_payee_memo() -> None:
    # Test ability to swap payee and memo in LitasEsisCsvStatementParser

    # Open sample csv to parse
    csvfile = os.path.join(os.path.dirname(__file__), "samples", "litas_esis.acc")

    # Create parser object and parse:
    fin = open(csvfile, "r", encoding="cp1257")
    parser = LitasEsisCsvStatementParser(fin)
    parser.swap_payee_and_memo()
    statement = parser.parse()

    # Memo and payee should be swapped
    line = statement.lines[3]
    assert line.memo == "LINUS TORVALDS"
    assert line.payee == "Hello World"
