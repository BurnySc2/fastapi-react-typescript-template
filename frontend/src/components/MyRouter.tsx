import React from 'react'
import { HashRouter, Switch, Route, Link } from 'react-router-dom'
import About from '../pages/About'
import Chat from '../pages/Chat'
import TodoPage from '../pages/TodoPage'
import HomePage from '../pages/Home'

export default function MyRouter(): JSX.Element {
    return (
        <HashRouter>
            <div>
                {/*Links in header*/}
                <div className="flex justify-center my-2">
                    <Link className="mx-2 p-1 border-2" to="/">
                        Home
                    </Link>
                    <Link className="mx-2 p-1 border-2" to="/about">
                        About
                    </Link>
                    <Link className="mx-2 p-1 border-2" to="/chat">
                        Chat
                    </Link>
                    <Link className="mx-2 p-1 border-2" to="/todo">
                        Todo
                    </Link>
                </div>

                {/*What to display based on current page path*/}
                <Switch>
                    <Route path="/about">
                        <About />
                    </Route>
                    <Route path="/chat">
                        <Chat />
                    </Route>
                    <Route path="/todo">
                        <TodoPage />
                    </Route>
                    <Route path="/">
                        <HomePage />
                    </Route>
                </Switch>
            </div>
        </HashRouter>
    )
}
