# Ontario Energy Demand Analytics

**Status: runnable starter. Real-data portfolio results are still to be built.**

Investigate when electricity demand peaks and how demand relates to weather. The first version demonstrates data validation, SQLite queries, and an HTML dashboard.

## Run it in five minutes

Requires Python 3.11 or newer. This starter uses only Python's standard library: no dependency installation, API key, or paid service is needed.

1. Click **Code > Download ZIP** on GitHub and extract it.
2. Open the extracted folder containing `run.py`.
3. Click the Windows File Explorer address bar, type `powershell`, and press Enter.
4. Check Python: `python --version`. If Windows does not find it, try `py --version` and substitute `py` in the commands below. If neither works, install Python from [python.org](https://www.python.org/downloads/) and enable the installer option to add Python to PATH.
5. Run:

```powershell
python run.py --demo
```

Then open `reports/generated/dashboard.html`. Generated files are local outputs and are ignored by Git. The starter's sample results demonstrate the workflow, not research or business findings.

## What works now

- Creates 336 synthetic hourly observations with a fixed random seed.
- Validates timezone-aware hourly timestamps, positive demand, numeric values, and duplicates; reports missing hours without filling them.
- Loads a SQLite database and runs the SQL files in sql/.
- Exports hourly and daily CSV summaries, provenance metadata, and an HTML dashboard.

## First task for you

Inspect `sql/hourly_profile.sql`. Add `ROUND(MIN(demand_mw), 2) AS minimum_demand_mw` to the selected columns. Rerun the demo and check the new column in `reports/generated/hourly_profile.csv`. The existing HTML chart uses the mean, so it should still work.

See [START_HERE.md](START_HERE.md) for a guided session and [ROADMAP.md](ROADMAP.md) for the project milestones.

## Validation

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests and demo on Python 3.11. Tests cover selected failure cases and starter behavior; they do not validate scientific conclusions or portfolio readiness.

## Limitations

No real Ontario observations have been analyzed. This is descriptive analysis, not forecasting. All grouping currently uses UTC. Missing hours can bias comparisons. The HTML dashboard is implemented; a Power BI dashboard is a next milestone.

## Sources and method

See [data sources](docs/DATA_SOURCES.md). Keep a development log of decisions and evidence in [docs/LEARNING_LOG.md](docs/LEARNING_LOG.md). No performance or impact claim should be added to a resume until it is supported by work you can reproduce and explain.
