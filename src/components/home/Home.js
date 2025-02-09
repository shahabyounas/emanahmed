import { Link } from 'gatsby';
import React, { useState } from 'react';
import './home.scss';

function Home() {

    const tabs = [
        {
            name: 'Education',
            to: '#bio',
            component: <UserBio />

        },
        {
            name: 'Research and Scholarship',
            to: '#research-and-scholarship',
            component: <ResearchandScholarship />
        },
        {
            name: 'Publications',
            to: '#publictions',
            component: <Publications />
        },
        { 
            name: 'Trips',
            to: '#trip',
            component: <Trips />
        }]



    const [activeTab, setActiveTab] = useState(()=> {
        if(typeof window !== 'undefined'){
            let selectedTab = window.location.href.split('#')[1]
            return selectedTab ?  `#${selectedTab}` : tabs[0].to
        }
        return tabs[0].to
    });

    console.log(window.location.href)


    return (<div className='home home-content'>
                <ul className='nav nav-tabs nav-justified home__tabs'>
                        {tabs.map((tab) => (
                            <li className='nav-item home__tab-item'>
                                <Link 
                                    className={`nav-link ${ activeTab === tab.to  && 'home__tab-item--active'}`}
                                    aria-current="page" 
                                    to={tab.to} 
                                    onClick={() => setActiveTab(tab.to)}>{tab.name}</Link>
                            </li>
                        ))}
                </ul>

                <div>
                    {tabs.filter((tab) => tab.to === activeTab)[0].component}
                </div>
         </div>)
}

function UserBio(){
    return <>
        <div className="home__bio">
        <h4 style={{ fontWeight: 'bold' }}> PhD Student Biomedical Engineering  </h4>
        Eman joined Rutgers Biomedical Engineering Department as a PhD student in 2022. She has a bachelor’s 
        in biomedical engineering from Rutgersand also a minor in mathematics. She conducted research on 
        <strong> nanoparticles characteristics in vitro and in silico </strong>. As a PhD student, she is interested in leveraging
          <strong> machine learning and nanobiomaterials for enhancing drug delivery </strong>.
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

function ResearchandScholarship(){
    return <>
        <div className="home__bio">
        <h4 style={{ fontWeight: 'bold' }}> Fellowship  </h4>
         Eman was awarded one year Fellowship at University of Rutgers, USA.
        </div>

        <div className="home__bio">
        <h4 style={{ fontWeight: 'bold' }}> Scholarship </h4>
          Eman was awarded fully funded scholarship under the USAID higher education initiative to study Biomedical Engineering at Rutgers University, USA. 
        </div>
    </>
}

function Publications(){
    return <>
        <div className="home__bio">
        <h4 style={{ fontWeight: 'bold' }}> Publications </h4>
        <h5 className='mt-3'> Mapping Biomaterial Complexity by Machine Learning  </h5>
        <h5 className='mt-4'> <em> <strong> Abstract </strong> </em> </h5>
        <div> 
         <i>Biomaterials often have subtle properties that ultimately drive their bespoke performance. Given this nuanced structure–function behavior,
         the standard scientific approach of one experiment at a time or design of experiment methods is largely inefficient for the discovery of 
         complex biomaterials. More recently, high-throughput experimentation coupled with machine learning methods has matured beyond expert users 
         allowing scientists and engineers from diverse backgrounds to access these powerful data science tools. As a result, we now have the 
         opportunity to strategically utilize all available data from high-throughput experiments to train efficacious models and map the 
         structure-function behavior of biomaterials for their discovery. Herein, we discuss this necessary shift to data-driven determination 
         of structure–function properties of biomaterials as we highlight how machine learning is leveraged in identifying physicochemical cues 
         for biomaterials in tissue engineering, gene delivery, drug delivery, protein stabilization, and antifouling materials. We also discuss
        data-mining approaches that are coupled with machine learning to map biomaterial functions that reduce the load on experimental 
        approaches for faster biomaterial discovery. Ultimately, harnessing the prowess of machine learning will lead to accelerated discovery
        and development of optimal biomaterial designs.</i>
        </div>
        <p className='mt-4'>
        <strong> Publication Link </strong> 
        <a href='https://pubmed.ncbi.nlm.nih.gov/39135398/' rel='noreferrer' target='_blank'> https://pubmed.ncbi.nlm.nih.gov/39135398/ </a>
        </p>
       </div>
    </>
}

function Trips(){
    return <>
        <div className="home__bio">
        <h4 style={{ fontWeight: 'bold' }}>  BIG  Symposium New York City  </h4>
        <div>
            The Bio-Inspired Green (BIG) Science & Technology Symposium 2024
        </div>
        </div>
    </>
}


export default Home;