import { render, screen } from './helpers/test-utils';
import App from "./App";


test("renders Welcome to Arhatogram text", () => {
  render(
      <App/>
  );
  const textElement =
    screen.getByText(/Welcome to Arhatogram!/i);
  expect(textElement).toBeInTheDocument();
});
