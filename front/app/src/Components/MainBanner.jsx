import React from "react";
import "./css/MainBanner.css";

function MainBanner({ bannerColor, title, description, imagesrc}) {
    return (
        <section className="MainBanner">
            <div className="BannerBox" style={{backgroundColor: bannerColor}}>
                <div className="BannerTextBox">
                    <div className="BannerText">
                        <h1 className="Title">{title}</h1>
                        <p className="Description">{description}</p>
                    </div>
                </div>
                <div className="BannerImage">
                    <img className="image" src={imagesrc} alt="Main_Banner"/>
                </div>
            </div>
        </section>
    );
}

export default MainBanner;