import { StaticQuery, graphql } from 'gatsby';
import React from 'react';


const Layout = ({ children }) => (
    <StaticQuery
      query={graphql`
        query SiteTitleQuery {
          site {
            siteMetadata {
              title
               menuLinks {
                 name
                 link
               }
            }
          }
        }
      `}
      render={data => (
        <React.Fragment>
            {children}
        </React.Fragment>
      )}
    />
  )

export default Layout;