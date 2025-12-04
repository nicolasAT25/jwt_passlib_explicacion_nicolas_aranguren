# **Descripción del problema 📖**

Se desea crear una pequeña API para una versión simplificada de una `Red Social`, donde para acceder a algunos de los servicios de la App se solicite autenticación de los usuarios.

# **Flujo de autenticación 👩🏻‍💻**

El proceso de autenticación consta de los siguientes pasos:

1. `Registrarse como usuarios en la DB`

    Por medio del endpoint destinado para la creación de usuarios, con un ***usuario*** y ***contraseña*** se crea el registro en la DB.

2. `Proceso de login`

    Una ves el usuario fue creado, en necesario su ***login*** para poder realizar ciertas peticiones a la ***App***/***API***.

    - El usuario ingresa sus credenciales (***usuario*** y ***contraseña***). Si el usuario no existe en la DB se muestra una excepción indicando que las credenciales son incorrectas.

    - Si el usuario existe, se compara la contraseña ingresada contra la contraseña "***hashed***" en la DB.

3. `Verificación de Token`

    - Si coinsiden estos dos *strings* del paso previo, se procede a tomar los datos enviados por el usuario (***usuario*** y ***contraseña***), se envía el ***user_id*** del usuario como data en el ***payload*** y se añade una llave más que contiene un datetime con la expiración de token (30 min).

    - Luego se codifica toda esta información con el algoritmo seleccionado, junto con un ***Secret Key*** creando así el ***access token***.

    - Para su verificación se toma el ***access token***, se decodifica utilizando de nuevo el ***Secret Key*** y se retorna el ***user_id***. Si no es posible extraer el ***user_id*** se muestra una excepción.

# `Descripción del uso de Passlib`

***Passlib*** permite utilizar diferentes algoritmos para aplicar un ***hash*** a las contraseñas.

- Se crea un ***context*** (clase ***CryptContext*** de ***Passlib***) el cual aplica un algoritmo de ***hash*** a la contraseña igresada por el usuario al registrarse en la App.

- Cuando el usuario ya registrado quiere hacer *login*, se toma la contraseña "plana" y se verifica contra la contraseña con ***hash*** guardada en DB.

- Esta verificación la realiza el método ***verify*** de la clase ***CryptContext***.

# `Ejemplo Payload JWT generado`

```python
Ejemplo
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3NjQ4MTU5NjN9.YcWzc5QweQwDRprxM6J34sKnmrr8vnjp19aY5uw5Wb8"
```
- Decodificación ***Payload***: la fecha de expiración se muestra como "*Tiempo unix*", que es una representación de segundos desde el 1 de enero de 1970 a las 00:00:00 UTC.

```python
{
"user_id": 3,
"exp": 1764815963
}
```

# 💡 `Conclusiones` 💡

## Seguridad

- `JWT`: es un método bastante eficiente para la autenticación de usuarios, donde no es necesatio guardar en el backend, API o DB que el usuario inició o no sesión. Garantiza seguridad para el usuario al contar con un tiempo de expiración.

- `Passlib`: altamete recomendado para respetar la confidencialidad de los usuarios al guardar las contraseñas codificadas. En caso de filtración de datos de los usuarios, las contraseñas estarán seguras además de toda la autenticación con JWT.

## Buenas prácticas

- Utilizar **FastAPI** como framework para crear APIs ya que facilita la generación automática de documentación con ***Swagger*** o ***ReDoc***.

- Probar el funcionamiento de los endpoints de las APIs con herramientas como ***Postman*** es bastante útil al poder ejecutar el flujo del proceso de las APIs y visualizar las respuestas/errores esperadas/os.

- Utilizar variables de entorno con ***.env*** para no exponer datos sensibles en repositorios públicos o incluso privados.

## Aprendizajes

- La implementación de **DBs**, **JWT**, **Passlib** aprendida durante este proyecto es replicable a diferentes casos de negocio donde la creación y autenticación de usuarios sea requerida.

- Implementar la dependencia de conexión a la DB y/o autenticación de usuarios para acceder a las operaciones o serviciios de nuestras APIs garantiza la seguridad y consistencia de los proyectos.