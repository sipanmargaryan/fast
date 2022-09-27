from pathlib import Path

from fastapi import APIRouter, status

from .schema import GenerateUserVectorRequest, UpdateUserVectorRequest, UserVector
from .utils import InterestVector

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/update-user-vector", status_code=status.HTTP_200_OK, response_model=UserVector)
async def update_user_vector(data: UpdateUserVectorRequest) -> UserVector:
    interest_vector = InterestVector(Path("app/categories/categories_dict.json"))
    vector = interest_vector.get_updated_vector(data.user_id, data.content_id, data.update_type)
    return UserVector(vector=vector)


@router.post("/generate-user-vector", status_code=status.HTTP_200_OK, response_model=UserVector)
async def generate_user_vector(data: GenerateUserVectorRequest) -> UserVector:
    interest_vector = InterestVector(Path("app/categories/categories_dict.json"))
    vector = interest_vector.create_vector(data.categories)
    return UserVector(vector=vector)
