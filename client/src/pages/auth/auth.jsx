import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { useNavigate } from "react-router-dom";

import React, { useState, useRef } from "react";


// ValidatedTextField.js
const ValidatedTextField = ({ label, validator, onChange }) => {
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);
  const handleChange = e => {
    const newValue = e.target.value;
    const errorMessage = validator(newValue);
    setValue(newValue);
    setError(errorMessage);
    onChange(!errorMessage);
  };
  return (
    <TextField
      label={label}
      value={value}
      onChange={handleChange}
      error={!!error}
      helperText={error}
      margin="normal"
      required
      fullWidth
    />
  );
};

// validators.js
const loginValidator = value => {
  if (value.length < 3) return "Login must be at least 3 characters long";
  if (value.length > 20) return "Login must be less than 20 characters long";
  if (!/^[a-zA-Z ]+$/.test(value))
    return "Login must contain only letters and spaces";
  return false;
};

const passwordValidator = value => {
  if (value.length < 5) return "Password must be at least 5 characters long";
  if (value.length > 20) return "Password must be less than 20 characters long";
  return false;
};

// const emailValidator = value => {
//   if (!/^[a-zA-Z0-9._:$!%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$/.test(value))
//     return "Invalid email address";
//   return false;
// };
// FormValidation.js


export default function FormValidation() {
  const formValid = useRef({ login: false, password: false });
  const nav = useNavigate()

  const handleSubmit = e => {
    e.preventDefault();
    if (Object.values(formValid.current).every(isValid => isValid)) {
      sessionStorage.setItem("token", "")
      nav("/admin_panel")
    }
  };
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{  
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <ValidatedTextField
            label="Login"
            validator={loginValidator}
            onChange={isValid => (formValid.current.login = isValid)}
          />
          <ValidatedTextField
            label="Password"
            validator={passwordValidator}
            onChange={isValid => (formValid.current.password = isValid)}
          />
          <Button type="submit" variant="contained" fullWidth
            sx={{ mt: 3, mb: 2 }}>
            Submit
          </Button>
        </Box>
      </Box>
    </Container>
    
  );
}

