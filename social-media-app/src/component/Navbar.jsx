import React from "react";
import { Navbar, Container, Image, NavDropdown, Nav } from "react-bootstrap";
import { useNavigate, Link } from "react-router-dom";
import useUserActions from "../hooks/user.actions"



function Navigationbar() {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem("auth");
    navigate("/login/");
  };
  const userActions = useUserActions();
  const user = userActions.getUser();

  return(
    <Navbar bg="primary" variant="dark">
      <Container>
        <Navbar.Brand className="fw-bold" href="#home">
          Arhatogram
        </Navbar.Brand>
        <Navbar.Collapse className="justify-content-end">
          <Nav>
            <NavDropdown title={
              <Image
                src={ user.avatar }
                roundedCircle
                width={36}
                height={36}
              />
            }>
              <NavDropdown.Item as={Link} to={`/profile/${user.id}/`}>
                Profile
              </NavDropdown.Item>
              <NavDropdown.Item onClick={handleLogout}>
              Logout</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigationbar;
