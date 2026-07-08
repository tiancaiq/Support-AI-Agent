import tempfile
import unittest
from pathlib import Path

from agent.tools.report_data import (
    load_external_data,
    validate_month,
    validate_user_id,
)


class ReportDataTest(unittest.TestCase):
    def test_validate_user_id_accepts_numeric_string(self):
        self.assertEqual(validate_user_id("1001"), "1001")

    def test_validate_user_id_rejects_non_numeric_string(self):
        with self.assertRaises(ValueError):
            validate_user_id("abc")

    def test_validate_month_requires_year_month_format(self):
        self.assertEqual(validate_month("2025-06"), "2025-06")
        with self.assertRaises(ValueError):
            validate_month("2025/06")

    def test_load_external_data_uses_csv_headers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "records.csv"
            path.write_text(
                '"user_id","profile","cleaning_efficiency","consumables","comparison","time"\n'
                '"1001","65 sqm apartment","coverage:90 percent","filter:good","above peer average","2025-06"\n',
                encoding="utf-8",
            )

            data = load_external_data(str(path))

        self.assertEqual(data["1001"]["2025-06"]["profile"], "65 sqm apartment")
        self.assertEqual(data["1001"]["2025-06"]["cleaning_efficiency"], "coverage:90 percent")


if __name__ == "__main__":
    unittest.main()
