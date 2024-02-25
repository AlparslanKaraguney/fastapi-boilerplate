from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
    Request,
)
from app.services.note.schemas import NoteCreate
from app.core.db.session import db

from .models import Note, Todo

router = APIRouter(prefix="/note", tags=["note"])


@router.post(
    "/create",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Note successfully created",
            "content": {
                "application/json": {"example": "Note 'anytitle' created"}
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Note already exists",
            "content": {
                "application/json": {"example": "This note is already created"}
            },
        },
    },
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    request_body: NoteCreate,
    request: Request,
    response: Response,
):
    """Create new note
    - Check if the note exists
    - Save in DB
    return: Confirmation OR denial
    """
    id = 0
    # Check if the note exists
    if Note.get_one(key=Note.title, value=request_body.title):
        raise HTTPException(
            status_code=400, detail="This note is already created"
        )

    # Save the new note
    note: Note = Note(
        title=request_body.title, description=request_body.description
    ).save()
    db.refresh(note)
    id = note.id

    todo: Todo = Todo(note_id=id, order=1).save()

    response.status_code = status.HTTP_201_CREATED
    return f"Note '{todo.order}' created"


@router.get(
    "/list",
    responses={
        status.HTTP_200_OK: {
            "description": "List of notes",
            "content": {
                "application/json": {
                    "example": [
                        {"title": "anytitle", "desctiption": "anydesctiption"}
                    ]
                }
            },
        }
    },
    status_code=status.HTTP_200_OK,
)
def list_notes():
    """List all notes"""
    return Note.get_all()


@router.get(
    "/get/{note_id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Note found",
            "content": {
                "application/json": {
                    "example": {
                        "title": "anytitle",
                        "desctiption": "anydesctiption",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Note not found",
            "content": {"application/json": {"example": "Note not found"}},
        },
    },
    status_code=status.HTTP_200_OK,
)
def get_note(note_id: int):
    """Get note by ID"""
    note: Note = Note.get_one(key=Note.id, value=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete(
    "/delete/{note_id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Note successfully deleted",
            "content": {
                "application/json": {"example": "Note 'anytitle' deleted"}
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Note not found",
            "content": {"application/json": {"example": "Note not found"}},
        },
    },
    status_code=status.HTTP_200_OK,
)
def delete_note(note_id: int):
    """Delete note by ID"""
    note: Note = Note.get_one(key=Note.id, value=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.delete()
    return f"Note '{note.title}' deleted"
