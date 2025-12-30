import React from "react";
import { useParams } from "react-router-dom";
import Layout from "../component/Layout";
import ProfileDetails from "../component/profile/ProfileDetail";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import Post from "../component/posts/Post";
import { Row, Col } from "react-bootstrap";

const Profile = () => {
  const { profileId } = useParams();

  const user = useSWR(`/users/${profileId}/`, fetcher);

  const posts = useSWR(`/post/?author__public_id=${profileId}`, fetcher, {
    refreshInterval: 20000,
  });

  return (
    <Layout hasNavigationBack>
      <Row className="justify-content-evenly">
        <Col sm={9}>
          <ProfileDetails profile={user.data} />
          <div>
            <Row className="my-4">
              {posts.data?.results.map((post, index) => (
                <Post key={index} post={post} refresh={posts.mutate} />
              ))}
            </Row>
          </div>
        </Col>
      </Row>
    </Layout>
  );
};

export default Profile;
