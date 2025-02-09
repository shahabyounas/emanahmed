import './style.scss'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import "@popperjs/core/dist/umd/popper.min.js";


export const onRouteUpdate = ({ location }) => {
    if (window && window.gtag) {
      window.gtag("event", "page_view", {
        page_path: location.href,
      });
    }
  };