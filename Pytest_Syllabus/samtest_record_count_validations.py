import pytest
from sqlalchemy import create_engine
import pandas as pd


# Fixture for database connections
@pytest.fixture(scope="module")
def db_connections():
    # Setup - create database connections
    # Replace with your actual connection details
    source_connection_string="oracle+cx_oracle://hr:hr@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))"
    target_connection_string="oracle+cx_oracle://core:core@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))"
    source_engine = create_engine(source_connection_string)
    target_engine = create_engine(target_connection_string)

    yield {
        "source": source_engine,
        "target": target_engine
    }

    # Teardown - dispose connections
    source_engine.dispose()
    target_engine.dispose()


# Test function to compare record counts
def test_record_counts(db_connections):
    """Test that verifies record counts match between source and target tables."""

    # Configuration - replace with your table names
    test_cases = [
        {"source_table": "EMPLOYEES", "target_table": "EMPLOYEES"},
        {"source_table": "DEPARTMENTS", "target_table": "DEPARTMENTS"},
        {"source_table": "JOBS", "target_table": "JOBS"},
    ]

    for case in test_cases:
        source_table = case["source_table"]
        target_table = case["target_table"]

        # Get source count
        with db_connections["source"].connect() as conn:
            source_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {source_table}", conn).iloc[0]['count']

        # Get target count
        with db_connections["target"].connect() as conn:
            target_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {target_table}", conn).iloc[0]['count']

        # Assert counts match
        assert source_count == target_count, (
            f"Record count mismatch between {source_table} ({source_count}) "
            f"and {target_table} ({target_count})"
        )

'''
# Optional: More detailed comparison with logging
def test_detailed_record_count_comparison(db_connections):
    """Test with more detailed output about the comparison."""

    source_table = "your_source_table"
    target_table = "your_target_table"

    # Get source count
    with db_connections["source"].connect() as conn:
        source_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {source_table}", conn).iloc[0]['count']

    # Get target count
    with db_connections["target"].connect() as conn:
        target_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {target_table}", conn).iloc[0]['count']

    # Print counts for debugging
    print(f"\nSource table '{source_table}' count: {source_count}")
    print(f"Target table '{target_table}' count: {target_count}")

    # Assert counts match
    assert source_count == target_count, (
        f"Record count mismatch: source has {source_count} records, "
        f"target has {target_count} records"
    )'''