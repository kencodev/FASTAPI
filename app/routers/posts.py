import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, database, models, Oauth2


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schemas.PostResponseWithOwnerAndVotes])
def get_posts(db: Session = Depends(database.get_db),
              current_user: dict = Depends(Oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id)
                       .label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(skip)\
        .all()
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No data")

    return results


# get one post


@router.get("/{id}", response_model=schemas.PostResponseWithOwnerAndVotes)
def get_post(id: int, db: Session = Depends(database.get_db),
             current_user: dict = Depends(Oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id)
                    .label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return post


# Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.postResponse)
def create_post(post: schemas.postCreate, db: Session = Depends(database.get_db),
                current_user: dict = Depends(Oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user['id'], **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete a post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(database.get_db),
                current_user: dict = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post.owner_id != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"forbidden action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post


@router.put("/{id}", response_model=schemas.responseOnUpdate)
def update_post(id: int, post_update: schemas.postUpdate,
                db: Session = Depends(database.get_db),
                current_user: dict = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found")

    if post.owner_id != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"forbidden action")

    post_query.update(dict(**post_update.dict()), synchronize_session=False)

    db.commit()
    db.refresh(post)
    return post
