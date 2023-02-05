from .. import database, schemas, Oauth2, models
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Voting, db: Session = Depends(database.get_db),
                current_user: dict = Depends(Oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user["id"])
    vote_present = vote_query.first()
    if (vote.dir == 1):
        if vote_present:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f" user {current_user['id']} has already voted")
        new_vote = models.Vote(post_id=vote.post_id,
                               user_id=current_user["id"])
        db.add(new_vote)
        db.commit()
        return {"message": "vote added succefully"}

    else:
        if not vote_present:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted"}
