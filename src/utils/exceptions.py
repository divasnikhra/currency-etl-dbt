class ETLError(Exception):
    """Base exception for ETL failures."""
    pass

class FetchError(ETLError):
    """Raised when API fetch fails."""
    pass

class DBError(ETLError):
    """Raised for database-related errors."""
    pass
