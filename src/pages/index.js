import * as React from "react"
import Home from "../components/home"
import Layout from "../components/Layout"
import UserDetail from "../components/user-detail"

// styles
const  pageStyles = {
  color: "#232129",
  fontFamily: "-apple-system, Roboto, sans-serif, serif",
  width: '100%',
  margin: 0,
  padding: 0,
}



// markup
const IndexPage = () => {
  return (
    <main style={pageStyles}> 
      <title> Eman Ahmed | Phd </title>
      <Layout>
        <UserDetail />
        <Home />
      </Layout>
    </main>
  )
}

export default IndexPage
