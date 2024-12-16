import Form from "../components/Form";

function Register() {
  return (
    <div className="mt-8">
      <Form route="api/user/create/" method="Register" />
    </div>
  );
}

export default Register;
