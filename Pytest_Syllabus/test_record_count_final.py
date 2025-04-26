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


# Define the table pairs to test
TABLE_PAIRS = [
    ("EMPLOYEES", "EMPLOYEES"),
    ("DEPARTMENTS", "DEPARTMENTS"),
    ("JOBS", "JOBS")
    # Add more table pairs as needed
]


@pytest.mark.parametrize("source_table,target_table", TABLE_PAIRS)
def test_record_counts(db_connections, source_table, target_table):
    """Test that verifies record counts match between source and target tables.

    This test will run once for each table pair defined in TABLE_PAIRS.
    Each pair will be reported as a separate test case.
    """
    # Get source count
    with db_connections["source"].connect() as conn:
        source_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {source_table}", conn).iloc[0]['count']

    # Get target count
    with db_connections["target"].connect() as conn:
        target_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {target_table}", conn).iloc[0]['count']

    # Print counts for debugging (only shown on failure with -v flag)
    print(f"\nComparing {source_table} (source) vs {target_table} (target):")
    print(f"Source count: {source_count}")
    print(f"Target count: {target_count}")

    # Assert counts match
    assert source_count == target_count, (
        f"Record count mismatch between {source_table} ({source_count}) "
        f"and {target_table} ({target_count})"
    )

'''
# Optional: Add a test that verifies all expected tables exist
def test_verify_tables_exist(db_connections):
    """Verify that all tables defined in TABLE_PAIRS exist in their respective databases."""
    missing_tables = []

    # Check source tables
    with db_connections["source"].connect() as conn:
        existing_source_tables = pd.read_sql(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'",
            conn
        )['table_name'].tolist()

    # Check target tables
    with db_connections["target"].connect() as conn:
        existing_target_tables = pd.read_sql(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'",
            conn
        )['table_name'].tolist()

    # Verify all tables exist
    for source_table, target_table in TABLE_PAIRS:
        if source_table not in existing_source_tables:
            missing_tables.append(f"Source table '{source_table}' does not exist")
        if target_table not in existing_target_tables:
            missing_tables.append(f"Target table '{target_table}' does not exist")

    if missing_tables:
        pytest.fail("\n".join(missing_tables))'''