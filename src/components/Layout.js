import { StaticQuery, graphql } from 'gatsby';
import React from 'react';
import Navigations from './navigations/Navigations';


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
        <Navigations menuLinks={data.site.siteMetadata.menuLinks} siteTitle={data.site.siteMetadata.title} />
          <div>
            {children}
          </div>
        </React.Fragment>
      )}
    />
  )

export default Layout;