import React, { Component, ReactElement } from "react"
import TodoPage from "./components/TodoPage"

class App extends Component {
    render(): ReactElement {
        return (
            <div>
                <TodoPage />
            </div>
        )
    }
}

export default App
