import doctest

from ofxstatement.plugins.danske import DanskeCsvStatementParser


def doctest_DanskeCsvStatementParser():
    """Test DanskeCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'danske.csv')


    Create parser and parse
        >>> fin = open(csvfile, 'r', encoding='cp1257')
        >>> parser = DanskeCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> len(statement.lines)
        4
        >>> statement.start_balance
        Decimal('0')
        >>> statement.end_balance
        Decimal('0.00')
        >>> statement.start_date
        datetime.datetime(2012, 3, 1, 0, 0)
        >>> statement.end_date
        datetime.datetime(2012, 3, 7, 0, 0)

    First line is a payment for incoming transaction:
        >>> l = statement.lines[0]
        >>> l.amount
        Decimal('-7.8')
        >>> l.memo
        'Paslaugų ir komisinių pajamos už gaunamus tarptautinius pervedimus USD'
        >>> l.date
        datetime.datetime(2012, 3, 1, 0, 0)
        >>> l.id
        'bef3396a4c86263e911f11a3b10bcc5558064116'

    Second line is incoming money
        >>> l = statement.lines[1]
        >>> l.amount
        Decimal('889.81')
        >>> l.memo
        'ACME LLC'
        >>> l.date
        datetime.datetime(2012, 3, 1, 0, 0)

    Third line is a pament with amount less than 1 USD
        >>> l = statement.lines[2]
        >>> l.amount
        Decimal('-0.46')
        >>> l.memo
        'Mokestis už lėšų, gautų iš kitų LR registruotų bankų, ... 2012.03.06'

    Fourth is a transfer to other account
        >>> l = statement.lines[3]
        >>> l.memo
        'John Doe'
        >>> l.amount
        Decimal('-881.55')
    """


def test_suite(*args):
    return doctest.DocTestSuite(
        optionflags=(
            doctest.NORMALIZE_WHITESPACE
            | doctest.ELLIPSIS
            | doctest.REPORT_ONLY_FIRST_FAILURE
            | doctest.REPORT_NDIFF
        )
    )


load_tests = test_suite
