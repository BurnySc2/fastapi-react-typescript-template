import React from "react"

function Card(props: any) {
    let cssClass = "flex flex-row"
    let cssButton = "m-1 p-1 border-2"
    let cssTodoDescription = "m-1 p-1"
    return (
        <div>
            {props.listOfTodos &&
                props.listOfTodos.map((todo: any) => {
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
