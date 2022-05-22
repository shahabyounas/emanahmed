module.exports = {
  siteMetadata: {
    title: `emanahmed`,
    siteUrl: `https://emanahmed.org`,
    menuLinks: [
      {
        "name": "home",
        "link": "/"
      },
      {
        "name": "blog",
        "link": "/blog"
      }
    ]
  },
  pathPrefix: "/",
  plugins: [
    {
    resolve: `gatsby-plugin-sass`,
  },
]
};