import React from 'react';
import PropTypes from 'prop-types';
import defaultImage  from '../../images/eman-profile.png';
import './user-detail.scss'


function UserDetail(props) {
    const { name, title, discipline, image, school } = props;
    return (<div>
                <div className="user-detail__top-bar">
                    <div className='user-detail__text'>
                        <img width="100" height="100" src={ image || defaultImage} alt="profile" className="mt-1" />
                        <div className='user-detail__title'>
                            <span className="user-detail__name">{name}</span>
                            <div> {title}</div>
                            <div> {discipline}</div>
                            <div> {school}</div>
                            <div className='email'>
                                <span style={{ fontSize: '1.5em', color: 'white' }}> &#9758; </span>
                                <strong> <em> <a style={{ textDecoration: 'none', color: 'white' }} href="mailto:eman.ahmed@rutgers.edu">Contact Eman</a> </em> </strong> 
                            </div>
                        </div>
                    </div>
                </div>
    </div> );
}


UserDetail.propTypes = {
    name: PropTypes.string,
    title: PropTypes.string,
    discipline: PropTypes.string,
}


UserDetail.defaultProps = {
    name: 'Eman Ahmed',
    title: 'Phd Scholar Rutgers',
    discipline: 'Biomedical Engineering',
    school: 'Rutgers, School of Engineering'
}


export default  UserDetail;