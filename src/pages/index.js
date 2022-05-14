import * as React from "react"

// styles
const pageStyles = {
  color: "#232129",
  padding: 96,
  fontFamily: "-apple-system, Roboto, sans-serif, serif",
}
const headingStyles = {
  marginTop: 0,
  marginBottom: 64,
  maxWidth: 320,
}
const headingAccentStyles = {
  color: "#663399",
}
const paragraphStyles = {
  marginBottom: 48,
}
const codeStyles = {
  color: "#8A6534",
  padding: 4,
  backgroundColor: "#FFF4DB",
  fontSize: "1.25rem",
  borderRadius: 4,
}


// markup
const IndexPage = () => {
  return (
    <main style={pageStyles}>
      <title>EmanAhamed </title>
      <h1 style={headingStyles}>
        Eman Ahmed Phd Scholar
        <br />
        <span style={headingAccentStyles}>— This site is for Eman</span>
        <span role="img" aria-label="Party popper emojis">
          🎉🎉🎉
        </span>
      </h1>
      <p style={paragraphStyles}>
        <span role="img" aria-label="Sunglasses smiley emoji">
          😎
        </span>
      </p>
      <img
        alt="Eman photo"
        src=""
      />
    </main>
  )
}

export default IndexPage
