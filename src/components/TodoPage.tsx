import React, { useState, useEffect, useContext } from "react"
import Card from "./Card"

const idkContext = React.createContext({ myValue: "Click me!" })

function TodoPage(props: any) {
    const [newTodo, setNewTodo] = useState("")
    const [todos, setTodos] = useState([])

    // Context variable example
    let idkVariable = useContext(idkContext)

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
        idkVariable["myValue"] =
            idkVariable["myValue"] === "Value changed!" ? "Click me!" : "Value changed!"
        /*
        To add optional search params, use:
        let params = new URLSearchParams("")
        params.set("mykey", "myvalue")
        fetch(`/api/${newTodo}?` + params.toString(), requestOptions)
         */
        // When using request body:
        /*
        let requestOptions = {
            method: "POST",
            body: JSON.stringify({
                new_todo: newTodo,
            }),
        }
        fetch("/api", requestOptions)
         */
        await fetch(`/api/${newTodo}`, {
            method: "POST",
        })
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
                    Submit {idkVariable["myValue"]}
                </button>
            </div>
            <Card listOfTodos={todos} removeTodo={removeTodo} />
        </div>
    )
}

export default TodoPage
