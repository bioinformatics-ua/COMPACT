from pathlib import Path

base_path = Path(__file__).parent
summariesPath = (base_path / "../aux/summaries").resolve()
dstPathOfOriginalSequences = (base_path / "../aux/original_sequences").resolve()
locationOfDatabases = (base_path / "../aux/references").resolve()

dstPathOfDatabaseSequences = (base_path / "../aux/database_sequences").resolve()