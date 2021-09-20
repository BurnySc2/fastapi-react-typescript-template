import React from 'react'

interface IProps {
    index: number
    id: number
    content: string
    deleteFunction: () => void
}

export default function TodoItem({ index, id, content, deleteFunction }: IProps): JSX.Element {
    return (
        <div>
            <div>{index + 1})</div>
            <button onClick={deleteFunction}>Delete</button>
            <div>{id})</div>
            <div>{content}</div>
        </div>
    )
}
