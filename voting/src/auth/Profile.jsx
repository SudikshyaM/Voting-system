import React from 'react'

const Profile = () => {
    const data=JSON.parse(localStorage.getItem('user'))
  return (
    <>
       <h2>
        {data.token}
       </h2>
    </>
  )
}

export default Profile