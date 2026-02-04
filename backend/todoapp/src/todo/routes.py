from fastapi import APIRouter, Depends,HTTPException,status
from .schemas import Newtodo
from core.dependency import get_current_user
from core.db import get_db
from sqlmodel import select,Session
from auth.models import User
from todo.models import todotable

todo_route = APIRouter(prefix="/todo",tags=["todo"])


@todo_route.get("/todotest")
def todo_test():
    return {"msg" : "Success from todo test"}


@todo_route.post("/newtodo")
async def create_new_todo(new_todo: Newtodo,user = Depends(get_current_user),db : Session = Depends(get_db)):
    print(f"user we got in the route is {user}")
    print(f"user id we got in the route is {user.id}")
    is_user_exists = db.exec(select(User).where(User.id == user.id)).first()
    print(f"create_new_todo --> is_user_exists {is_user_exists}")
    if not is_user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user does not exists")
    
    add_todo = todotable(todo=new_todo.todo,user_id=user.id)
    db.add(add_todo)
    db.commit()
    db.refresh(add_todo)
    
    print(f"new todo {add_todo}")
    
    return {"msg" : "done"}


@todo_route.get("/getalltodo")
def get_all_todos(user = Depends(get_current_user),db : Session = Depends(get_db)):
    user_id = user.id
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    all_todos = db.exec(select(todotable).where(todotable.user_id == user_id)).all()
    print(f"get_all_todos  --> all_todos {all_todos}")
    
    return {"msg" : all_todos}

@todo_route.delete("/deletetodo/{todo_id}")
def delete_todo(todo_id : int,user = Depends(get_current_user),db : Session = Depends(get_db)):
    
    is_todo_avaialbe = db.exec(select(todotable).where(todotable.id == todo_id,todotable.user_id == user.id)).first()
    if not is_todo_avaialbe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="todo not exists")
    
    print(f"delete_todo --> is_todo_avaialbe {is_todo_avaialbe}")
    
    db.delete(is_todo_avaialbe)
    db.commit()
    
    return {"msg" : "success"}



@todo_route.patch("/markdone/{todo_id}")
def mark_done(todo_id : int,user = Depends(get_current_user),db : Session = Depends(get_db)):
    error = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="todo not exists")
    todo = db.exec(select(todotable).where(todotable.id == todo_id,todotable.user_id == user.id)).first()
    if not todo:
        raise error
    
    print(f"mark_done  --> is_todo_avaialbe {todo}")
    todo.is_done = True
    print(f"mark_done  --> updated_todo {todo}")
    db.commit()
    db.refresh(todo)
    return {"msg" : "done"}
    
    
@todo_route.patch("/marknotdone/{todo_id}")
def mark_notdone(todo_id : int,user = Depends(get_current_user),db : Session = Depends(get_db)):
    error = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="todo not exists")
    todo = db.exec(select(todotable).where(todotable.id == todo_id,todotable.user_id == user.id)).first()
    if not todo:
        raise error
    
    print(f"mark_done  --> is_todo_avaialbe {todo}")
    todo.is_done = False
    print(f"mark_done  --> updated_todo {todo}")
    db.commit()
    db.refresh(todo)
    return {"msg" : "done"}




@todo_route.patch("/edittodo")
def edit_todo(updated_todo : todotable,user = Depends(get_current_user),db : Session = Depends(get_db)):
    
    error = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="todo not found")
    
    todo = db.exec(select(todotable).where(todotable.id == updated_todo.id,todotable.user_id == user.id)).first()
    if not todo:
        raise error
    
    todo.todo = updated_todo.todo
    print(f"edit_todo --called --edit_todo {updated_todo}")
    print(f"edit_todo --called --user {user}")
    print(f"edit_todo --called --todo {todo}")
    db.commit()
    db.refresh(todo)
    return {"msg" : "done"}


    