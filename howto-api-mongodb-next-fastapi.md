# FastAPI backend + MongoDB + Next.js

Install FastAPI Package

```sh
pip install fastapi unicorn pymongo
```

Fast API Backend
```py
// main.py
from fastapi import FastAPI, HTTPEexception
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# Allow Next.js frontend to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client["demo_db"]
users_collection = db["Users"]

class User(BaseModel);
    userid: str
    fname: str
    lname: str

@app.get("/api/users")
def get_users();
    users = list(users_collection.find({}, {"_id": 0}))
    return users

@app.post("/api/users")
def add_user(user: User)
    existing_user = users_collection.find_one({"userid":user.userid})

    if existing_user:
        raise HTTPExeception(status_code=400, detail="User already exists")
        users_collection.insert_one(user.model_dump())
        return {"message": "User added sucessfully"}

@app.put("/api/users/{userid}")
def update_user(userid: str, user: User):
    result = users_collection.update_one(
        {"userid": userid},
        {"$set": {
            "fname": user.fname,
            "lname": user.lname,
        }}
    )

    if result.matched_count == 0:
        raise HTTPExecption(status_code == 404, detail="User not found")
        return {"message": "User updated sucessfully"}

    @app.delete("/api/users/{userid}")
    def delete_user(userid: str):
        result = users_collection.delete_one({"userid": userid})

    if result.delete_count == 0:
        raise HTTPException(status_code == 404, detail="User not found")
        return {"message": "User deleted sucessfully"}
```

## Run FastAPI
```sh
uvicorn main:app --reload --port 5000
```

### API URL:
```sh
http://localhost:5000/api/users
```

### Swagger UI
```sh
http://localhost:5000/docs
```

## Next.js Frontend
You can keep the same smaller component structure:
```sh
app/
├── page.jsx
└── components/
    ├── UserManager.jsx
    ├── UserForm.jsx
    └── UserTable.jsx
```

# Parent Component
```jsx
# app/components/UserManager.jsx
"user client"

import {useEffect, useState} from "react";
import UserForm from "./UserForm";
import UserTable from "./UserTable";

const API_URL = "http://localhost:5000/api/users";

export default function UserManager() {
    const [users, setUsers] = useState([]);
    const [editingUser, setEditingUser] = useState(null);

    useEffect(() => {
        loadUsers();
    }, []);

    async function loadUsers() {
        const response = await fetch(API_URL);
        const data = await response.json();
        setUsers(data);
    }

    async function handleSave(user) {
        if (editingUser) {
            await fetch(`${API_URL}/${user.userid}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            });
        } else {
            await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            }); 
        }

        setEditingUser(null);
        loadUsers();
    }

    async function handleDelete(userid) {
        await fetch(`${API_URL}/${userid}`, {
            method: "DELETE",
        });

        loadUsers();
    }

    return (
        <div>
            <h2>User CRUD</h2>

            <UserForm
                onSave={handleSave}
                editingUser={editingUser}
                onCancel={() => setEditingUser(null)}
            />

            <UserTable
                users={users}
                onEdit={setEditingUser}
                onDelete={handleDelete}
            />
        </div>
    );
}
```

# Form Component
```jsx
# app/components/UserForm.jsx
"user client";

import { useEffect, useState } from "react";

const emptyForm = {
    userid: "",
    fname: "",
    lname: "",
}

export default function UserForm({ onSave, editingUser, onCancel }) {
    const [from, setForm] = useState(emptyForm);

    useEffect(() => {
        if (editingUser) {
            setForm(editingUser);
        } else {
            setform(emptyForm)
        }
    }, [editingUser]);

    function handleChange(event) {
        setForm({
            ...form,
            [event.target.name]: event.target.value,
        });
    }

    function handleSubmit(event) {
        event.preventDefault();
        onSave(form);
        setForm(emptyForm);
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                name="userid"
                placeholder="User ID"
                value={form.userid}
                onChange={handleChange}
                disabled={!!editingUser}
                required
            />

            <input
                name="fname"
                placeholder="First Name"
                value={form.fname}
                onChange={handleChange}
                required
            />

            <input
                name="lname"
                placeholder="Last Name"
                value={form.lname}
                onChange={handleChange}
                required
            />

            <button type="submit">
                {editingUser ? "Update User" : "Add User"}
            </button>

            {editingUser && (
                <button type="button" onClick={onCancel}>
                    Cancel
                </button>
            )}
        </form>
    );
}
```
# Table Component
```jsx
# app/components/UserTable.jsx
"use client"

export default function UserTable({ users, onEdit, onDelete }) {
    return (
        <table border="1" cellPadding="8">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                {users.map((user) => (
                    <tr key={user.userid}>
                        <td>{user.userid}</td>
                        <td>{user.fname}</td>
                        <td>{user.lname}</td>
                        <td>
                            <button onClick={() => onEdit(user)}>Edit</button>
                            <button onClick={() => onDelete(user.userid)}>
                                Delete
                            </button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
```

# Next.js Page
```jsx
# app/page.jsx
import UserManager from "./components/UserManager";

export default function HomePage() {
    return (
        <main>
            <h1> Next.js + FastAPI + MongoDB Users CRUD</h1>
            <UserManager />
        </main>
    )
}
```

# MongoDB Record Example
```json
{
    "userid": "1001",
    "fname": "John",
    "lname": "Smith"
}
```