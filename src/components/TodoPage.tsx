import React, { useState, useEffect } from "react"
import Card from "./Card"
import ContextConsumer from "./ContextConsumer"
import { ContextProvider } from "./ContextProvider"

function TodoPage(props: any) {
    const [newTodo, setNewTodo] = useState("")
    const [todos, setTodos] = useState([])
    // Context variable example
    const [contextValue, setContextValue] = useState("some text")
    console.log(contextValue)

    useEffect(() => {
        getTodos()
    }, [])

    let getTodos = async () => {
        let response = await fetch("/api")
        if (response.ok) {
            setTodos(await response.json())
        } else {
            // @ts-ignore
            setTodos([{ id: 0, content: "SERVER ERROR" }])
        }
    }

    let submitPressed = async () => {
        /*
        To add optional search params, use:
        let params = new URLSearchParams("")
        params.set("mykey", "myvalue")
        fetch(`/api/${newTodo}?` + params.toString(), requestOptions)
         */
        await fetch(`/api/${newTodo}`, {
            method: "POST",
        })
        setNewTodo("")
        await getTodos()
    }

    let submitPressedBody = async () => {
        // When using request body:
        let requestOptions = {
            method: "POST",
            body: JSON.stringify({
                new_todo: newTodo,
            }),
        }
        fetch("/api_body", requestOptions)
        setNewTodo("")
        await getTodos()
    }

    let submitPressedModel = async () => {
        // When using request body:
        let requestOptions = {
            method: "POST",
            body: JSON.stringify({
                todo_description: newTodo,
            }),
        }
        fetch("/api_model", requestOptions)
        setNewTodo("")
        await getTodos()
    }

    let removeTodo = async (id: number) => {
        await fetch(`/api/${id}`, {
            method: "DELETE",
        })
        await getTodos()
    }

    return (
        <div className="flex flex-col">
            <ContextProvider.Provider
                // @ts-ignore
                value={{ contextValue, setContextValue }}
            >
                <ContextConsumer />
            </ContextProvider.Provider>
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
                <button onClick={submitPressedBody} className="border-2 my-2 mx-1">
                    SubmitBody
                </button>
                <button onClick={submitPressedModel} className="border-2 my-2 mx-1">
                    SubmitModel
                </button>
            </div>
            <Card listOfTodos={todos} removeTodo={removeTodo} />
        </div>
    )
}

export default TodoPage
