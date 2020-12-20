import React, { useState, useEffect } from "react"
import Card from "./Card"

function TodoPage(props: any) {
    const [newTodo, setNewTodo] = useState("")
    const [todos, setTodos] = useState([])

    useEffect(() => {
        getTodos()
    }, [])

    let getTodos = () => {
        fetch("/api")
            .then((response) => {
                if (response.ok) {
                    return response.json()
                }
                // TODO Better error handling when server is offline
                else
                    return [
                        {
                            id: 0,
                            content: "SERVER ERROR",
                        },
                    ]
            })
            .then((data) => {
                setTodos(data)
            })
    }

    let submitPressed = () => {
        let requestOptions = {
            method: "POST",
        }
        fetch(`/api/${newTodo}`, requestOptions)
        // When using request body:
        // let requestOptions = {
        //     method: "POST",
        //     body: JSON.stringify({
        //         new_todo: newTodo,
        //     }),
        // }
        // fetch("/api", requestOptions)
        setNewTodo("")
        getTodos()
    }

    let removeTodo = (id: number) => {
        let requestOptions = {
            method: "DELETE",
        }
        fetch(`/api/${id}`, requestOptions)
        getTodos()
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
                    placeholder="My new todo item"
                    className="border-2 my-2 mx-1"
                />
                <button onClick={submitPressed} className="border-2 my-2 mx-1">
                    Submit
                </button>
            </div>
            <Card listOfTodos={todos} removeTodo={removeTodo} />
        </div>
    )
}

export default TodoPage
