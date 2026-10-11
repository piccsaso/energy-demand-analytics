import tempfile
from pathlib import Path
import unittest
from src.energy import load_csv, correlation, build_database


class EnergyTests(unittest.TestCase):
    def load(self, body):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'input.csv'
            path.write_text('timestamp,demand_mw,temperature_c\n'+body, encoding='utf-8')
            return load_csv(path)

    def test_duplicate_offsets_refer_to_same_instant(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.load('2025-01-01T00:00:00+00:00,100,1\n2024-12-31T19:00:00-05:00,110,2\n')

    def test_gap_is_reported_not_filled(self):
        rows, checks = self.load('2025-01-01T00:00:00Z,100,1\n2025-01-01T02:00:00Z,120,2\n')
        self.assertEqual(checks['missing_hours'], 1)
        with build_database(rows, ':memory:') as db:
            self.assertEqual(db.execute('SELECT MAX(demand_mw) FROM observations').fetchone()[0],120)

    def test_naive_time_and_nonfinite_numbers_rejected(self):
        for row in ['2025-01-01T00:00:00,100,1', '2025-01-01T00:00:00Z,nan,1']:
            with self.assertRaises(ValueError):
                self.load(row+'\n2025-01-01T01:00:00Z,110,2\n')

    def test_constant_temperature_has_no_correlation(self):
        self.assertIsNone(correlation([('a',100,1),('b',200,1)]))
