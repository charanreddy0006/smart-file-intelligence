def test_search_empty_query():
    from app.search.engine import search_files
    assert search_files("") == []
