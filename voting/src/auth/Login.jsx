import React,{useState} from 'react'
import {Helmet} from "react-helmet";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import {useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate=useNavigate()

    const [username,setUsername]=useState('')
    const [password,setPassword]=useState('')

    const handleSubmit=async(e)=>{
        e.preventDefault()

        try{
            const {data}=await axios.post('http://localhost:8000/api/login/',{
                username,
                password
            })
            //save data in local storage
            localStorage.setItem('user',JSON.stringify(data))
            navigate('/profile')
        }
        catch(err){
            toast.error(err.response.data.err)
        }
    }
  return (
    
    <>
      
    
    <Helmet>
        <title>Login</title>
        <meta name="description" content="voting,posts" />
    </Helmet>

    <ToastContainer theme='colored' position='top-center'/>
    <div className="contaiber my-3">
        <div className="row d-flex justify-content-center">
            <div className="col md-5">
                <form className="py-3 shadow" onSubmit={handleSubmit}>
                    <div className="my-3">

                    <label htmlFor="username">Username</label>
                    <input 
                    type="text"
                    name="username" 
                    id="username"
                    className='form-control'
                    onChange={e=>setUsername(e.target.value)}
                    value={username}
                    required
                    />

                    </div>

                    <div className="my-3">
                        <label htmlFor="password">Password</label>
                        <input 
                        type="password" 
                        name="password" 
                        id="password" 
                        className='form-control'
                        onChange={e=>setPassword(e.target.value)}
                        value={password}
                        required
                        />

                    </div>

                    <div className="my-2">
                        <input type="submit" value="Login" className='btn btn-primary' />
                    </div>
                </form>
            </div>
        </div>
    </div>
    </>
  )
}

export default Login