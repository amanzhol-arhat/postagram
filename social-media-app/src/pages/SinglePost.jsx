import React from "react";

import Layout from "../component/Layout";
import { Row, Col } from "react-bootstrap";
import { useParams } from "react-router-dom";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import Post from "../component/posts/Post";
import CreateComment from "../component/comment/CreateComment";
import Comment from "../component/comment/Comment";


function SinglePost() {
  console.log(useParams())
  let { postId } = useParams();

  const post = useSWR(`/post/${postId}/`, fetcher);

  const comments = useSWR(`/post/${postId}/comment/`, fetcher);

  return (
    <Layout hasNavigationBack>
      {post.data ? (
        <Row className="justify-content-center">
          <Col sm={8}>
            <Post post={post.data} refresh={post.mutate} isSinglePost />
            <CreateComment postId={post.data.id} refresh={comments.mutate} />
            {comments.data &&
              Array.isArray(comments.data.results) &&
              comments.data.results.map((comment, index) => (
                <Comment
                  key={index}
                  postId={post.data.id}
                  comment={comment}
                  refresh={comments.mutate}
                />
              ))}
          </Col>
        </Row>
      ) : (
        <div>Loading...</div>
      )}
    </Layout>
  );
}

export default SinglePost;
