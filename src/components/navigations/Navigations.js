import { Link } from 'gatsby';
import React from 'react';
import './navigations.scss';


function Navigations(props){
     const { menuLinks } = props;
    return (
    <>
        <div> 
          <nav>
            <ul className="navigation nav justify-content-end"> 
                {
                  menuLinks.map((menuLink) => 
                  <li
                    key={menuLink.link}
                    className="nav-item navigation__nav-item"
                  > 
                    <Link className="navigation__link nav-link" to={menuLink.link}>{menuLink.name}</Link>
                  </li>)
                }
            </ul>
          </nav>
        </div>
    </>)
}

export default Navigations;

