from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель для рецепта
class Recipe(BaseModel):
    id: int
    title: str
    ingredients: List[str]
    instructions: str

# Хранилище рецептов
recipes = []

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    # Проверка на уникальность id
    if any(r.id == recipe.id for r in recipes):
        raise HTTPException(status_code=400, detail="Recipe ID already exists")
    recipes.append(recipe)
    return recipe

@app.get("/recipes/", response_model=List[Recipe])
def read_recipes():
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, updated_recipe: Recipe):
    for idx, recipe in enumerate(recipes):
        if recipe.id == recipe_id:
            recipes[idx] = updated_recipe
            return updated_recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@app.delete("/recipes/{recipe_id}", response_model=Recipe)
def delete_recipe(recipe_id: int):
    for idx, recipe in enumerate(recipes):
        if recipe.id == recipe_id:
            return recipes.pop(idx)
    raise HTTPException(status_code=404, detail="Recipe not found")