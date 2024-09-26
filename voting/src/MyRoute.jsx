import React from 'react'
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom'
import Register from './auth/Register'
import Login from './auth/Login'
import NotFound from './NotFound'
import Profile from './auth/Profile'
const MyRoute = () => {
  return (
    <Router>
    

        <Routes>
           <Route path='/' element={<Register/>}/>
           <Route path='/login' element={<Login/>}/>
           <Route path='/profile' element={<Profile/>}/>
           <Route path='/*' element={<NotFound/>}/>
        </Routes>
    </Router>
  )
}

export default MyRoute