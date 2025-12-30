import React, { useState, useContext } from "react";
import { format } from "timeago.js";
import {
  LikeFilled,
  CommentOutlined,
  LikeOutlined,
  MoreOutlined,
} from "@ant-design/icons";
import { Button, Modal, Form, Dropdown, Card, Image } from "react-bootstrap";
import axiosService from "../../helpers/axios";
import { Link } from "react-router-dom";
import useUserActions from "../../hooks/user.actions.js";
import UpdatePost from "./UpdatePost";
import {Context} from "../Layout";


const MoreToggleIcon = React.forwardRef(({ onClick }, ref) => (
  <Link
    to="#"
    ref={ref}
    onClick={(e) => {
      e.preventDefault();
      onClick(e);
    }}
  >
    <MoreOutlined />
  </Link>
));

function Post(props) {
  const { post, refresh, isSinglePost } = props;
  const userActions = useUserActions();
  const user = userActions.getUser();


  const { setToaster } = useContext(Context);

  const handleShowToast = (message, type) => {
    setToaster({
      title: "Post",
      message,
      type,
      show: true,
    });
  };


  const handleLikeClick = (action) => {
    axiosService
      .post(`/post/${post.id}/${action}/`)
      .then(() => {
        refresh();
      })
      .catch((err) => console.error(err));
  };

  const handleDelete = () => {
    axiosService
      .delete(`/post/${post.id}/`)
      .then(() => {
        handleShowToast("Post deleted", "danger");
        refresh();
      })
      .catch((err) => console.error(err));
  };
  return (
    <>
      <Card className="rounded-3 my-4"
            data-testid="post-test">
        <Card.Body>
          <Card.Title className="d-flex flex-row justify-content-between">
            <div className="d-flex flex-row">
              <Image
                src={post.author.avatar}
                roundedCircle
                width={48}
                height={48}
                className="me-2 border border-primary border-2"
              />
              <div
                className="d-flex flex-column
              justify-content-start
              align-self-center mt-2"
              >
                <p className="fs-6 m-0">{post.author.username}</p>
                <p className="fs-6 fw-lighter">
                  <small>{format(post.created_at)}</small>
                </p>
              </div>
            </div>
            {user.username === post.author.username && (
              <div>
                <Dropdown>
                  <Dropdown.Toggle as={MoreToggleIcon}></Dropdown.Toggle>
                  <Dropdown.Menu>
                    <UpdatePost
                      post={post}
                      refresh={refresh}
                      showToast={handleShowToast}
                    />
                    <Dropdown.Item
                      onClick={handleDelete}
                      className="text-danger"
                    >
                      Delete
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </div>
            )}
          </Card.Title>
          <Card.Text>{post.body}</Card.Text>
          <div className="d-flex flex-row">
            <LikeFilled
              style={{
                color: "#fff",
                backgroundColor: "#0D6EFD",
                borderRadius: "50%",
                width: "18px",
                height: "18px",
                fontSize: "75%",
                padding: "2px",
                margin: "3px",
              }}
            />
            <p className="ms-1 fs-6">
              <small>{post.likes_count} like</small>
            </p>
          </div>
        </Card.Body>
        <Card.Footer
          className="d-flex bg-white w-50
                              justify-content-between border-0"
        >
          <div className="d-flex flex-row">
            <LikeOutlined
              style={{
                width: "24px",
                height: "24px",
                padding: "2px",
                fontSize: "20px",
                color: post.liked ? "#0D6EFD" : "#C4C4C4",
              }}
              onClick={() => {
                if (post.liked) {
                  handleLikeClick("remove_like");
                } else {
                  handleLikeClick("like");
                }
              }}
            />
            <p className="ms-1">
              <small>Like</small>
            </p>
          </div>
          {!isSinglePost && (
            <div className="d-flex flex-row">
              <Link
                to={`/post/${post.id}/`}
                className="d-flex flex-row text-decoration-none text-dark"
              >
                <CommentOutlined
                  style={{
                    width: "24px",
                    height: "24px",
                    padding: "2px",
                    fontSize: "20px",
                    color: "#C4C4C4",
                  }}
                />
                <p className="ms-1 mb-0">
                  <small>{post.comments_count} Comment</small>
                </p>
              </Link>
            </div>
          )}
        </Card.Footer>
      </Card>
    </>
  );
}

export default Post;
