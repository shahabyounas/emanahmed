import React from 'react';
import PropTypes from 'prop-types';
import defaultImage  from '../../images/eman-cairo.jpeg';
import './header.scss'


function Header(props) {
    const { name, title, discipline, image, school } = props;
    return (<div>
                <div className="header__top-bar">
                    <div className='header__text'>
                        <img width="100" height="100" src={ image || defaultImage} alt="profile" className="mt-3" />
                        <div className='header__title'>
                            <span className="header__name">{name}</span>
                            <div> {title}</div>
                            <div> {discipline}</div>
                            <div> {school}</div>
                        </div>
                    </div>
                </div>
    </div> );
}


Header.propTypes = {
    name: PropTypes.string,
    title: PropTypes.string,
    discipline: PropTypes.string,
}


Header.defaultProps = {
    name: 'Eman Ahmed',
    title: 'Phd Scholar Retgers',
    discipline: 'Biomedical Engineering',
    school: 'Rutgers, School of Engineering'
}


export default  Header;