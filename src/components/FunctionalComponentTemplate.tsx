import React, { useState } from "react"

export default function FunctionalComponentTemplate(props: any) {
    let [variable, setVariable] = useState("")

    let myFunction = () => {
        console.log("Hello world!")
    }

    return <div></div>
}
