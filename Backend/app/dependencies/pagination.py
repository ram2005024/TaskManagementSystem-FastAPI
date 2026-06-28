from fastapi import Query

def pagination(page:int=Query(1,ge=1,description="Page number"),
    limit:int=Query(10,ge=1,le=100,description="Limit per page")):

    return {
        "page":page,
        "limit":limit
    }
