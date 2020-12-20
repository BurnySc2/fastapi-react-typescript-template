import React from "react"

function Card(props: any) {
    let cssClass = "flex flex-row"
    return (
        <div>
            {props.listOfTodos &&
                props.listOfTodos.map((todo: any) => {
                    return (
                        <ul key={todo.id} className={cssClass}>
                            <button className="m-2" onClick={() => props.removeTodo(todo.id)}>
                                Remove
                            </button>
                            <li className="m-2">{todo.content}</li>
                        </ul>
                    )
                })}
        </div>
    )
}

export default Card
