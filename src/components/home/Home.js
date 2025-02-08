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
        return <>
            <div className="home__bio">
            <h4 style={{ fontWeight: 'bold' }}> PhD Student Biomedical Engineering  </h4>
            Eman joined Rutgers Biomedical Engineering Department as a PhD student in 2022. She has a bachelor’s 
            in biomedical engineering from Rutgersand also a minor in mathematics. She conducted research on 
            <strong>nanoparticles characteristics in vitro and in silico </strong>. As a PhD student, she is interested in leveraging
             machine learning and nanobiomaterials for enhancing drug delivery.
            </div>

            <div className="home__bio">
            <h4 style={{ fontWeight: 'bold' }}> Bachelor’s Biomedical Engineering   </h4>
                Eman holds an undergraduate Biomedical Engineering degree from Rutgers School of Engineering and a
                minor in Mathematics. Nanotechnology is her key interest. Eman has experience creating computer simulations 
                for nanoparticles using Dissipative Particle Dynamics. Also, she conducted research to investigate the use 
                of gold nanoparticles in Hepatitis C diagnosis.
            </div>
        </>
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