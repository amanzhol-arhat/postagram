import { render, screen } from "../../../helpers/test-utils";
import Post from "../Post";
import userFixtures from "../../../helpers/fixtures/user";
import postFixtures from "../../../helpers/fixtures/post";

// Mock the entire useUserActions module
jest.mock("../../../hooks/user.actions.js", () => ({
  __esModule: true,
  default: () => ({
    getUser: jest.fn(() => ({
      username: "testuser", // Provide a default mock user for getUser
      id: 1,
      // Add any other properties your Post component might need from `user` object
    })),
    // Add other functions if they are called directly in the test file
  }),
  // Mock raw functions if they are used directly in the test file outside the hook
  getUserRaw: jest.fn(() => ({
    username: "testuser",
    id: 1,
  })),
}));

const userData = userFixtures();
const postData = postFixtures();

beforeEach(() => {
  localStorage.clear();
  jest.clearAllMocks();

  // Directly set localStorage for testing `getUser` and other raw functions
  // This simulates a logged-in user for the tests
  localStorage.setItem(
    "auth",
    JSON.stringify({
      user: userData,
      access: "mockAccessToken",
      refresh: "mockRefreshToken",
    })
  );
});

test("render Post component", () => {
  render(<Post post={postData} />);
  const postElement = screen.getByTestId("post-test");
  expect(postElement).toBeInTheDocument();
});
