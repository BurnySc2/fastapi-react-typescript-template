import React, { useContext } from "react"
import { ContextProvider } from "./ContextProvider"

export default function ContextConsumer(props: any) {
    // @ts-ignore
    let { contextValue, setContextValue } = useContext(ContextProvider)

    console.log(contextValue)

    return (
        <div>
            <div>{contextValue}</div>
            <button
                className={"p-1 border-2"}
                onClick={(e) => {
                    setContextValue(contextValue === "asd" ? "dsa" : "asd")
                }}
            >
                Change data
            </button>
        </div>
    )
}
