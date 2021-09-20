import React, { useState } from "react"
import TodoItem from "../components/TodoItem"

export interface ITodoItem {
    id: number
    content: string
}

export default function TodoPage(): JSX.Element {
    // https://github.com/BurnySc2/fastapi-svelte-template/blob/master/src/components/TodoPage.svelte
    const [newTodoText, setNewTodoText] = useState("")
    const [todos, setTodos] = useState<ITodoItem[]>([])
    const APIserverIsResponding = true

    const localSubmit = () => {
        // Add an item if server isnt responding
        let maxIndex = 0
        todos.forEach((todo) => {
            maxIndex = Math.max(todo.id, maxIndex)
        })
        maxIndex += 1
        setTodos([...todos, { id: maxIndex, content: newTodoText }])
        setNewTodoText("")
    }

    const localRemove = (id: number) => {
        // Remove an item if server isnt responding
        const obj = todos.find((obj) => {
            return obj.id === id
        })
        if (obj) {
            const index = todos.indexOf(obj)
            if (index >= 0) {
                setTodos([...todos.slice(undefined, index), ...todos.slice(index + 1)])
            }
        }
    }

    const todos_jsx: JSX.Element[] = todos.map((todoItem, index) => {
        return (
            <TodoItem
                index={index}
                id={todoItem.id}
                content={todoItem.content}
                deleteFunction={() => localRemove(todoItem.id)}
                key={todoItem.id}
            />
        )
    })

    return (
        <div className="flex flex-col items-center">
            <div className="flex">
                <input
                    id="newTodoInput"
                    className="border-2 my-2 mx-1"
                    type="text"
                    onChange={(e) => {
                        setNewTodoText(e.target.value)
                    }}
                    value={newTodoText}
                    placeholder="My new todo item"
                />
                <button className="border-2 my-2 mx-1" id="submit1" onClick={localSubmit}>
                    Submit
                </button>
                {/*<button className="border-2 my-2 mx-1" id="submit2" on:click={submitPressedBody}*/}
                {/*    >SubmitBody</button*/}
                {/*>*/}
                {/*<button className="border-2 my-2 mx-1" id="submit3" on:click={submitPressedModel}*/}
                {/*    >SubmitModel</button*/}
            </div>
            {APIserverIsResponding ? "server responding" : "server not respondingg"}
            {todos_jsx}
        </div>
    )
}
