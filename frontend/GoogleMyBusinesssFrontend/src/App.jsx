import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom'
import GoogleLogin from './components/GoogleLogin'
import Dashboard from './components/Dashboard'
import PageNotFound from './components/PageNotFound'
import {GoogleOAuthProvider} from '@react-oauth/google'


function App() {
  const GoogleAuthWrapper = ()=>{
    return(
      <GoogleOAuthProvider clientId='154250790058-t7d20mqf4ipgju60d5spg4jr785vshnm.apps.googleusercontent.com'>
        <GoogleLogin> </GoogleLogin>
      </GoogleOAuthProvider>
    )
  }
  

  return (
    <>
      <BrowserRouter>
      <Routes>
        <Route path="/login" element={<GoogleAuthWrapper />} />
        <Route path="/" element={<Navigate to='/login'/>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<PageNotFound />} />

      </Routes>

      </BrowserRouter>
      
    </>
  )
}

export default App
