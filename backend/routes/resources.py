from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models.user import User
from backend.models.resource import LearningResource
from backend.models.bookmark import Bookmark
from backend.schemas import ResourceResponse, BookmarkCreateRequest
from backend.services.auth import get_current_user, get_optional_current_user

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("", response_model=List[ResourceResponse])
def get_resources(
    skill: Optional[str] = Query(None, description="Filter by skill_code"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search keyword in title/desc"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    query = db.query(LearningResource)
    if skill:
        query = query.filter(LearningResource.skill_code == skill.lower())
    if category:
        query = query.filter(LearningResource.category.ilike(f"%{category}%"))
    if difficulty:
        query = query.filter(LearningResource.difficulty.ilike(f"%{difficulty}%"))
    if search:
        query = query.filter(
            (LearningResource.title.ilike(f"%{search}%")) | 
            (LearningResource.description.ilike(f"%{search}%"))
        )

    resources = query.all()

    bookmarked_ids = set()
    if current_user:
        bms = db.query(Bookmark.resource_id).filter(Bookmark.user_id == current_user.id).all()
        bookmarked_ids = {b[0] for b in bms}

    result = []
    for r in resources:
        item = ResourceResponse.model_validate(r)
        item.is_bookmarked = r.id in bookmarked_ids
        result.append(item)
    return result

@router.post("/bookmark", status_code=status.HTTP_201_CREATED)
def toggle_bookmark(
    req: BookmarkCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.resource_id == req.resource_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"status": "unbookmarked", "resource_id": req.resource_id}
    else:
        new_bm = Bookmark(
            user_id=current_user.id,
            resource_id=req.resource_id,
            notes=req.notes
        )
        db.add(new_bm)
        db.commit()
        return {"status": "bookmarked", "resource_id": req.resource_id}

@router.get("/bookmarks", response_model=List[ResourceResponse])
def get_user_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
    res_list = []
    for bm in bookmarks:
        r = bm.resource
        if r:
            item = ResourceResponse.model_validate(r)
            item.is_bookmarked = True
            res_list.append(item)
    return res_list
