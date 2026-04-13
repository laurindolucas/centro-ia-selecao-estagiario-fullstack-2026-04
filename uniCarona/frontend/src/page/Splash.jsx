import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Splash.css";

import logo from "../assets/uniCaronaLogo.png";

export default function Splash() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/cadastro");
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="splash-container">
      <img src={logo} alt="Logo UniCarona" className="splash-logo" />
    </div>
  );
}