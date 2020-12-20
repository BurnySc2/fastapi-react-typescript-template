import React, { useState, useEffect } from "react"
import Card from "./Card"

function TodoPage(props: any) {
    const [newTodo, setNewTodo] = useState("")
    const [todo, setTodo] = useState([])

    useEffect(() => {
        getTodos()
    }, [])

    let getTodos = () => {
        fetch("/api/get")
            .then((response) => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then((data) => {
                setTodo(data)
            })
    }

    let submitPressed = () => {
        let requestOptions = {
            method: "POST",
            header: { "Content-Type": "application/json" },
            body: JSON.stringify({
                new_todo: newTodo,
            }),
        }
        fetch("/api/create", requestOptions)
            .then((response) => {
                if (response.ok) {
                    console.log("create response", response)
                }
            })
            .then((data) => {
                console.log("received create", data)
                // Update todos list
                getTodos()
            })
    }

    let removeTodo = (id: number) => {
        console.log("Removing todo:", id)
        let requestOptions = {
            method: "DELETE",
            header: { "Content-Type": "application/json" },
            body: JSON.stringify({
                remove_todo_id: id,
            }),
        }
        fetch("/api/delete", requestOptions)
            .then((response) => {
                if (response.ok) {
                    console.log("remove response", response)
                }
            })
            .then((data) => {
                console.log("received remove", data)
                // Update todos list
                getTodos()
            })
    }

    return (
        <div className="flex flex-col">
            <div className="flex flex-row">
                <input
                    type="text"
                    value={newTodo}
                    onChange={(e) => {
                        setNewTodo(e.target.value)
                    }}
                    className="border-2"
                />
                <button onClick={submitPressed} className="border-2">
                    Submit
                </button>
            </div>
            <Card listOfTodos={todo} removeTodo={removeTodo} />
        </div>
    )
}

export default TodoPage
