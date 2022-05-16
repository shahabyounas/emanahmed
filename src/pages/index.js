import * as React from "react"
import Header from "../components/header/Header"

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
      <title>Shahab Younas </title>
      <Header />
      {/* <img
        alt="Eman photo"
        src=""
      /> */}
    </main>
  )
}

export default IndexPage
