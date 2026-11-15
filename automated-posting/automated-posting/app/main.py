from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import post_to_all_platforms

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="Publish one message to multiple connected platforms.",
    version="1.0.0",
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest) -> PostingResponse:
    results = await post_to_all_platforms(request.message)
    # Overall success means at least one platform accepted the post.
    any_success = any(result.status == "success" for result in results)
    return PostingResponse(success=any_success, results=results)
