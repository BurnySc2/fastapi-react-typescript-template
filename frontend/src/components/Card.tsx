import React, { ReactElement } from 'react'

function Card(props: {
    listOfTodos: { id: number; content: string }[]
    removeTodo: (id: number) => void
}): ReactElement {
    const cssClass = 'flex flex-row'
    const cssButton = 'm-1 p-1 border-2'
    const cssTodoDescription = 'm-1 p-1'
    return (
        <div>
            {props.listOfTodos &&
                props.listOfTodos.map((todo) => {
                    return (
                        <ul key={todo.id} className={cssClass}>
                            <button className={cssButton} onClick={() => props.removeTodo(todo.id)}>
                                Remove
                            </button>
                            <li className={cssTodoDescription}>{todo.content}</li>
                        </ul>
                    )
                })}
        </div>
    )
}

export default Card
