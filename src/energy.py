"""Validated CSV -> SQLite -> SQL summaries. Standard library only."""
import csv
from datetime import datetime, timezone
import math
from pathlib import Path
import sqlite3


def load_csv(path):
    rows, seen = [], set()
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        required = {'timestamp', 'demand_mw', 'temperature_c'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('CSV needs timestamp, demand_mw, temperature_c columns.')
        for line, r in enumerate(reader, 2):
            try:
                stamp = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00'))
                if stamp.tzinfo is None:
                    raise ValueError('timestamp needs a UTC offset')
                stamp = stamp.astimezone(timezone.utc)
                demand, temp = float(r['demand_mw']), float(r['temperature_c'])
                if not math.isfinite(demand) or not math.isfinite(temp) or demand <= 0:
                    raise ValueError('demand must be positive and both numbers finite')
                if stamp.minute or stamp.second or stamp.microsecond:
                    raise ValueError('timestamps must fall on whole hours')
                if stamp in seen:
                    raise ValueError('duplicate timestamp')
                seen.add(stamp)
                rows.append((stamp.isoformat(), demand, temp))
            except (ValueError, TypeError) as e:
                raise ValueError(f'Line {line}: {e}') from e
    if len(rows) < 2:
        raise ValueError('Need at least two hourly observations.')
    rows.sort()
    gaps = sum(int((datetime.fromisoformat(b[0])-datetime.fromisoformat(a[0])).total_seconds()/3600)-1
               for a, b in zip(rows, rows[1:]))
    return rows, {'rows': len(rows), 'missing_hours': gaps}


def build_database(rows, path):
    conn = sqlite3.connect(path)
    conn.execute('DROP TABLE IF EXISTS observations')
    conn.execute('CREATE TABLE observations (timestamp TEXT PRIMARY KEY, demand_mw REAL NOT NULL, temperature_c REAL NOT NULL)')
    conn.executemany('INSERT INTO observations VALUES (?, ?, ?)', rows)
    conn.commit()
    return conn


def correlation(rows):
    xs, ys = [r[2] for r in rows], [r[1] for r in rows]
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    denominator = math.sqrt(sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/denominator if denominator else None
