import { Link } from 'gatsby';
import React, { useState } from 'react';
import appLocale from '../../locale/en.json'
import './home.scss';

function Home() {

    const tabs = [
        {
            name: 'Eman Bio',
            to: '#bio',
            component: <UserBio />

        },
        {
            name: 'Research and Scholarship',
            to: '#research-and-scholarship'
        },
        {
            name: 'Publications',
            to: '#publictions'
        },
        { 
            name: 'Trips',
            to: '#trip'
        }]


    const [activeTab, setActiveTab] = useState(tabs[0]);

    function UserBio(){
        return (<div className="home__bio"> {appLocale['user-bio']} </div>)
    }


    return (<div className='home home-content'> 
                <ul className='nav nav-tabs nav-justified home__tabs'>
                        {tabs.map((tab) => (
                            <li className='nav-item home__tab-item'>
                                <Link 
                                    className={`nav-link ${ activeTab.to === tab.to  && 'home__tab-item--active'}`}
                                    aria-current="page" 
                                    to={tab.to} 
                                    onClick={() => setActiveTab(tab)}>{tab.name}</Link>
                            </li>
                        ))}
                </ul>

                <div>
                    {activeTab['component']}
                </div>
         </div>)
}

export default Home;