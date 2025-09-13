import unittest
from unittest.mock import patch, MagicMock
from src.tools import ExecuteSQLQuery
from typing import Dict, Any

class TestExecuteSQLQuery(unittest.TestCase):
    def setUp(self):
        self.tool = ExecuteSQLQuery()

    @patch('src.tools.sqlite3.connect')
    def test_sqlite_select_query_success(self, mock_connect):
        # Mock SQLite connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1,)]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        query: Dict[str, str] = {'sql': 'SELECT 1'}
        result: Dict[str, Any] = self.tool._run(
            query=query,
            db_path='test.sqlite',
            db_type='sqlite'
        )

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Query executed successfully')
        self.assertEqual(result['data'], [(1,)])
        mock_cursor.execute.assert_called_with('SELECT 1')

    @patch('src.tools.sqlite3.connect')
    def test_sqlite_invalid_query(self, mock_connect):
        # Mock SQLite to raise an exception
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('SQL error')
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        query: Dict[str, str] = {'sql': 'INVALID SQL'}
        result: Dict[str, Any] = self.tool._run(
            query=query,
            db_path='test.sqlite',
            db_type='sqlite'
        )

        self.assertEqual(result['status'], 'error')
        self.assertIn('Error executing query: SQL error', result['message'])
        self.assertIsNone(result['data'])

    @patch('src.tools.psycopg.connect')
    def test_postgres_select_query_success(self, mock_connect):
        # Mock Psycopg connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(2,)]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        query: Dict[str, str] = {'sql': 'SELECT 2'}
        result: Dict[str, Any] = self.tool._run(
            query=query,
            conn_string='test_conn_string',
            db_type='postgres'
        )

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Query executed successfully')
        self.assertEqual(result['data'], [(2,)])
        mock_cursor.execute.assert_called_with('SELECT 2')

    def test_unsupported_db_type(self):
        query: Dict[str, str] = {'sql': 'SELECT 1'}
        result: Dict[str, Any] = self.tool._run(
            query=query,
            db_type='unsupported'
        )

        self.assertEqual(result['status'], 'error')
        self.assertIn('Unsupported db_type', result['message'])

    def test_missing_required_params(self):
        query: Dict[str, str] = {'sql': 'SELECT 1'}
        
        # Missing db_path for sqlite
        result_sqlite = self.tool._run(query=query, db_type='sqlite')
        self.assertEqual(result_sqlite['status'], 'error')
        self.assertIn('SQLite requires db_path', result_sqlite['message'])
        
        # Missing conn_string for postgres
        result_postgres = self.tool._run(query=query, db_type='postgres')
        self.assertEqual(result_postgres['status'], 'error')
        self.assertIn('PostgreSQL requires conn_string', result_postgres['message'])

if __name__ == '__main__':
    unittest.main()
