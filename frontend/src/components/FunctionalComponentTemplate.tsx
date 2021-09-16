import React, { useState } from "react"

export default function FunctionalComponentTemplate(props: any) {
    const [variable, setVariable] = useState("")

    const myFunction = () => {
        console.log("Hello world!")
    }

    return <div></div>
}
