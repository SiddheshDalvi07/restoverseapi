import React from 'react'
import { useNavigate } from 'react-router-dom'

function PageNotFound() {
    const navigate = useNavigate()
  return (
    <>
    <div>PageNotFound</div>
    <button onClick={()=>navigate('/login')}>Login</button>
    </>
    
  )
}

export default PageNotFound