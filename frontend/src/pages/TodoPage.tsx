import React, { useEffect, useState } from 'react'
import TodoItem from '../components/TodoItem'

type ITodoItem = {
    id: number
    content: string
}

export default function TodoPage(): JSX.Element {
    // https://github.com/BurnySc2/fastapi-svelte-template/blob/master/src/components/TodoPage.svelte
    const [newTodoText, setNewTodoText] = useState('')
    const [todos, setTodos] = useState<ITodoItem[]>([])
    const [APIserverIsResponding, setAPIserverIsResponding] = useState(true)

    useEffect(() => {
        getTodos()
    }, [])

    const getTodos = async () => {
        try {
            const response = await fetch(`/api`)
            if (response.ok) {
                setTodos(await response.json())
                setAPIserverIsResponding(true)
                // console.log(`Response is: ${JSON.stringify(cards)}`);
            } else {
                throw new Error(response.statusText)
            }
        } catch {
            setAPIserverIsResponding(false)
        }
    }

    /*
    TODO functions:
    get todos from server, if server unavailable: set APIserverIsResponding = false
    submit pressed via multiple ways, see
    https://github.com/BurnySc2/fastapi-svelte-template/blob/master/src/components/TodoPage.svelte#L72
    https://github.com/BurnySc2/fastapi-svelte-template/blob/master/src/components/TodoPage.svelte#L89

     */

    const submitPressed = async () => {
        /*
        To add optional search params, use:
        let params = new URLSearchParams("")
        params.set("mykey", "myvalue")
        fetch(`/api/${newTodo}?` + params.toString(), requestOptions)
         */
        if (APIserverIsResponding) {
            await fetch(`/api/${newTodoText}`, {
                method: 'POST',
            })
        } else {
            localSubmit()
        }
        setNewTodoText('')
        await getTodos()
    }

    const submitPressedBody = async () => {
        if (APIserverIsResponding) {
            const requestOptions = {
                method: 'POST',
                body: JSON.stringify({
                    new_todo: newTodoText,
                }),
            }
            await fetch(`/api_body`, requestOptions)
        } else {
            localSubmit()
        }
        setNewTodoText('')
        await getTodos()
    }

    const submitPressedModel = async () => {
        if (APIserverIsResponding) {
            const requestOptions = {
                method: 'POST',
                // Otherwise it gets send as binary data?
                headers: {
                    'Content-Type': 'application/json',
                },
                // The expected object model is the same as defined in fastapi - automatic 422 error if it doesn't match the model
                body: JSON.stringify({
                    todo_description: newTodoText,
                }),
            }
            const response = await fetch(`/api_model`, requestOptions)
            if (!response.ok) {
                // If error, then you can debug here and see which fields were missing/expected
                const body = await response.text()
                console.log(body)
            }
        } else {
            localSubmit()
        }
        setNewTodoText('')
        await getTodos()
    }

    const removeTodo = async (id: number) => {
        if (APIserverIsResponding) {
            await fetch(`/api/${id}`, {
                method: 'DELETE',
            })
        } else {
            localRemove(id)
        }
        await getTodos()
    }

    const localSubmit = () => {
        // Add an item to local todolist
        let maxIndex = 0
        todos.forEach((todo) => {
            maxIndex = Math.max(todo.id, maxIndex)
        })
        setTodos([...todos, { id: maxIndex + 1, content: newTodoText }])
        setNewTodoText('')
    }

    const localRemove = (id: number) => {
        // Remove an item from local todolist
        const index = todos.findIndex((obj) => {
            return obj.id === id
        })
        if (index >= 0) {
            setTodos([...todos.slice(undefined, index), ...todos.slice(index + 1)])
        }
    }

    // Render UI
    const todoTextInput = (
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
    )

    const renderTodoItem = (todoItem: ITodoItem, index: number) => {
        return (
            <TodoItem
                index={index}
                id={todoItem.id}
                content={todoItem.content}
                deleteFunction={() => removeTodo(todoItem.id)}
                key={todoItem.id}
            />
        )
    }

    const renderApiServerResponding = APIserverIsResponding ? (
        ''
    ) : (
        <div className="bg-red-300 rounded p-1">Unable to connect to server - running local mode</div>
    )

    return (
        <div>
            <div className="flex flex-col items-center">
                <div className="flex">
                    {todoTextInput}
                    <button className="border-2 my-2 mx-1" id="submit1" onClick={submitPressed}>
                        Submit
                    </button>
                    <button className="border-2 my-2 mx-1" id="submit2" onClick={submitPressedBody}>
                        SubmitBody
                    </button>

                    <button className="border-2 my-2 mx-1" id="submit3" onClick={submitPressedModel}>
                        SubmitModel
                    </button>
                </div>
                {renderApiServerResponding}
            </div>

            <div className="grid grid-cols-1 justify-items-center ">
                <div>{todos.map(renderTodoItem)}</div>
            </div>
        </div>
    )
}
