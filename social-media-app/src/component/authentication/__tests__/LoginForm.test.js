import { render, screen } from "../../../helpers/test-utils";
import userEvent from "@testing-library/user-event";
import LoginForm from "../LoginForm";
import { faker } from "@faker-js/faker";
import userFixtures from "../../../helpers/fixtures/user";


const userData = userFixtures();

test("renders Login form", async () => {
  render(<LoginForm />);

  const loginFormElement = screen.getByTestId("login-form");
  expect(loginFormElement).toBeInTheDocument();

  const emailField = screen.getByTestId("email-field");
  expect(emailField).toBeInTheDocument();

  const passwordField = screen.getByTestId("password-field");
  expect(passwordField).toBeInTheDocument();

  const password = faker.lorem.slug(2);
  await userEvent.type(emailField, userData.email);
  await userEvent.type(passwordField, password);

  expect(emailField.value).toBe(userData.email);
  expect(passwordField.value).toBe(password);
});
