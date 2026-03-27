from google.cloud.firestore_v1.pipeline_stages import SearchOptions, Search, QueryEnhancement
from google.cloud.firestore_v1.pipeline_expressions import Field, Ordering, document_matches

def test_search_options():
    options = SearchOptions(
        query="test query",
        limit=10,
        retrieval_depth=2,
        sort=Ordering("score", Ordering.Direction.DESCENDING),
        add_fields=[Field("extra")],
        select=[Field("name")],
        offset=5,
        query_enhancement="disabled",
        language_code="en",
    )
    assert options.limit == 10
    assert options.retrieval_depth == 2
    assert len(options.sort) == 1
    assert options.offset == 5
    assert options.query_enhancement == QueryEnhancement.DISABLED
    assert options.language_code == "en"
    
    # Check proto generation
    stage = Search(options)
    pb_opts = stage._pb_options()
    
    assert pb_opts["limit"].integer_value == 10
    assert pb_opts["retrieval_depth"].integer_value == 2
    assert len(pb_opts["sort"].array_value.values) == 1
    assert pb_opts["offset"].integer_value == 5
    assert pb_opts["query_enhancement"].string_value == "disabled"
    assert pb_opts["language_code"].string_value == "en"

def test_search_options_bool_expr():
    options = SearchOptions(query=document_matches("query string"))
    stage = Search(options)
    pb_opts = stage._pb_options()
    assert "query" in pb_opts

def test_between():
    expr = Field("age").between(18, 65)
    assert expr.name == "between"
    assert len(expr.params) == 3

def test_geo_distance():
    expr = Field("location").geo_distance("other")
    assert expr.name == "geo_distance"
    assert len(expr.params) == 2

def test_document_matches():
    expr = document_matches("search query")
    assert expr.name == "document_matches"
    assert len(expr.params) == 1
