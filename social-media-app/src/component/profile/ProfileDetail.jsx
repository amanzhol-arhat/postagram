import React from "react";
import { Button, Image } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import useUserActions from "../../hooks/user.actions";

const ProfileDetail = (props) => {
  const { profile } = props;
  const { getUser } = useUserActions();
  const loggedInUser = getUser();
  const navigate = useNavigate();

  if (!profile) {
    return <div>Loading...</div>;
  }

  const { first_name, last_name, bio, posts_count, id, avatar } = profile;

  return (
    <div>
      <div className="d-flex flex-row border-bottom p-5">
        <Image
          src={avatar}
          roundedCircle
          width={120}
          height={120}
          className="me-5 border border-primary border-2"
        />
        <div className="d-flex flex-column justify-content-start align-self-center mt-2">
          <p className="fs-4 m-0">
            {first_name} {last_name}
          </p>
          <p className="fs-5"></p>
          <p className="fs-6">
            <small>{bio || "(No bio.)"}</small>
          </p>
          {loggedInUser && loggedInUser.id === id && (
            <Button
              variant="primary"
              size="sm"
              onClick={() => navigate(`/profile/${id}/edit/`)}
            >
              Edit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileDetail;
