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
    {
      resolve: "gatsby-plugin-google-gtag",
      options: {
        trackingIds: ["G-110M5L4JWS"], // Replace with your GA4 Measurement ID
        gtagConfig: {
          anonymize_ip: true, // GDPR compliance
        },
        pluginConfig: {
          head: true, // Loads script in <head>
        },
      },
    },
  ],
};