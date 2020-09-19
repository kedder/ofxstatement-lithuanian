"""Parser implementation for swedbank generated statement reports"""
from typing import List, Optional, Iterable
import re

from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import StatementLine

LINETYPE_TRANSACTION = "20"
LINETYPE_STARTBALANCE = "10"
LINETYPE_ENDBALANCE = "86"

CARD_PURCHASE_RE = re.compile(r"PIRKINYS \d+ (\d\d\d\d\.\d\d\.\d\d) .* \((\d+)\).*")


class SwedbankCsvStatementParser(CsvStatementParser):
    mappings = {"date": 2, "payee": 3, "memo": 4, "amount": 5, "id": 8}

    def split_records(self) -> Iterable[List[str]]:
        # We cannot parse swedbank csv as regular csv because swedbanks format
        # uses unescaped quote symbols.
        for line in self.fin.readlines():
            if not line.strip():
                yield []
                continue
            parts = [p[1:] for p in line.split('",')]
            yield parts

    def parse_record(self, line: List[str]) -> Optional[StatementLine]:
        if not line:
            return None

        if self.cur_record == 1:
            # Skip header line
            return None

        # Split line to the parts and strip quotes around fields
        # parts = [l[1:] for l in line.split('",')]
        parts = line
        if not self.statement.account_id:
            self.statement.account_id = "%s-%s" % (parts[0], self.statement.currency)

        lineType = parts[1]

        if lineType == LINETYPE_TRANSACTION:
            # parse transaction line in standard fasion
            stmtline = super().parse_record(parts)
            if stmtline is None:
                return None
            if parts[7] == "D":
                assert stmtline.amount is not None
                stmtline.amount = -stmtline.amount

            linecur = parts[6]
            if self.statement.currency != linecur:
                # Skip lines with different currency
                return None

            if stmtline.memo:
                m = CARD_PURCHASE_RE.match(stmtline.memo)
                if m:
                    # this is an electronic purchase. extract some useful
                    # information from memo field
                    dt = m.group(1).replace(".", "-")
                    stmtline.date_user = self.parse_datetime(dt)
                    stmtline.check_no = m.group(2)

            return stmtline

        elif lineType == LINETYPE_ENDBALANCE:
            self.statement.end_balance = self.parse_float(parts[5])
            self.statement.end_date = self.parse_datetime(parts[2])

        elif lineType == LINETYPE_STARTBALANCE:
            self.statement.start_balance = self.parse_float(parts[5])
            self.statement.start_date = self.parse_datetime(parts[2])

        return None


class SwedbankPlugin(Plugin):
    """Lithuanian Swedbank CSV"""

    def get_parser(self, fin: str) -> SwedbankCsvStatementParser:
        f = open(fin, "r")
        parser = SwedbankCsvStatementParser(f)
        parser.statement.currency = self.settings.get("currency", "EUR")
        return parser
