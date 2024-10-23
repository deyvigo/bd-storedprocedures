#### POST /signup/admin

```javascript
body = {
  "nombre": "Nombre",
  "apellido_pat": "Apellido Paterno",
  "apellido_mat": "Apellido Materno",
  "fecha_nacimiento": "2000-01-01",
  "dni": "12345678",
  "sexo": "Masculino",
  "telefono": "123456789",
  "correo": "correo@correo.com",
  "username": "username",
  "password": "password"
}
```

#### POST /signup/client

```javascript
body = {
  "nombre": "Nombre",
  "apellido_pat": "Apellido Paterno",
  "apellido_mat": "Apellido Materno",
  "fecha_nacimiento": "2000-01-01",
  "dni": "12345678",
  "sexo": "Masculino",
  "telefono": "123456789",
  "correo": "correo@correo.com",
  "username": "username",
  "password": "password"
}
```

#### POST /login/admin
```javascript
body = {
  "username": "username",
  "password": "12345678"
}
```

#### POST /login/client
```javascript
body = {
  "username": "username",
  "password": "12345678"
}
```

#### GET /helloworld/public

#### GET /helloworld/private JWT