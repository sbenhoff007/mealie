from pydantic import UUID4
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from mealie.schema._mealie import MealieModel

from ...db.models.recipe import RecipeModel, Tool


class RecipeToolCreate(MealieModel):
    name: str
    on_hand: bool = False


class RecipeToolSave(RecipeToolCreate):
    group_id: UUID4


class RecipeToolOut(RecipeToolCreate):
    id: UUID4
    slug: str

    class Config:
        orm_mode = True


class RecipeToolResponse(RecipeToolOut):
    recipes: list["RecipeSummary"] = []

    class Config:
        orm_mode = True

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            selectinload(Tool.recipes).joinedload(RecipeModel.recipe_category),
            selectinload(Tool.recipes).joinedload(RecipeModel.tags),
            selectinload(Tool.recipes).joinedload(RecipeModel.tools),
        ]


from .recipe import RecipeSummary  # noqa: E402

RecipeToolResponse.update_forward_refs()
