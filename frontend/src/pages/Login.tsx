import Form from "../components/Form";

function Login() {
  return (
    <div className="mt-8">
      <Form route="api/auth/" method="Login" />
    </div>
  );
}

export default Login;
